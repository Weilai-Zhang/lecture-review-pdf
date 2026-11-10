# lecture-review-pdf

**[English](#english) · [中文](#中文)**

An Agent Skill that turns university lecture slides, workshop sheets, tutorial questions (with official solutions) and past exams into a **bilingual Chinese–English (中英) review PDF with full worked solutions**.

一个 Agent Skill：把大学的讲义 PPT、workshop、tutorial 习题（含官方答案）和往年考题，整理成一份**中英双语、带完整解题过程的复习 PDF**。

---

## English

### What it does

You give it one week's course files (or several weeks, or the whole course), and it produces a print-ready A4 review pack written for Chinese-speaking students at English-taught universities:

- **English stays where marks are earned.** Exam terms, definitions, theorem statements, formulas and final answers are kept in English, so the wording matches what the exam expects.
- **Chinese does the teaching.** Each definition comes with a plain-Chinese explanation: when to use it, what it does *not* say, and the usual mistakes. Every calculation step explains *why* in Chinese.
- **Nothing is skipped.** Every slide topic, worked example and tutorial part is covered. "See slide" or "同理可得" are not allowed in place of working.
- **Numbers are recomputed.** Every numerical answer is recalculated in Python and checked against the official solutions. Where the two differ, the pack shows both and explains the gap.

Each pack includes: learning objectives, a knowledge map, detailed lecture notes, step-by-step tutorial solutions (思路 → steps → answer → 本题意图 → 易错点), a must-know formula sheet, an EN↔中文 glossary, and extra practice questions with full solutions.

### Modes

| Mode | Say something like | You get |
|---|---|---|
| Full pack (default) | "做 Topic 9 复习包" | Complete pack for one week |
| Multi-week | files from several weeks | One PDF with a section per week |
| Cram sheet | "考前速查" | 4–8 page quick review |
| Solutions update | official solutions just released | Answers rechecked, `_v2` saved, list of changes |
| Final review | "期末总复习" | Whole-course map, priorities, mixed practice |
| Past-exam recap | a past paper | Full solutions + topic-frequency table |

It handles **quantitative** courses (statistics, econometrics, corporate finance, derivatives, accounting) and **conceptual** ones (management, governance, strategy, case-based courses) differently. Quantitative packs get software-output walkthroughs and full hypothesis-test layouts. Conceptual packs get case applications and model short answers.

### How it works

- **Typesetting:** [Typst](https://typst.app) via the `typst` Python package (no LaTeX needed), with an HTML + KaTeX → Chromium fallback. Math stays as searchable text.
- **Built-in QA:** `assets/qa.py` fails the build if a slide range is uncovered, a tutorial part has no solution, a must-know point is never practised, an answer disagrees with the official solution, a 思路/易错点 box is too thin, a forbidden placeholder phrase appears, or fonts are not embedded.
- **Per-course memory:** the first pack for a course creates a `.build/review-kit/` folder with a course profile, the theme and QA script, and a `lessons.md` file. Your feedback on each pack ("Q3 思路太空泛") is saved there as a rule, so later packs get better.

### Install

**Claude apps (claude.ai / desktop):** download this repo as a ZIP (Code → Download ZIP), then add it under *Settings → Capabilities → Skills*.

**Claude Code:**

```bash
git clone https://github.com/Weilai-Zhang/lecture-review-pdf.git ~/.claude/skills/lecture-review-pdf
```

or `npx skills add https://github.com/Weilai-Zhang/lecture-review-pdf`.

**Other agents:** any agent that reads the `SKILL.md` format can use it. Copy the folder into that agent's skills directory.

### Requirements

Python 3 with `typst`, `pypdf` and `numpy`/`scipy`; `poppler-utils` (`pdftotext`, `pdffonts`, `pdftoppm`); fonts TeX Gyre Pagella, Noto Serif/Sans CJK SC and New Computer Modern Math. `tesseract` is only needed for scanned pages.

### Notes

- The skill was written for Claude's cloud workspace. Steps that mention `device_list_dir`, `device_stage_files`, `SendUserFile` or `propose_skills` refer to tools in that environment. In other agents, attach the files directly and the rest works the same.
- The skill talks to the user in Chinese by default.
- Use it with your own course materials. Don't redistribute your university's slides or solutions.

---

## 中文

### 它能做什么

把一周（或多周、或整门课）的课程文件交给它，它会生成一份可以直接打印的 A4 复习包。这份复习包是为在英文授课大学读书的中文学生设计的：

- **得分的地方保留英文**：考试术语、定义、定理表述、公式和最终答案都用英文，和考卷的措辞一致。
- **讲解用中文**：每个定义后面都有大白话的中文解释，讲清楚什么时候用、它*没有*说什么、常见的错误是什么。每一步计算都用中文说明“为什么这样做”。
- **不跳步、不省略**：每一页讲义的知识点、每个例题、每道 tutorial 小问都会覆盖，不允许用“见幻灯片”“同理可得”代替过程。
- **数字重新算过**：所有数值答案都用 Python 重新计算，并和官方答案核对。不一致的地方会把两个结果都列出来，并解释差异的原因。

每份复习包包括：学习目标、知识地图、讲义精讲、tutorial 逐题精讲（思路 → 步骤 → 答案 → 本题意图 → 易错点）、必背公式清单、中英术语表，以及附完整解答的额外练习。

### 几种模式

| 模式 | 你可以这样说 | 得到什么 |
|---|---|---|
| 完整复习包（默认） | “做 Topic 9 复习包” | 单周完整复习包 |
| 多周合并 | 一次给好几周的文件 | 一份 PDF，每周一个部分 |
| 考前速查 | “考前速查”“精简版” | 4–8 页速查表 |
| 答案更新 | 官方答案刚发布 | 重新核对答案，另存 `_v2`，并列出改动 |
| 期末总复习 | “期末总复习” | 全课程知识地图、重点排序、混合练习 |
| 往年考题 | 提供 past paper | 完整解答 + 各主题考频表 |

它对**计算类**课程（统计、计量、公司金融、衍生品、会计）和**概念类**课程（管理、公司治理、战略、案例类课程）采用不同的写法。计算类会逐行解读软件输出，并给出完整的假设检验答题格式。概念类会把框架套到案例上一步步分析，并给出英文的范例简答。

### 工作原理

- **排版**：使用 [Typst](https://typst.app)（通过 Python 的 `typst` 包，不需要 LaTeX）。备选方案是 HTML + KaTeX → Chromium。公式保持为可搜索的文字，不是图片。
- **自动质检**：`assets/qa.py` 会在以下情况让构建失败：有讲义页没被覆盖、有 tutorial 小问没写解答、必背知识点没练到、答案和官方答案不一致、思路/易错点写得太单薄、出现禁止的占位语，或者字体没有嵌入。
- **按课程积累经验**：每门课第一次生成复习包时，会建一个 `.build/review-kit/` 文件夹，里面放课程档案、主题样式、质检脚本和 `lessons.md`。你对每份复习包的反馈（例如“Q3 思路太空泛”）都会作为规则存进去，之后生成的复习包会越来越贴合你的需要。

### 安装

**Claude 应用（claude.ai / 桌面端）**：把本仓库下载为 ZIP（Code → Download ZIP），然后在 *Settings → Capabilities → Skills* 里添加。

**Claude Code**：

```bash
git clone https://github.com/Weilai-Zhang/lecture-review-pdf.git ~/.claude/skills/lecture-review-pdf
```

或运行 `npx skills add https://github.com/Weilai-Zhang/lecture-review-pdf`。

**其他 agent**：只要支持 `SKILL.md` 格式就能用，把文件夹复制到对应的 skills 目录即可。

### 依赖

Python 3，需要 `typst`、`pypdf`、`numpy`/`scipy`；`poppler-utils`（`pdftotext`、`pdffonts`、`pdftoppm`）；字体 TeX Gyre Pagella、Noto Serif/Sans CJK SC、New Computer Modern Math。只有处理扫描件时才需要 `tesseract`。

### 说明

- 这个 skill 是为 Claude 的云端工作环境写的。文中提到的 `device_list_dir`、`device_stage_files`、`SendUserFile`、`propose_skills` 是那个环境里的工具。在其他 agent 里直接上传文件就行，其余流程不变。
- 默认用中文和用户交流。
- 请用你自己的课程资料来生成复习包，不要公开分发学校的讲义或答案。

---

## Files · 文件

```
SKILL.md          the skill itself · skill 本体
assets/theme.typ  Typst theme · 排版主题
assets/qa.py      QA script · 质检脚本
LICENSE           MIT
```

## License · 许可

MIT
