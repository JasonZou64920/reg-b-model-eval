"""Shared constants for the Regulation B hardness harness.

Everything that affects what a model sees lives here, so a reader can check
in one place that every model got the same instructions.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # repo root (ctgt/)
SOURCES = ROOT / "sources"
WORK = ROOT / "work"
RESULTS = ROOT / "results"

# The fixed task prompt, verbatim from the work-sample spec.
FIXED_PROMPT = (
    "Label this case under 12 CFR 1002.9(b)(2) as complies, violates, or depends. "
    "If depends, name the deciding fact. Give one sentence of reasoning citing the specific provision."
)

# Output contract appended to every prompt. The harness parses this JSON.
JSON_INSTRUCTION = (
    "Respond with only a JSON object with exactly these keys: "
    '"label" (one of "complies", "violates", "depends"), '
    '"reasoning" (one sentence), '
    '"citation" (the provision or provisions you rely on), '
    '"deciding_fact" (a string if label is "depends", otherwise null).'
)

# Sent once, and only when the first reply cannot be parsed. It asks for the
# format again and adds no content, so it is not a second attempt at the answer.
FORMAT_ONLY_REREQUEST = (
    "Your previous reply could not be parsed. Return the same answer as a single JSON object "
    'with the keys "label", "reasoning", "citation", "deciding_fact" and nothing else.'
)

LABELS = ("complies", "violates", "depends")

# Condition A: rule text only (defines "hard"). Condition B: rule text plus the
# official commentary to 9(b)(2). Condition C (added after the audit): rule text plus
# every provision and comment in sources/, so a miss cannot come from missing authority.
CONDITIONS = ("A", "A2", "B", "C")
# "A2" is a replication draw: the identical Condition A prompt, run again later on the
# selected cases, so their miss counts are not judged only on the draw used to select them.

# Transport retry policy (429 and 5xx only). These retries never count as attempts.
MAX_TRANSPORT_RETRIES = 8
BACKOFF_BASE_SECONDS = 2.0
BACKOFF_CAP_SECONDS = 60.0

MAX_OUTPUT_TOKENS = 1024
REQUEST_TIMEOUT_SECONDS = 120
