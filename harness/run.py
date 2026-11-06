"""Run the hardness test against provider APIs.

Usage (from the repo root):
    python -m harness.run --condition A
    python -m harness.run --condition B --models anthropic=claude-opus-4-1 openai=gpt-5

One request per case per model. Temperature 0 where the model accepts it.
No content retries: a model gets one answer. If that answer cannot be parsed,
the harness sends one format-only re-request (no new content); if the result
is still unparseable the case is scored as a miss and logged as a parse failure.
"""
import argparse
import json
import sys
from datetime import date

from .config import CONDITIONS, FORMAT_ONLY_REREQUEST, RESULTS, WORK
from .parse import ParseError, parse_reply
from .prompts import case_prompt, prompt_hash
from .providers import ALL_PROVIDERS, CallStats, TransportError


def ask_once(provider, model, prompt):
    """One attempt at the answer, plus at most one format-only re-request."""
    stats = CallStats()
    turns = [{"role": "user", "content": prompt}]
    first = provider.chat(model, turns, stats)
    rec = {"attempt_text": first, "format_rerequest": False, "rerequest_text": None}
    try:
        rec["parsed"], rec["parse_status"] = parse_reply(first), "ok"
    except ParseError:
        rec["format_rerequest"] = True
        turns += [{"role": "assistant", "content": first}, {"role": "user", "content": FORMAT_ONLY_REREQUEST}]
        second = provider.chat(model, turns, stats)
        rec["rerequest_text"] = second
        try:
            rec["parsed"], rec["parse_status"] = parse_reply(second), "ok_after_rerequest"
        except ParseError:
            rec["parsed"], rec["parse_status"] = None, "unparseable"
    rec["transport_retries"], rec["notes"] = stats.transport_retries, stats.notes
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--condition", choices=CONDITIONS, required=True)
    ap.add_argument("--cases", default=str(WORK / "candidates.json"), help="JSON list of {id, facts, ...}")
    ap.add_argument("--models", nargs="*", default=[], help="override flagship pick, e.g. openai=gpt-5")
    ap.add_argument("--out", default=str(RESULTS / "raw_responses.jsonl"))
    args = ap.parse_args(argv)

    overrides = dict(m.split("=", 1) for m in args.models)
    cases = json.load(open(args.cases))
    providers = [P() for P in ALL_PROVIDERS]
    live = [p for p in providers if p.available]
    for p in providers:
        if not p.available:
            print(f"[skip] {p.name}: {p.env_key} not set", file=sys.stderr)
    if not live:
        sys.exit("No API keys found. Use the subagent panel fallback (python -m harness.panel) and disclose it.")

    # Pick each provider's flagship from its live model list unless overridden.
    panel = []
    for p in live:
        model = overrides.get(p.name) or p.pick_flagship(p.list_models())
        print(f"[model] {p.name}: {model}", file=sys.stderr)
        panel.append((p, model))

    run_date = date.today().isoformat()
    with open(args.out, "a") as out:
        for p, model in panel:
            for c in cases:
                prompt = case_prompt(c["facts"], args.condition)
                try:
                    rec = ask_once(p, model, prompt)
                except TransportError as e:
                    rec = {"attempt_text": None, "parsed": None, "parse_status": "transport_failure",
                           "format_rerequest": False, "rerequest_text": None, "transport_retries": None, "notes": [str(e)]}
                rec.update(run_date=run_date, mode="api", condition=args.condition, provider=p.name,
                           model_id=model, case_id=c["id"], prompt_sha=prompt_hash(prompt))
                out.write(json.dumps(rec) + "\n")
                print(f"{p.name} {c['id']} {rec['parse_status']} {(rec.get('parsed') or {}).get('label')}", file=sys.stderr)


if __name__ == "__main__":
    main()
