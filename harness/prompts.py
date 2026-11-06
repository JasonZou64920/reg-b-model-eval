"""Build the exact text each model sees.

API mode sends one case per request. The fallback panel (subagents, used when
no API key is available) receives several of these same per-case blocks in one
session, so both modes are built from `case_prompt` and differ only in framing.
"""
import hashlib
import random

from .config import FIXED_PROMPT, JSON_INSTRUCTION
from .sources import commentary_9b2, full_rulebook, rule_text_9b2


def case_prompt(facts: str, condition: str) -> str:
    """The single-case prompt. A: rule text only. B: plus the 9(b)(2) commentary. C: plus the full rulebook."""
    parts = [
        FIXED_PROMPT,
        "",
        "Rule text, 12 CFR 1002.9(b)(2), verbatim:",
        rule_text_9b2(),
    ]
    if condition == "B":
        parts += [
            "",
            "Official interpretations of 12 CFR 1002.9(b)(2) (Supplement I to Part 1002, comments 9(b)(2)-1 to 9(b)(2)-9), verbatim:",
            commentary_9b2(),
        ]
    elif condition == "C":
        parts += [
            "",
            "Reference material: the full text of the provisions and official interpretations a reviewer would use, verbatim.",
            full_rulebook(),
        ]
    elif condition not in ("A", "A2"):
        raise ValueError(f"unknown condition {condition!r}")
    parts += ["", "Case:", facts, "", JSON_INSTRUCTION]
    return "\n".join(parts)


def prompt_hash(text: str) -> str:
    """Short content hash recorded with every response, so runs can be compared."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def make_batches(cases: list, size: int, seed: int = 20261031) -> list:
    """Split cases into batches for the subagent panel.

    Cases are shuffled with a fixed seed, then dealt so that no batch holds two
    cases from the same seam where avoidable. Related cases side by side would
    let a model reason by contrast, which a one-case-per-call API run cannot do.
    """
    rng = random.Random(seed)
    pool = cases[:]
    rng.shuffle(pool)
    n_batches = -(-len(pool) // size)
    batches = [[] for _ in range(n_batches)]
    for case in sorted(pool, key=lambda c: c["seam"]):      # group by seam, then deal round-robin
        order = sorted(range(n_batches), key=lambda b: (sum(c["seam"] == case["seam"] for c in batches[b]), len(batches[b])))
        for b in order:
            if len(batches[b]) < size:
                batches[b].append(case)
                break
    for b in batches:
        rng.shuffle(b)
    return batches


def panel_batch_prompt(batch: list, condition: str) -> str:
    """Framing for one subagent session. Each case block is the unmodified API prompt."""
    head = (
        "You are one member of a model panel being tested on Regulation B cases. "
        "Do not use any tools, files or web access. Answer from the text below only. "
        "Treat each case as a separate, independent request: do not compare cases or let one answer influence another. "
        "Give your first answer for each; do not revise.\n\n"
        "Return a JSON array, one object per case, each with keys \"id\", \"label\", \"reasoning\", \"citation\", \"deciding_fact\", "
        "in the order the cases appear. Return only the JSON array, then one final line of the form "
        "\"MODEL_ID: <your exact model identifier as stated in your system prompt>\".\n"
    )
    blocks = [f"\n===== REQUEST id={c['id']} =====\n{case_prompt(c['facts'], condition)}" for c in batch]
    return head + "".join(blocks)
