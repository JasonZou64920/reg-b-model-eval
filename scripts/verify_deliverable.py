"""Phase 8 checks on the final deliverable.

1. Page count and orientation of the PDF.
2. Every citation string in the deliverable text exists in sources/ (via harness.sources).
3. Every final case is marked as missed by at least one model in Condition A in results/scores.csv.
4. No em dashes in the deliverable.
"""
import csv, json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from harness.sources import check_citation  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
pdf = ROOT / "deliverable/Zou_CTGT_Work_Sample_RulesTrack.pdf"
ok = True

info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
w, h = map(float, re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", info).groups())
print(f"[pages] {pages} page(s), {'portrait' if h > w else 'landscape'} {w:.0f}x{h:.0f} pt")
ok &= pages <= 2 and h > w

text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
# Citations are read from the .docx (no line wrapping); the PDF text is used for page and dash checks.
from docx import Document  # noqa: E402
d = Document(ROOT / "deliverable/Zou_CTGT_Work_Sample_RulesTrack.docx")
parts = [p.text for p in d.paragraphs] + [c.text for t in d.tables for row in t.rows for c in row.cells]
flat = re.sub(r"\s+", " ", " ".join(parts).replace("\u2060", ""))   # drop word joiners used for line breaking
# Pull every parenthesized or inline citation from the rendered text, including the method note.
cites = set(re.findall(r"(?:(?:12 CFR )?1002\.\d+(?:\([a-zA-Z0-9]+\))*|[Cc]omments? \d+(?:\([a-z0-9]+\))*-\d+(?: and \d+(?:\([a-z0-9]+\))*-\d+)?|appendix C, para\. \d|Form C-\d+)", flat))
bad = []
for c in sorted(cites):
    r = check_citation(c if c.startswith(("12 CFR", "comment", "Comment", "appendix", "Form")) else "12 CFR " + c)
    if r["missing"] or r["empty"] or r["withdrawn"]:
        bad.append((c, r))
print(f"[citations] {len(cites)} distinct citation strings found; {len(bad)} not in sources/")
for c in sorted(cites):
    print("   ", c)
for c, r in bad:
    print("   MISSING:", c, r["missing"])
ok &= not bad

final = json.load(open(ROOT / "work/final_cases.json"))
rows = {r["case_id"]: r for r in csv.DictReader(open(ROOT / "results/scores.csv"))}
for c in final:
    r = rows[c["id"]]
    flag = r["hard_A"] == "True" and int(r["misses_A"]) >= 1
    print(f"[hard] case {c['n']:>2} {c['id']}: misses_A={r['misses_A']} A2={r.get('misses_A2') or '-'} C={r.get('misses_C') or '-'} {'OK' if flag else 'NOT HARD'}")
    ok &= flag

dashes = text.count("—") + text.count("–")
print(f"[dashes] em/en dashes in rendered text: {dashes}")
ok &= dashes == 0

print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
