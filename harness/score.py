"""Score raw responses against gold labels and write scores.csv and summary.md.

    python -m harness.score --template   # add ungraded deciding-fact rows to the grades file
    python -m harness.score              # write results/scores.csv, scores_long.csv, summary.md

Outcome codes for each case x model x condition:
    hit         label matches gold (and, for gold 'depends', the deciding fact matches)
    miss_label  wrong label
    miss_fact   gold and model both say 'depends' but the model names a different deciding fact
    miss_parse  no parseable answer after one format-only re-request (or transport failure)

Deciding-fact matches are graded in results/deciding_fact_grades.csv (one row per
depends/depends pair). A match means the model's fact is the same decisive unknown
as the gold fact, whatever the wording. Citation problems (a cited provision that is
not in sources/, a withdrawn circular, or no parseable citation) are logged separately
and do not change the outcome.
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from .config import RESULTS, WORK
from .sources import check_citation

GRADES = RESULTS / "deciding_fact_grades.csv"
GRADE_FIELDS = ["condition", "model_id", "case_id", "model_deciding_fact", "gold_deciding_fact", "match", "grader_note"]


def load_raw(path):
    recs = [json.loads(l) for l in open(path) if l.strip()]
    # If a case was re-run, the latest record for (condition, model, case) wins.
    latest = {}
    for r in recs:
        latest[(r["condition"], r["model_id"], r["case_id"])] = r
    return latest


def load_grades():
    if not GRADES.exists():
        return {}
    with open(GRADES) as f:
        return {(r["condition"], r["model_id"], r["case_id"]): r for r in csv.DictReader(f)}


def write_template(raw, gold):
    grades = load_grades()
    for (cond, model, cid), r in raw.items():
        p = r.get("parsed") or {}
        if gold[cid]["gold_label"] == "depends" and p.get("label") == "depends" and (cond, model, cid) not in grades:
            grades[(cond, model, cid)] = {"condition": cond, "model_id": model, "case_id": cid,
                                          "model_deciding_fact": p.get("deciding_fact") or "",
                                          "gold_deciding_fact": gold[cid]["deciding_fact"], "match": "", "grader_note": ""}
    with open(GRADES, "w", newline="") as f:
        w = csv.DictWriter(f, GRADE_FIELDS)
        w.writeheader()
        for k in sorted(grades):
            w.writerow(grades[k])
    print(f"{GRADES}: {sum(1 for g in grades.values() if not g['match'])} rows need grading")


def outcome(r, g, grades):
    p = r.get("parsed")
    if not p:
        return "miss_parse"
    if p["label"] != g["gold_label"]:
        return "miss_label"
    if g["gold_label"] == "depends":
        grade = grades.get((r["condition"], r["model_id"], r["case_id"]), {}).get("match", "")
        if grade not in ("yes", "no"):
            raise SystemExit(f"ungraded deciding fact: {r['condition']} {r['model_id']} {r['case_id']} (run --template)")
        return "hit" if grade == "yes" else "miss_fact"
    return "hit"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", default=str(RESULTS / "raw_responses.jsonl"))
    ap.add_argument("--gold", default=str(WORK / "candidates.json"))
    ap.add_argument("--template", action="store_true")
    a = ap.parse_args(argv)

    gold = {c["id"]: c for c in json.load(open(a.gold))}
    raw = load_raw(a.raw)
    if a.template:
        return write_template(raw, gold)
    grades = load_grades()

    models = defaultdict(set)                      # condition -> model ids
    for cond, model, _ in raw:
        models[cond].add(model)
    cols = [(c, m) for c in sorted(models) for m in sorted(models[c])]

    long_rows, table = [], defaultdict(dict)
    for (cond, model, cid), r in sorted(raw.items()):
        g = gold[cid]
        o = outcome(r, g, grades)
        p = r.get("parsed") or {}
        cc = check_citation(p.get("citation", ""))
        cite_flag = ";".join(filter(None, [
            "missing:" + "|".join(cc["missing"]) if cc["missing"] else "",
            "withdrawn" if cc["withdrawn"] else "",
            "none" if cc["empty"] and p else "",
        ]))
        table[cid][(cond, model)] = o
        long_rows.append({"condition": cond, "model_id": model, "case_id": cid, "seam": g["seam"],
                          "gold_label": g["gold_label"], "model_label": p.get("label", ""), "outcome": o,
                          "parse_status": r.get("parse_status"), "citation": p.get("citation", ""),
                          "citation_flag": cite_flag, "model_deciding_fact": p.get("deciding_fact") or "",
                          "reasoning": p.get("reasoning", "")})

    with open(RESULTS / "scores_long.csv", "w", newline="") as f:
        w = csv.DictWriter(f, list(long_rows[0]))
        w.writeheader()
        w.writerows(long_rows)

    # Wide case x model table.
    with open(RESULTS / "scores.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "seam", "gold_label"] + [f"{c}:{m}" for c, m in cols]
                   + [f"misses_{c}" for c in sorted(models)] + ["hard_A", "missed_by_all_A"])
        for cid in sorted(table):
            row = table[cid]
            # A condition the case was not run under gets a blank, not a zero.
            misses = {c: (sum(1 for m in models[c] if row[(c, m)] != "hit")
                          if any((c, m) in row for m in models[c]) else "") for c in sorted(models)}
            nA = len(models.get("A", []))
            mA = misses.get("A") or 0
            w.writerow([cid, gold[cid]["seam"], gold[cid]["gold_label"]] + [row.get(k, "") for k in cols]
                       + [misses[c] for c in sorted(models)]
                       + [mA >= 1, nA > 0 and mA == nA])

    write_summary(raw, gold, table, models, cols, long_rows)


def write_summary(raw, gold, table, models, cols, long_rows):
    any_rec = next(iter(raw.values()))
    lines = ["# Hardness test results", "",
             f"Run date: {any_rec['run_date']}. Mode: {any_rec['mode']}.", "",
             "## Panel", ""]
    aliases = {}
    for r in raw.values():
        aliases[r["model_id"]] = r.get("panel_alias", r.get("provider"))
    for m in sorted(aliases):
        lines.append(f"- `{m}` ({aliases[m]})")
    lines += ["", "## Accuracy by model and condition", "", "| Condition | Model | Correct | Label misses | Fact misses | Parse misses |", "|---|---|---|---|---|---|"]
    for c, m in cols:
        os_ = [table[cid].get((c, m)) for cid in table if (c, m) in table[cid]]
        lines.append(f"| {c} | `{m}` | {os_.count('hit')}/{len(os_)} | {os_.count('miss_label')} | {os_.count('miss_fact')} | {os_.count('miss_parse')} |")
    for c in sorted(models):
        n = len(models[c])
        run = [cid for cid in sorted(table) if any((c, m) in table[cid] for m in models[c])]   # cases run under c
        nm = {cid: sum(table[cid].get((c, m)) != "hit" for m in models[c]) for cid in run}
        hard = [cid for cid in run if nm[cid] >= 1]
        allm = [cid for cid in run if nm[cid] == n]
        two = [cid for cid in run if nm[cid] >= 2]
        lines += ["", f"## Condition {c}", "",
                  f"- Missed by at least one model: {len(hard)} of {len(run)} ({', '.join(hard)})",
                  f"- Missed by two or more: {len(two)} ({', '.join(two)})",
                  f"- Missed by every model: {len(allm)} ({', '.join(allm)})"]
    cite = [r for r in long_rows if r["citation_flag"]]
    lines += ["", "## Citation flags (logged separately, not scored)", ""]
    lines += [f"- {r['condition']} `{r['model_id']}` {r['case_id']}: {r['citation_flag']} (cited: {r['citation']})" for r in cite] or ["- none"]
    parse = [r for r in long_rows if r["parse_status"] not in ("ok",)]
    lines += ["", "## Parse status other than first-try ok", ""]
    lines += [f"- {r['condition']} `{r['model_id']}` {r['case_id']}: {r['parse_status']}" for r in parse] or ["- none"]
    notes = RESULTS / "summary_notes.md"
    if notes.exists():
        lines += ["", notes.read_text().strip()]
    (RESULTS / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:40]))


if __name__ == "__main__":
    main()
