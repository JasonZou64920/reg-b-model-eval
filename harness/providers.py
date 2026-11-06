"""Provider clients: list models, pick the current flagship, send one prompt.

Standard library only (urllib), so the harness runs without installing SDKs.
Every request goes through `http_json`, which retries 429 and 5xx responses
with exponential backoff and full jitter. Those transport retries are counted
and logged but never count as an attempt at the answer.
"""
import json
import os
import random
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from .config import (BACKOFF_BASE_SECONDS, BACKOFF_CAP_SECONDS, MAX_OUTPUT_TOKENS,
                     MAX_TRANSPORT_RETRIES, REQUEST_TIMEOUT_SECONDS)


class TransportError(RuntimeError):
    """Raised when retries are exhausted or a non-retryable HTTP error occurs."""

    def __init__(self, status, body):
        super().__init__(f"HTTP {status}: {body[:300]}")
        self.status, self.body = status, body


@dataclass
class CallStats:
    transport_retries: int = 0
    notes: list = field(default_factory=list)


def _sleep_for(attempt: int, retry_after: str | None) -> float:
    """Full-jitter exponential backoff, honoring Retry-After when the server sends one."""
    if retry_after:
        try:
            return min(float(retry_after), BACKOFF_CAP_SECONDS)
        except ValueError:
            pass
    return random.uniform(0, min(BACKOFF_CAP_SECONDS, BACKOFF_BASE_SECONDS * 2 ** attempt))


