"""Fallback panel: export prompts for subagent models and import their replies.

Used when no provider API key is reachable. Each panel member is a separate
agent session running a different model. A session receives a batch of cases;
every case block inside the batch is exactly the prompt the API path would send.

    python -m harness.panel export --condition A --batch-size 5
    python -m harness.panel import --condition A --member opus=claude-opus-5-5 ...

Replies are saved by the operator as results/panel/replies/<condition>/<alias>_batch<k>.txt
(the subagent's raw text). `import` parses them into results/raw_responses.jsonl
using the same record schema as the API path, with mode="subagent_panel".
"""
import argparse
import json
from datetime import date
from pathlib import Path

from .config import CONDITIONS, RESULTS, WORK
from .parse import ParseError, normalize
from .prompts import case_prompt, make_batches, panel_batch_prompt, prompt_hash

PANEL = RESULTS / "panel"


def panel_dir(set_name: str):
    """'main' uses results/panel/; any other set (e.g. 'supp') gets results/panel/<set>/."""
    return PANEL if set_name == "main" else PANEL / set_name


def export(condition, batch_size, cases_path, set_name="main", ids=None):
    cases = [c for c in json.load(open(cases_path)) if not ids or c["id"] in ids]
    batches = make_batches([{"id": c["id"], "facts": c["facts"], "seam": c["seam"]} for c in cases], batch_size)
    base = panel_dir(set_name)
    d = base / "prompts"
    d.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for k, b in enumerate(batches, 1):
        (d / f"{condition}_batch{k}.txt").write_text(panel_batch_prompt(b, condition))
        manifest[f"batch{k}"] = [c["id"] for c in b]
    (base / "batches.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest))


def _array(text):
    """Extract the JSON array a panel member returned."""
    # Drop the trailing self-report line ("MODEL_ID: ...") before locating the array.
    t = "\n".join(l for l in text.strip().splitlines() if not l.strip().startswith("MODEL_ID:"))
    s, e = t.find("["), t.rfind("]")
    return json.loads(t[s : e + 1])


def import_replies(condition, members, cases_path, out_path, set_name="main"):
    cases = {c["id"]: c for c in json.load(open(cases_path))}
    base = panel_dir(set_name)
    manifest = json.loads((base / "batches.json").read_text())
    rdir = base / "replies" / condition
    run_date = date.today().isoformat()
    n = 0
    with open(out_path, "a") as out:
        for alias, model_id in members.items():
            for batch, ids in manifest.items():
                path = rdir / f"{alias}_{batch}.txt"
                if not path.exists():          # batch not run under this condition (e.g. Condition B only for selected cases)
                    continue
                text = path.read_text()
                try:
                    items = {str(o.get("id")): o for o in _array(text)}
                except (ValueError, json.JSONDecodeError):
                    items = {}
                rerq = rdir / f"{alias}_{batch}.rerequest.txt"     # present only if a format-only re-request was sent
                rer_items = {}
                if rerq.exists():
                    try:
                        rer_items = {str(o.get("id")): o for o in _array(rerq.read_text())}
                    except (ValueError, json.JSONDecodeError):
                        pass
                for cid in ids:
                    rec = {"attempt_text": json.dumps(items.get(cid)) if cid in items else None,
                           "format_rerequest": cid not in items and rerq.exists(), "rerequest_text": None,
                           "transport_retries": 0, "notes": []}
                    try:
                        rec["parsed"], rec["parse_status"] = normalize(items[cid]), "ok"
                    except (KeyError, ParseError):
                        try:
                            rec["parsed"], rec["parse_status"] = normalize(rer_items[cid]), "ok_after_rerequest"
                            rec["rerequest_text"] = json.dumps(rer_items[cid])
                        except (KeyError, ParseError):
                            rec["parsed"], rec["parse_status"] = None, "unparseable"
                    prompt = case_prompt(cases[cid]["facts"], condition)
                    rec.update(run_date=run_date, mode="subagent_panel", condition=condition, provider="anthropic",
                               model_id=model_id, panel_alias=alias, batch=f"{set_name}:{batch}", case_id=cid, prompt_sha=prompt_hash(prompt))
                    out.write(json.dumps(rec) + "\n")
                    n += 1
    print(f"imported {n} records")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("--condition", choices=CONDITIONS, required=True)
    e.add_argument("--batch-size", type=int, default=5)
    e.add_argument("--cases", default=str(WORK / "candidates.json"))
    e.add_argument("--set", default="main", help="prompt set name; non-main sets go to results/panel/<set>/")
    e.add_argument("--ids", nargs="*", help="export only these case ids")
    i = sub.add_parser("import")
    i.add_argument("--condition", choices=CONDITIONS, required=True)
    i.add_argument("--member", nargs="+", required=True, help="alias=model_id, e.g. opus=claude-opus-5-5")
    i.add_argument("--cases", default=str(WORK / "candidates.json"))
    i.add_argument("--out", default=str(RESULTS / "raw_responses.jsonl"))
    i.add_argument("--set", default="main")
    a = ap.parse_args(argv)
    if a.cmd == "export":
        export(a.condition, a.batch_size, a.cases, a.set, set(a.ids or []))
    else:
        import_replies(a.condition, dict(m.split("=", 1) for m in a.member), a.cases, a.out, a.set)


if __name__ == "__main__":
    main()
