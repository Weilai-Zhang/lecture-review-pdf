---
name: "lecture-review-pdf"
description: "Turn university lecture slides, workshop sheets, tutorial questions (plus official solutions) and past exams into a Chinese-rich bilingual 中英 review PDF with full worked solutions. Use for 复习包, 复习资料, 做 Topic N, Week N 的复习, 考前速查, 期末总复习, or updating a pack when official solutions are released."
---

# University Lecture Review PDF

Turn lecture / workshop / tutorial / past-exam files into a bilingual (中英) review PDF that a Chinese-speaking student can actually learn from. Default setting: English-taught Australian / international university. Talk to the user in Chinese.

## The standard (single source of truth — everything below refers back here)

**Language.** Exam terms, definitions, theorem statements, formula labels and markable final answers stay in **English**. **Chinese carries the teaching**: intuition, clause-by-clause meaning, when/why to use something, common mistakes, 思路, and the "why this step" on every calculation. Never translate code identifiers, R/Excel function names, paper titles, proper nouns or Greek letters; define every symbol in Chinese on first use. Use established Chinese terminology, and keep lecturer phrasing that looks like exam wording.

**What "Chinese-rich" means** (applies to notes, tutorial recap and practice solutions alike):
- After every English definition / theorem / boxed formula: 2–4+ complete Chinese sentences — assumptions, what it does *not* claim, when to reach for it.
- No knowledge point whose only Chinese is a short label; no English-primary pack with decorative Chinese.
- Every 思路 is a real Chinese paragraph (typically 4–8 sentences); every numbered solution step has ≥1 Chinese sentence explaining *why*; every question ends with 本题意图 and 易错点.
- The explanation always contains more Chinese teaching than the official solution sheet does.
- The test is *teaching value, not character count*: a Chinese-speaking student should be able to learn from the Chinese prose alone, with English terms as anchors. Don't pad — repetition and filler are failures too.

**Completeness over page count.** Every taught idea, worked example and tutorial part is covered; typical honest length is 22–40+ pages per lecture week in Full mode. Never write "see slide", "略" or "同理可得" in place of working.

**Numbers are computed, not remembered.** Recompute every numerical answer in Python (numpy/scipy) before writing it. Official solutions are ground truth for the number and intended method; if yours differs after rechecking, show both and explain in Chinese.

## 0. Preflight (always, before reading any lecture)

1. **Environment.** `pip install --break-system-packages typst` (not preinstalled), then `python3 -c "import typst"`; `fc-list | grep -E "Pagella|Noto (Serif|Sans) CJK SC|New Computer Modern Math"`. If Typst can't install, switch to the fallback in §6 now, not halfway through.
2. **Locate files.** If the user attached files, use them. If they just say "做 Topic 10" and the session is linked to their computer, `device_list_dir` the course folder (non-recursive first; skip `.build/`, `output/`, `.workbuddy/`). Files named `*_Review_CN-EN*.pdf` or `*Bilingual*.pdf` are previous outputs, never sources. Stage only what this pack needs with `device_stage_files` (files land under `/mnt/user-data/uploads/<folder>/`); always include the tutorial solutions file if it exists. If a matching file is missing (e.g. `T10_Sol` not released yet), proceed without it and say so on the cover and in the final message — don't stop to ask. Ask only if *which* topic/week is genuinely ambiguous (e.g. "做下一周的" with no clear reference).
3. **Load the course kit** from `<course folder>/.build/review-kit/` and read everything in it before planning:
   - `course.md` — this course's profile (§1). Follow it over the generic defaults here.
   - `lessons.md` — accumulated feedback from earlier packs. **Every rule in it is binding.** Re-read it before writing notes and again before QA.
   - `exemplars/` — pages/sections the user approved. Match their depth, tone and layout.
   - `theme.typ`, `qa.py` — reuse as-is so every week looks and is checked identically.
   - `ledger-<topic>.json` from earlier weeks — for prerequisites and cross-links.
   If the kit doesn't exist, create it at the end (§9) from the templates in this skill.
4. **Pick the mode** (§2). If a pack for this topic already exists and the request isn't an update, save the new one with `_v2` (or next free number); never overwrite.

## 1. Course profile (`course.md`)

Course-specific facts live here, not in this skill. Create it on the first pack for a course and update it whenever you learn something new. Template:

