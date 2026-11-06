"""Extract the regulation body from a saved CFPB interactive-regulation page to plain text.

Usage: python3 -I extract_cfpb.py <page.html> <out.txt>
Keeps paragraph structure: one block per <p>, heading, or list item.
"""
import re, sys, html as H

src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding="utf-8").read()
start = h.find('id="content__main"')
h = h[start:]
# Cut off everything after the regulation body (footer / wayfinder for next section).
for marker in ('<footer', 'Regulation inquiries'):
    k = h.find(marker)
    if k > 0:
        h = h[:k]
        break
h = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
h = re.sub(r"<(p|h\d|li|dt|dd|div)[^>]*>", "\n\n", h)
h = re.sub(r"<br\s*/?>", "\n", h)
h = re.sub(r"<[^>]+>", "", h)
h = H.unescape(h)
lines = [re.sub(r"[ \t\r\f\v]+", " ", l).strip() for l in h.split("\n")]
text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
open(out, "w").write(text + "\n")
print(out, len(text))