def http_json(method, url, headers=None, payload=None, stats=None, opener=urllib.request.urlopen, sleep=time.sleep):
    """Send a JSON request and return the decoded JSON body.

    `opener` and `sleep` are injectable so the retry logic can be unit tested
    without network access.
    """
    stats = stats or CallStats()
    data = json.dumps(payload).encode() if payload is not None else None
    hdrs = {"content-type": "application/json", **(headers or {})}
    for attempt in range(MAX_TRANSPORT_RETRIES + 1):
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            with opener(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace") if hasattr(e, "read") else ""
            retryable = e.code == 429 or 500 <= e.code < 600
            if not retryable or attempt == MAX_TRANSPORT_RETRIES:
                raise TransportError(e.code, body)
            stats.transport_retries += 1
            sleep(_sleep_for(attempt, e.headers.get("retry-after") if e.headers else None))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt == MAX_TRANSPORT_RETRIES:
                raise TransportError(-1, str(e))
            stats.transport_retries += 1
            sleep(_sleep_for(attempt, None))
    raise AssertionError("unreachable")


# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------
class Provider:
    name = "base"
    env_key = ""

    def __init__(self, http=http_json):
        self.key = os.environ.get(self.env_key, "")
        self.http = http

    @property
    def available(self) -> bool:
        return bool(self.key)

    def list_models(self) -> list:
        raise NotImplementedError

    def pick_flagship(self, models: list) -> str:
        raise NotImplementedError

    def chat(self, model: str, turns: list, stats: CallStats) -> str:
        """turns: [{'role': 'user'|'assistant', 'content': str}, ...] -> reply text."""
        raise NotImplementedError

    def _with_temperature_fallback(self, send, stats):
        """Ask for temperature 0; if the model rejects the parameter, resend without it and log that."""
        try:
            return send(True)
        except TransportError as e:
            if e.status == 400 and "temperature" in e.body.lower():
                stats.notes.append("temperature_unsupported")
                return send(False)
            raise


class Anthropic(Provider):
    name, env_key = "anthropic", "ANTHROPIC_API_KEY"
    base = "https://api.anthropic.com/v1"
    # Tier order used to identify the flagship family; newest model in the top tier wins.
    TIERS = ("mythos", "opus", "sonnet", "haiku")

    def _h(self):
        return {"x-api-key": self.key, "anthropic-version": "2023-06-01"}

    def list_models(self):
        out, after = [], None
        while True:
            url = f"{self.base}/models?limit=100" + (f"&after_id={after}" if after else "")
            r = self.http("GET", url, self._h())
            out += r.get("data", [])
            if not r.get("has_more"):
                return out
            after = r.get("last_id")

    def pick_flagship(self, models):
        def tier(m):
            mid = m["id"].lower()
            return next((i for i, t in enumerate(self.TIERS) if t in mid), len(self.TIERS))
        best = min(models, key=lambda m: (tier(m), -_ts(m.get("created_at"))))
        return best["id"]

    def chat(self, model, turns, stats):
        def send(with_temp):
            body = {"model": model, "max_tokens": MAX_OUTPUT_TOKENS, "messages": turns}
            if with_temp:
                body["temperature"] = 0
            r = self.http("POST", f"{self.base}/messages", self._h(), body, stats)
            return "".join(b.get("text", "") for b in r.get("content", []) if b.get("type") == "text")
        return self._with_temperature_fallback(send, stats)


class OpenAI(Provider):
    name, env_key = "openai", "OPENAI_API_KEY"
    base = "https://api.openai.com/v1"
    EXCLUDE = ("mini", "nano", "audio", "realtime", "search", "transcribe", "tts", "image", "embedding", "moderation", "codex", "instruct")

    def _h(self):
        return {"authorization": f"Bearer {self.key}"}

    def list_models(self):
        return self.http("GET", f"{self.base}/models", self._h()).get("data", [])

    def pick_flagship(self, models):
        cands = [m for m in models if m["id"].startswith("gpt-") and not any(x in m["id"] for x in self.EXCLUDE)]
        # Prefer undated aliases (e.g. 'gpt-5') over dated snapshots when created times tie.
        return max(cands, key=lambda m: (m.get("created", 0), -len(m["id"])))["id"]

    def chat(self, model, turns, stats):
        def send(with_temp):
            body = {"model": model, "input": turns, "max_output_tokens": MAX_OUTPUT_TOKENS}
            if with_temp:
                body["temperature"] = 0
            r = self.http("POST", f"{self.base}/responses", self._h(), body, stats)
            if r.get("output_text"):
                return r["output_text"]
            return "".join(c.get("text", "") for o in r.get("output", []) for c in o.get("content", []) or [] if c.get("type") == "output_text")
        return self._with_temperature_fallback(send, stats)


class Gemini(Provider):
    name, env_key = "google", "GEMINI_API_KEY"
    base = "https://generativelanguage.googleapis.com/v1beta"

    def list_models(self):
        out, token = [], None
        while True:
            url = f"{self.base}/models?pageSize=1000&key={self.key}" + (f"&pageToken={token}" if token else "")
            r = self.http("GET", url)
            out += r.get("models", [])
            token = r.get("nextPageToken")
            if not token:
                return out

    def pick_flagship(self, models):
        cands = [m for m in models if "generateContent" in m.get("supportedGenerationMethods", [])
                 and "-pro" in m["name"] and not any(x in m["name"] for x in ("vision", "tts", "image", "embedding"))]
        # Highest version number wins; Google names models like 'models/gemini-2.5-pro'.
        def ver(m):
            import re
            nums = re.findall(r"gemini-(\d+(?:\.\d+)?)", m["name"])
            return (float(nums[0]) if nums else 0.0, "preview" not in m["name"] and "exp" not in m["name"])
        return max(cands, key=ver)["name"].removeprefix("models/")

    def chat(self, model, turns, stats):
        contents = [{"role": "model" if t["role"] == "assistant" else "user", "parts": [{"text": t["content"]}]} for t in turns]
        def send(with_temp):
            cfg = {"maxOutputTokens": MAX_OUTPUT_TOKENS, "responseMimeType": "application/json"}
            if with_temp:
                cfg["temperature"] = 0
            r = self.http("POST", f"{self.base}/models/{model}:generateContent?key={self.key}", None,
                          {"contents": contents, "generationConfig": cfg}, stats)
            cands = r.get("candidates") or [{}]
            return "".join(p.get("text", "") for p in cands[0].get("content", {}).get("parts", []))
        return self._with_temperature_fallback(send, stats)


def _ts(created_at) -> float:
    """Anthropic returns ISO timestamps; convert to a sortable number."""
    from datetime import datetime
    if not created_at:
        return 0.0
    try:
        return datetime.fromisoformat(created_at.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


ALL_PROVIDERS = (Anthropic, OpenAI, Gemini)