```markdown
# <UNIT CODE> <Course name> — course profile
- Course type: quantitative | conceptual | mixed   (decides §4 branch)
- File naming: e.g. Topic-NN_<Name>.pdf = lecture; <UNIT>_TNN.pdf = tutorial; <UNIT>_TNN_Sol.pdf = solutions;
  <UNIT>_<year>-S<n>_WONN.pdf = workshop (check page 1 for real topic); <UNIT>_Add-Ex-SetN.pdf = extra sets
- Tutorial ↔ topic mapping seen so far: e.g. T05 → Topic 4
- Software / tables: R | Excel | printed z/t/χ²/F tables; rounding convention of official solutions
- Exam format: MCQ / short answer / calculation / essay; open or closed book; formula sheet provided?
- Lecturer's recurring exam phrasings worth keeping verbatim
- Past exams available: list
```

Generic fallbacks if no profile exists: confirm tutorial↔topic mapping from content, not file number; workshops may cover a different topic than the lecture of the same week.

## 2. Modes

| Mode | Trigger | Output |
|---|---|---|
| **Full pack** (default) | "做 Topic 9 复习包", files for one week | Full structure §7, extra practice 8–12 (or 6–10 if a tutorial exists) |
| **Multi-week** | several weeks in one drop | Same structure with part banners per week; 6–8 practice per topic, cap 24 |
| **Cram sheet** 考前速查 | "速查", "考前", "精简版" | 4–8 pages: knowledge map, must-know sheet, A-vs-B traps, 易错点 per topic, 1 worked example per must-know KP. Built from existing ledgers/packs where possible |
| **Solutions update** | official solutions released after a pack was made | Re-check every answer against the new file, fix the recap, re-run QA, save `_v2`, list in Chinese exactly what changed |
| **Final review** 期末总复习 | "期末", "总复习", whole course | Merge all ledgers: cross-topic map, must-know sheet for the course, exam-weighted priorities (from past exams if any), mixed practice set that forces choosing *which* method. Do not re-paste every weekly note |
| **Past-exam recap** | past paper supplied | Treat like a tutorial (§5) plus a topic-frequency table that feeds `course.md` and future emphasis |

Extra-practice *count* stays moderate; *solutions* are full length in every mode.

## 3. Ingest and align

- Extract **all** text, speaker notes, alt text, comments, table values and diagram labels.
- PPTX → `python-pptx`; PDF → `pdftotext -layout` for bulk text and coverage bookkeeping.
- **Math-heavy slides and handwritten/scanned solutions: look at the pages** with the Read tool (`pages`, ≤20 per call). Take formulas, tables and diagrams from what you see; `pdftotext` mangles fractions, subscripts and Greek. Image-only pages → `pdftoppm` + `tesseract` (`chi_sim+eng`).
- Rebuild a knowledge outline (week → topic → atomic knowledge point). Lecture = definition/theorem/formula/distinction; workshop = procedure; tutorial/exam = test of the same point.
- Keep `ledger.json` in the build dir — it drives QA:

```json
{"kps": {"KP9.1": {"en": "One-way ANOVA F-test", "zh": "单因素方差分析 F 检验", "type": "theorem", "must_know": true, "slides": "8-12"}},
 "slides": {"1-7": ["KP9.0"], "8-12": ["KP9.1"]},
 "tutorial": {"T09 Q1a": {"kps": ["KP9.1"], "skills": ["compute", "interpret"], "recap": true, "official": "0.0213", "ours": "0.0213", "diff_explained": false}},
 "practice": {"P1": {"kps": ["KP9.2"], "stars": 2}}}
```
`skills` ∈ classify / compute / prove / interpret / code / read-software-output. `official` / `ours` hold the boxed final value (number or short string); fill `ours` from your Python computation. Set `diff_explained: true` only when you've shown both values and explained the difference in the pack.

For each KP record: ID, English term, Chinese term, type, full English statement, Chinese teaching paragraphs, prerequisites and contrasts, source slides, emphasis (must-know / important / background). Diagrams that carry meaning: describe them in Chinese keeping the slide's English labels, and recreate simple ones (Venn, tree, 2D plot, distribution curve) — no screenshot galleries.

