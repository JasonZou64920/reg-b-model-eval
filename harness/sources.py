"""Load verbatim Regulation B text from sources/ and check citation strings against it.

Two jobs:
1. Supply the exact text that goes into prompts (the 9(b)(2) paragraph for
   Condition A, plus the 9(b)(2) commentary for Condition B).
2. Build an index of every provision designation present in sources/ so that
   any citation string (ours or a model's) can be checked mechanically.
"""
import re
from functools import lru_cache

from .config import SOURCES


def _body(name: str) -> str:
    """Return a source file without its '#' header lines."""
    text = (SOURCES / name).read_text(encoding="utf-8")
    return "\n".join(l for l in text.splitlines() if not l.startswith("# ")).strip()


@lru_cache(maxsize=None)
def rule_text_9b2() -> str:
    """Verbatim text of 12 CFR 1002.9(b)(2)."""
    body = _body("12_CFR_1002.9.txt")
    m = re.search(r"\(2\) Statement of specific reasons\..*?(?=\n\n\(c\) )", body, re.S)
    if not m:
        raise RuntimeError("Could not locate 1002.9(b)(2) in sources")
    return m.group(0).strip()


@lru_cache(maxsize=None)
def commentary_9b2() -> str:
    """Verbatim text of comments 9(b)(2)-1 through 9(b)(2)-9."""
    body = _body("SuppI_comments_9.txt")
    m = re.search(r"Paragraph 9\(b\)\(2\)\.\n(.*?)(?=\n9\(c\) )", body, re.S)
    if not m:
        raise RuntimeError("Could not locate 9(b)(2) commentary in sources")
    return m.group(1).strip()


@lru_cache(maxsize=None)
def full_rulebook() -> str:
    """Every source file used for gold labels: 1002.9, 1002.2(c), Supplement I comments to 9 and 2(c), Appendix C."""
    parts = [
        ("12 CFR 1002.9, verbatim", "12_CFR_1002.9.txt"),
        ("12 CFR 1002.2(c), verbatim", "12_CFR_1002.2c.txt"),
        ("Supplement I to Part 1002, official interpretations of 1002.9, verbatim", "SuppI_comments_9.txt"),
        ("Supplement I to Part 1002, official interpretations of 1002.2(c), verbatim", "SuppI_comments_2c.txt"),
        ("Appendix C to Part 1002 (instructions and sample forms), verbatim", "Appendix_C.txt"),
    ]
    return "\n\n".join(f"{title}:\n{_body(name)}" for title, name in parts)


# ---------------------------------------------------------------------------
# Provision index
# ---------------------------------------------------------------------------
_ROMAN = {"i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"}


def _reg_designations(section: str, body: str) -> set:
    """Walk CFR paragraph markers like '(b) ...—(2) ...' and return full designations.

    CFR nesting is (a) -> (1) -> (i) -> (A). Roman numerals are ambiguous with
    letters, so a roman token is treated as level 3 when we are already at level 2+.
    """
    found, stack = set(), []
    for line in body.splitlines():
        line = line.strip()
        # Markers at the start of a paragraph, possibly chained after a heading dash.
        # A marker opens the paragraph, or follows a heading ending in '—' or '. '.
        for tok in re.findall(r"(?:^|—|\. )\((\w{1,4})\)(?= [A-Z0-9$])", line):
            if tok.isdigit():
                level = 2
            elif tok.isupper():
                level = 4
            elif tok in _ROMAN and len(stack) >= 2:
                level = 3
            else:
                level = 1
            stack = stack[: level - 1] + [tok]
            found.add(section + "".join(f"({t})" for t in stack))
    return found


def _comment_designations(body: str, general_prefix: str) -> set:
    """Turn commentary headings plus numbered paragraphs into 'comment X-n' strings."""
    found, current = set(), general_prefix
    for line in body.splitlines():
        line = line.strip()
        para = re.match(r"^Paragraph (\d+(?:\([a-z0-9]+\))+)\.$", line)   # 'Paragraph 9(b)(2).'
        head = re.match(r"^(\d+\([a-z]\)) [A-Z]", line)                  # '9(g) Applications ...'
        if para:
            current = para.group(1)
        elif head:
            current = head.group(1)
        num = re.match(r"^(\d+)\. ", line)                               # '7. Combined credit ...'
        if num:
            found.add(f"comment {current}-{num.group(1)}")
    return found


@lru_cache(maxsize=None)
def provision_index() -> frozenset:
    """Every citable designation present in sources/."""
    idx = set()
    idx.add("12 CFR 1002.9")                      # the whole section is in sources/
    idx |= _reg_designations("12 CFR 1002.9", _body("12_CFR_1002.9.txt"))
    idx |= _reg_designations("12 CFR 1002.2", _body("12_CFR_1002.2c.txt"))
    idx |= _comment_designations(_body("SuppI_comments_9.txt"), "9")
    idx |= _comment_designations(_body("SuppI_comments_2c.txt"), "2(c)")
    app = _body("Appendix_C.txt")
    for n in re.findall(r"^(\d)\. ", app, re.M):
        idx.add(f"appendix C, para. {n}")
    for f in re.findall(r"^Form (C-\d+) ", app, re.M):
        idx.add(f"Form {f}")
    return frozenset(idx)


# ---------------------------------------------------------------------------
# Citation parsing
# ---------------------------------------------------------------------------
_WITHDRAWN = re.compile(r"Circular\s+20(22-03|23-03)", re.I)


def parse_citations(cite: str) -> list:
    """Split a citation string into normalized designations.

    Handles shorthand such as 'comments 9(b)(2)-2, 9(b)(2)-5' and
    '§ 1002.9(b)(2)'. Returns a list of strings in index format.
    """
    if not cite:
        return []
    s = cite.replace("§", " ").replace("Sec.", " ")
    s = re.sub(r"\s+", " ", s)
    out = []
    # Regulation text: 1002.9(a)(2)(ii) etc. ("12 CFR" optional).
    for m in re.finditer(r"(?:12 C\.?F\.?R\.? (?:§ )?)?1002\.(\d+)((?:\([a-zA-Z0-9]{1,4}\))*)", s):
        out.append(f"12 CFR 1002.{m.group(1)}{m.group(2)}")
    # Comments: 'comment 9(b)(2)-7' and lists after 'comments'.
    for m in re.finditer(r"comments? ((?:\d+(?:\([a-z0-9]{1,4}\))*-\d+(?:, (?:and )?|,? and )?)+)", s, re.I):
        for d in re.findall(r"(\d+(?:\([a-z0-9]{1,4}\))*-\d+)", m.group(1)):
            out.append(f"comment {d}")
    # Appendix C paragraphs and forms.
    for m in re.finditer(r"appendix C,? (?:para\.?|paragraph) (\d)", s, re.I):
        out.append(f"appendix C, para. {m.group(1)}")
    for m in re.finditer(r"Form (C-\d+)", s):
        out.append(f"Form {m.group(1)}")
    return out


def check_citation(cite: str) -> dict:
    """Return {'parsed': [...], 'missing': [...], 'withdrawn': bool, 'empty': bool}."""
    parsed = parse_citations(cite or "")
    idx = provision_index()
    missing = [p for p in parsed if p not in idx]
    return {
        "parsed": parsed,
        "missing": missing,
        "withdrawn": bool(_WITHDRAWN.search(cite or "")),
        "empty": not parsed,
    }
