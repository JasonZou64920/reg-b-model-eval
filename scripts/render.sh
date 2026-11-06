#!/usr/bin/env bash
# Build the deliverable: the PDF is rendered from a copy with line-break guards in citations;
# the delivered .docx is built without them so Find and copy-paste work on plain text.
set -euo pipefail
cd "$(dirname "$0")/.."
TMP=$(mktemp -d)
python scripts/build_docx.py --for-pdf --out "$TMP/Zou_CTGT_Work_Sample_RulesTrack.docx"
soffice --headless --convert-to pdf --outdir "$TMP" "$TMP/Zou_CTGT_Work_Sample_RulesTrack.docx" >/dev/null 2>&1
cp "$TMP/Zou_CTGT_Work_Sample_RulesTrack.pdf" deliverable/
python scripts/build_docx.py --out deliverable/Zou_CTGT_Work_Sample_RulesTrack.docx
rm -rf "$TMP"