Coverage check before writing (QA enforces the ledger part, you enforce the rest):
- Every non-decorative slide title sits in the outline; every numbered/bulleted teaching point has a home (definition, formula, example or pitfall).
- Every worked numerical example on the slides is rewritten in the notes (never "see slide").
- Every tutorial question maps to ≥1 KP (`【缺讲义】` if its lecture wasn't supplied).
- Every must-know KP appears in the notes **and** is drilled by a tutorial question or an extra practice item.

## 4. Lecture notes — the spine

For each knowledge block, in order:
1. **Context（背景）** — why this block exists, what question it answers (2–5 Chinese sentences).
2. **Definitions / theorems** — full markable English statement, then Chinese clause-by-clause unpacking.
3. **Formulas** — boxed display math; symbols defined in Chinese; **何时使用** and **常见误用** each ≥1 Chinese sentence.
4. **Mechanism / procedure** — numbered steps, each with a Chinese reason.
5. **Worked examples from the slides** — full working with the slide's numbers, a Chinese "why" after each key move, ending with 本题在考什么.
6. **Distinctions and traps** — A-vs-B table (English cells) + Chinese explanation below.
7. **Links** — `→ T09 Q1, Q4`, `→ WO07 task 1`.
8. **本节要点** — 4–8 Chinese bullets the student should write from memory.

Do not dump slides 1:1; do not collapse a 10-slide topic into one English paragraph.

**Quantitative branch** (stats, econometrics, corporate finance, derivatives, accounting calculations):
- **Software output** (R `lm()`/`t.test`/`chisq.test`, Excel, SPSS, Bloomberg-style tables): reproduce in monospace and annotate in Chinese which number answers which exam question. Include at least one "interpret this output" practice item when the topic has output.
- **Tables vs software**: give critical values as the course's printed table does (with df row); note software-exact differences. Follow official rounding (record it in `course.md`).
- **Hypothesis tests** always as the full markable sequence: hypotheses → statistic & null distribution → decision rule → computed value → decision → conclusion in context, Chinese commentary on each line.
- **Finance calculations** (NPV/IRR, bond pricing, CAPM, option payoffs, ratios): show the timeline or cash-flow table, state the sign convention and compounding assumption in Chinese, and flag the classic unit traps (annual vs periodic rate, % vs decimal, nominal vs real).
- Draw distribution / payoff curves (matplotlib → SVG) when the picture teaches more than a paragraph.

**Conceptual branch** (management, governance, ethics, strategy, law-flavoured finance, case-based units):
- Replace "worked example" with **case application**: take each framework and apply it step by step to the lecture's case (or a short invented one, labelled `【补充案例】`), Chinese commentary on each step.
- Add **framework comparison tables** (dimension × framework) and the lecturer's own definitions verbatim.
- For each must-know idea, write a **model short answer in English** (exam-length, markable structure: claim → explanation → example → limitation) followed by Chinese 解析 of why each sentence earns marks.
- Essay/discussion questions: Chinese 答题框架 (how to structure, what the marker looks for), then an English outline — not a full essay unless asked.

## 5. Tutorial / past-exam recap

For **every** question and part:
1. **Stem** — English, complete enough to attempt without the sheet (every number, assumption, α).
2. **Tag** — `[Topic 9 · One-way ANOVA F-test]`.
3. **思路** — Chinese paragraph before any algebra: what type of question, what to define first, which rule/test and why not the look-alike, what the official solution is aiming at.
4. **Steps** — numbered; English markable expression + Chinese why; intermediate arithmetic shown; tables/trees built explicitly.
5. **Final answer** — `#answer[...]`, matching the official value; record both in the ledger.
6. **本题意图** — 2–4 Chinese sentences.
7. **易错点** — the usual wrong answer and why students make it.

Missing lecture for a question → still solve it, flag `【缺讲义】`. Additional exercise sets (`Add-Ex-Set*`): don't recap by default; use them to sense exam flavour and to avoid duplicating them in extra practice. If the user asks for them, recap with this same standard, grouped by topic. Past exams: also produce a topic-frequency table (topic × years × marks) and copy the summary into `course.md`.

## 6. PDF build

**Engine: Typst** (installed in Preflight). No `@preview/…` packages (registry unreachable) — built-ins only. `xelatex` lacks `ctex`/`xeCJK`; don't use it for Chinese. Fallback only if Typst fails: HTML + KaTeX (`npm i katex`, server-side render) → Playwright Chromium `page.pdf({format:'A4', outline:true, tagged:true})`. WeasyPrint is not installed. Never render formulas as images; math must stay searchable text.

Fonts: TeX Gyre Pagella (English), Noto Serif CJK SC (Chinese body), Noto Sans CJK SC (headings), New Computer Modern Math. 10.5 pt, line height ~1.4, A4, 17 mm margins, page numbers, running header `{Course} · {Topics} · Review Pack` (Typst headings become PDF bookmarks automatically). Callout colours: definition blue, formula slate, example green, pitfall amber, tutorial teal; must-know = amber pip.

**`theme.typ`** (tested; if the kit has one, use the kit's copy):

```typst
#let ink = rgb("#1F2933")
#let accent = rgb("#1B4F72")
#let wash = (def: rgb("#EAF2F8"), formula: rgb("#EEF1F4"), example: rgb("#EAF5EC"), pitfall: rgb("#FDF3E1"), tut: rgb("#E6F4F3"))
#let edge = (def: accent, formula: rgb("#52606D"), example: rgb("#2E7D4F"), pitfall: rgb("#B7791F"), tut: rgb("#1F7A73"))
#let setup(course: "", topics: "", body) = {
  set document(title: course + " · " + topics + " · Review Pack")
  set page(paper: "a4", margin: 17mm, numbering: "1",
    header: context { if counter(page).get().first() > 1 [
      #set text(size: 8pt, fill: gray); #course · #topics · Review Pack] })
  set text(font: ("TeX Gyre Pagella", "Noto Serif CJK SC"), size: 10.5pt, fill: ink, lang: "zh", region: "cn")
  show math.equation: set text(font: ("TeX Gyre Pagella Math", "New Computer Modern Math"))
  set par(leading: 0.78em, justify: true)
  set heading(numbering: "1.1")
  show heading: set text(font: ("TeX Gyre Pagella", "Noto Sans CJK SC"), fill: accent)
  show heading.where(level: 1): it => { pagebreak(weak: true); it }
  show raw.where(block: true): set block(fill: rgb("#F5F7FA"), inset: 7pt, radius: 2pt, width: 100%)
  body
}
#let zh(t) = text(size: 0.72em, fill: gray, weight: "regular")[#t]
#let pip = box(baseline: -0.15em, circle(radius: 2.6pt, fill: edge.pitfall))
#let callout(kind, title, body) = block(width: 100%, breakable: true,
  fill: wash.at(kind), stroke: (left: 2.5pt + edge.at(kind)), inset: (x: 9pt, y: 7pt), radius: 2pt,
  [#text(font: ("TeX Gyre Pagella", "Noto Sans CJK SC"), weight: "bold", fill: edge.at(kind))[#title] \ #body])
#let defbox(title, body) = callout("def", title, body)
#let formula(title, body) = callout("formula", title, body)
#let example(title, body) = callout("example", title, body)
#let pitfall(title, body) = callout("pitfall", title, body)
#let tutq(title, body) = callout("tut", title, body)
#let answer(body) = align(center, box(stroke: 0.8pt + accent, inset: 6pt, radius: 2pt, body))
```

Usage: `#import "theme.typ": *`, `#show: setup.with(course: "STAT7055", topics: "Topic 9 ANOVA")`, headings `= Lecture Notes #zh[讲义精讲]`, `#outline(depth: 2)`. Put 思路 / 易错点 / 本题意图 in callouts titled exactly that (e.g. `#tutq[思路][...]`, `#pitfall[易错点][...]`) so QA can find them.

**Typst gotchas** (these cause most compile failures):
- Math: `$x$` inline, `$ x $` (spaces inside) display. `frac(a, b)` or `a/b`; `bar(x)`, `hat(p)`, `tilde`; multi-char subscripts need parens `x_(i j)`, `F_(k-1, n-k)`, `sum_(i=1)^n`; words inside math need quotes `"SST"`, `"under"`; `dot`/`times` for products; `<=`, `>=`, `!=` work.
- In text, escape `#`, `$`, `*`, `_`, `@`, `<` with `\` (e.g. `\$500`). Software output goes in raw blocks.
- Function args that are prose need `[...]` content blocks, not `(...)`.
- Tables: `#table(columns: 3, [a], [b], [c], …)`; set `stroke` and header fill explicitly.

**Build in stages**: one file per part (`00-front`, `10-notes-<topic>`, `20-workshop`, `30-tutorial`, `40-mustknow`, `50-glossary`, `60-practice`, `70-solutions`, `90-sources`, all `.typ`) included from `main.typ`. Compile after each part; track parts in the task list. R isn't installed: reproduce R results in Python and mark any R code you wrote yourself `【未运行】`.

Bilingual pattern: English section title + grey `#zh[中文]`; `English term (中文)` on first use per section; boxes = English statement on top, Chinese explanation below. Not a two-column EN|ZH dump.

## 7. PDF structure (Full / Multi-week mode; omit empty parts)

1. Cover — unit, topics/weeks, files used by kind, missing files, mode
2. 使用说明 — short Chinese guide
3. Contents
4. 学习目标 — what the student can *do*
5. 知识地图 — tree, must-know marked
6. 讲义精讲 (§4)
7. 工作坊操作 — only if workshop files exist (given / goal / steps / checks / typical bugs; say so if it belongs to another topic)
8. Tutorial 逐题精讲 (§5) — only if tutorial files exist
9. 必背清单 — English formulas + Chinese when-to-use, 1–2 pages
10. Glossary — English ↔ 中文 + 1-line Chinese gloss
11. 额外练习 — English stems (Chinese hint only when the stem is linguistically heavy, never leaking the answer); ★/★★/★★★, type, minutes, source tag; built from gaps the tutorial/Add-Ex sets didn't cover; untaught facts labelled `【补充】`
12. 额外练习详解 — new page; §5 standard plus a Chinese wrap-up linking back (`见 §4.3`); for MCQ, why each distractor is wrong
13. Sources — files + slide/question ranges

Multi-week: part-title banners (`Week 3 · …`) inside the same PDF, same design system. Never invent workshop or tutorial sections when those files weren't supplied.

Filename: `{Unit}_{Topics}_Review_CN-EN.pdf` (Cram: `_Cram_CN-EN`; Final: `_Final_Review_CN-EN`).

## 8. QA — run the script, then look

Copy `qa.py` from the kit (or write it from below), then:
`python3 qa.py --pdf OUT.pdf --src . --ledger ledger.json --preview qa-preview`

It hard-fails on: slide ranges with no KPs, tutorial parts without KPs or recap, must-know KPs never drilled, **final answers that disagree with the official solutions** (unless `diff_explained`), 思路/易错点/本题意图 callouts with < 40 Chinese characters, forbidden phrases, non-embedded or Type 3 fonts, missing bookmarks. It *warns* on sections with low Chinese density — treat a warning as "re-read this section against The standard", not "add characters".

Then Read the preview PNGs for: cover, one notes spread, one tutorial solution, the densest table page, every figure page. Check no tofu, no overflowing math/tables, no near-empty pages from unbreakable blocks. Finally re-read `lessons.md` and confirm each rule is honoured. Fix and rerun until `QA PASS`.

```python
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
```

## 9. Deliver and update the kit

1. Write the PDF to the course folder root with `device_commit_files`, and send it with `SendUserFile`. Not linked → just send it and say it can go into the course folder once linked.
2. Update `<course folder>/.build/review-kit/`: `theme.typ`, `qa.py`, `ledger-<topic>.json`, `course.md` (anything newly learned: mapping, rounding, exam format), `README.md` (engine, fonts, how to rebuild). Don't copy source PDFs there. Create `lessons.md` and `exemplars/` if missing.

## 10. Feedback loop — how the skill gets better

**Capture.** When the user gives feedback on a pack ("Q3 思路太空泛", "表格溢出了", "这一节讲得正好"), turn it into a rule and append it to `lessons.md` in this form, then fix the current pack:

```markdown
- [2026-11-10 · Topic 9] RULE: For ANOVA tables, always add a row explaining each df in Chinese.
  WHY: student lost marks confusing k-1 and n-k. SCOPE: course | all-courses
```

**Exemplars.** When the user says a section is exactly right, save that `.typ` excerpt to `exemplars/<topic>-<what>.typ` with a one-line note on what makes it good.

**Promote.** Rules tagged `all-courses` that held for two or more packs belong in this skill itself: tell the user, and when they agree, propose the edit to this SKILL.md via `propose_skills` (an improvement with `edits`). Course-only rules stay in `course.md` / `lessons.md`.

**Regression.** Keep one approved pack's sources + ledger as the course's benchmark (`exemplars/benchmark/`). After a significant skill change, rebuild it and compare page count, QA output and a few pages side by side before trusting the change.

**Prune.** When `lessons.md` passes ~40 rules, merge duplicates and drop ones that no longer bite.

## 11. Tell the user (Chinese, short)

Mode and topics, files by kind (lecture / workshop / tutorial / solutions / past exam / missing), page count, extra-question count, QA result, where the PDF was saved, any `【缺讲义】` or missing-solutions caveats. When regenerating an older pack, say what changed. End with one line inviting specific feedback (什么地方讲浅了 / 排版问题 / 哪一节特别好用) so it can go into `lessons.md`.
