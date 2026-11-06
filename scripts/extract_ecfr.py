"""Extract verbatim text of Reg B provisions from the eCFR Part 1002 XML into plain-text files."""
import sys, re, html
import xml.etree.ElementTree as ET

src, outdir = sys.argv[1], sys.argv[2]
tree = ET.parse(src)
root = tree.getroot()

def text_of(el):
    # Flatten element to text, one paragraph per P / HD / HED element.
    lines = []
    for node in el.iter():
        if node.tag in ("HEAD", "HD", "HED", "P", "FP", "PSPACE", "TDESC"):
            t = "".join(node.itertext())
            t = re.sub(r"\s+", " ", t).strip()
            if t:
                lines.append(t)
    return "\n\n".join(lines)

found = {}
for div in root.iter():
    if div.tag.startswith("DIV") and div.get("N"):
        n = div.get("N")
        head = div.find("HEAD")
        h = "".join(head.itertext()).strip() if head is not None else ""
        if n in ("1002.2", "1002.9") or h.startswith("Appendix C to Part 1002") or h.startswith("Supplement I to Part 1002"):
            found[h or n] = div

for h, div in found.items():
    print(h[:90], div.tag, div.get("N"))

def save(name, el):
    open(f"{outdir}/{name}", "w").write(text_of(el))

for h, div in found.items():
    if div.get("N") == "1002.2": save("ecfr_1002_2.txt", div)
    elif div.get("N") == "1002.9": save("ecfr_1002_9.txt", div)
    elif h.startswith("Appendix C"): save("ecfr_appendix_c.txt", div)
    elif h.startswith("Supplement I"): save("ecfr_supplement_I_full.txt", div)
