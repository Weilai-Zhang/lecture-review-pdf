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
