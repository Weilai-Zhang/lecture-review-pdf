#!/usr/bin/env python3
"""Review-pack QA. Usage: python3 qa.py --pdf OUT.pdf --src . [--ledger ledger.json] [--preview qa-preview]
Exit 1 if any FAIL; WARN lines are advisory."""
import argparse, json, re, subprocess, sys, pathlib
ap = argparse.ArgumentParser()
ap.add_argument("--pdf", required=True); ap.add_argument("--src", default=".")
ap.add_argument("--ledger"); ap.add_argument("--preview")
a = ap.parse_args()
hard, warn = [], []
CJK = re.compile(r"[一-鿿]"); LAT = re.compile(r"[A-Za-z]+")

if a.ledger:  # 1. coverage + answer cross-check
    L = json.load(open(a.ledger, encoding="utf-8")); kps = L.get("kps", {})
    for rng, ids in L.get("slides", {}).items():
        if not ids: hard.append(f"coverage: slides {rng} have no KPs")
    drilled = set()
    for qid, q in L.get("tutorial", {}).items():
        if not q.get("kps"): hard.append(f"coverage: {qid} has no KPs")
        if not q.get("recap", False): hard.append(f"coverage: {qid} has no recap entry")
        drilled |= set(q.get("kps", []))
        off, ours = q.get("official"), q.get("ours")
        if off is not None and ours is not None and not q.get("diff_explained"):
            try:
                o, u = float(off), float(ours)
                tol = max(abs(o) * 0.005, 10 ** -(len(str(off).split(".")[-1]) if "." in str(off) else 0) / 2)
                if abs(o - u) > tol: hard.append(f"answer: {qid} ours={ours} official={off}")
            except ValueError:
                if str(off).strip() != str(ours).strip(): hard.append(f"answer: {qid} ours='{ours}' official='{off}'")
    for pid, v in L.get("practice", {}).items():
        drilled |= set(v if isinstance(v, list) else v.get("kps", []))
    for k, v in kps.items():
        if v.get("must_know") and k not in drilled: hard.append(f"coverage: must-know {k} never drilled")

def strip(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S); t = re.sub(r"\$[^$]*\$", " ", t)
    return re.sub(r"#[a-zA-Z_.]+(\([^)]*\))?", " ", t)
for f in sorted(pathlib.Path(a.src).glob("*.typ")):  # 2. Chinese density
    if f.name in ("theme.typ", "main.typ"): continue
    text = f.read_text(encoding="utf-8")
    for sec in re.split(r"\n(?==+ )", text):
        head = sec.strip().splitlines()[0][:50] if sec.strip() else ""
        s = strip(sec); c, w = len(CJK.findall(s)), len(LAT.findall(s))
        if w > 30 and c < 1.5 * w: warn.append(f"density: {f.name} «{head}» CJK={c} Latin={w}")
    for m in re.finditer(r"\[(思路|易错[点]?|本题意图)[^\]]*\]\s*\[", text):
        start, depth, i = m.end(), 1, m.end()
        while i < len(text) and depth:
            depth += {"[": 1, "]": -1}.get(text[i], 0); i += 1
        n = len(CJK.findall(strip(text[start:i])))
        if n < 40: hard.append(f"density: {f.name} «{m.group(1)}» callout only {n} CJK chars")

txt = subprocess.run(["pdftotext", "-layout", a.pdf, "-"], capture_output=True, text=True).stdout
for p in ["see slide", "See slide", "见幻灯片", "同理可得", "TODO", "??", "（略）", "(略)"]:  # 3. forbidden
    if p in txt: hard.append(f"forbidden: '{p}' in PDF")
for line in subprocess.run(["pdffonts", a.pdf], capture_output=True, text=True).stdout.splitlines()[2:]:  # 4. fonts
    cols = line.split()
    if " 3 " in line and "Type" in line: hard.append(f"fonts: Type 3 font: {cols[0]}")
    if len(cols) >= 5 and cols[-5] == "no": hard.append(f"fonts: not embedded: {cols[0]}")
from pypdf import PdfReader
r = PdfReader(a.pdf); pages = len(r.pages)
if not r.outline: hard.append("structure: no PDF outline/bookmarks")
if "�" in txt or "□" in txt: warn.append("glyphs: replacement/tofu characters in text")
if a.preview:  # 5. previews for visual check
    pathlib.Path(a.preview).mkdir(exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "60", "-png", a.pdf, f"{a.preview}/p"])
print(f"pages={pages}")
for x in warn: print("WARN ", x)
for x in hard: print("FAIL ", x)
print("QA PASS" if not hard else f"QA FAIL ({len(hard)})"); sys.exit(1 if hard else 0)
