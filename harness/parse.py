"""Parse model replies into {label, reasoning, citation, deciding_fact}."""
import json
import re

from .config import LABELS


class ParseError(ValueError):
    pass


def _first_json_object(text: str) -> dict:
    """Pull the first JSON object out of a reply, tolerating code fences or prose around it."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    # Fall back to the first balanced {...} span.
    start = text.find("{")
    while start != -1:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(text[start : i + 1])
                        if isinstance(obj, dict):
                            return obj
                    except json.JSONDecodeError:
                        break
        start = text.find("{", start + 1)
    raise ParseError("no JSON object found")


def normalize(obj: dict) -> dict:
    """Validate keys and normalize the label. Raises ParseError on a bad label."""
    label = str(obj.get("label", "")).strip().lower()
    label = {"comply": "complies", "violate": "violates", "depend": "depends"}.get(label, label)
    if label not in LABELS:
        raise ParseError(f"bad label {obj.get('label')!r}")
    df = obj.get("deciding_fact")
    if isinstance(df, str) and df.strip().lower() in ("", "null", "none", "n/a"):
        df = None
    return {
        "label": label,
        "reasoning": str(obj.get("reasoning", "")).strip(),
        "citation": str(obj.get("citation", "") or "").strip(),
        "deciding_fact": df,
    }


def parse_reply(text: str) -> dict:
    return normalize(_first_json_object(text))
