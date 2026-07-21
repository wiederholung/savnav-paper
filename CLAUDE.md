# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A LaTeX manuscript (not a software project) for an IEEE Robotics and Automation Letters (RA-L) submission:
**"Listen to Yield: Socially-Aware Audio-Visual Navigation via Acoustic Boundaries"** (SAVNav).

Work here is research writing — narrative, method definition, experimental argument, terminology consistency — not mechanical local polishing. Adopt a senior-reviewer stance: before editing any passage, judge its function in the whole paper.

## Build

Compile the PDF with `latexmk` (MiKTeX + pdflatex are on PATH):

```sh
latexmk -pdf main.tex          # full build: pdflatex -> bibtex -> pdflatex x2
latexmk -c                     # clean intermediate files (keeps main.pdf)
```

Manual sequence if needed: `pdflatex main` → `bibtex main` → `pdflatex main` → `pdflatex main`.

- Entry point is [main.tex](main.tex); it `\input`s `templates/ral/head` (document class `IEEEtran[conference]` + package preamble) then the six section files in order.
- Bibliography is resolved from `ref4ral.bib` (see `\bibliography{ref4ral}` in main.tex). Style: `IEEEtran`.
- All intermediate files (`*.aux`, `*.bbl`, `*.log`, `*.synctex.gz`, etc.) and the root `main.pdf` are gitignored.
- Two git remotes: `origin` (GitHub) and `overleaf`. Push to `origin` only; touch `overleaf` only when explicitly asked.

## Structure

- [main.tex](main.tex) — title, abstract, section includes, bibliography. The active title is the `\title{...}` line that is *not* commented out.
- [sections/](sections/) — the paper body, one file per section. Edit these, not main.tex, for content:
  - `01-introduction.tex` — problem definition, motivation, contributions (`enumerate` list).
  - `02-related_work.tex` — social navigation, audio-visual navigation, active auditory perception.
  - `03-method.tex` — problem formulation, module names, symbols, mechanisms, the method figure.
  - `04-dataset.tex` — task setup, entity definitions, Habitat/SoundSpaces simulation, metrics, comparison table.
  - `05-experiments.tex` — metrics, baselines, ablations, results.
  - `06-conclusions.tex` — summary.
- [figures/](figures/) — each figure ships as a `.pdf` (the form `\includegraphics` references), usually exported from a same-named `.pptx` source kept alongside it: edit the `.pptx`, re-export the `.pdf`; the `.png` is a preview. Exception: `exp-q-sim.pdf` and `exp-q-real.pdf` are composed by `scripts/build_exp_q_sim.py` / `scripts/build_exp_q_real.py` from keyframes under `figures/qualitative_exp/` — edit the script or frames and re-run; there is no `.pptx` to export.
- [drafts/savnav_impl.md](drafts/savnav_impl.md) — method implementation details; the ground-truth reference for what the method actually does.
- [drafts/glossary.md](drafts/glossary.md) — the single source of truth for terminology, acronyms, and math symbols (see below).
- [templates/](templates/) — `ral/` (active, IEEEtran conference class) and `rss/` (alternate).
- [references/](references/) — source `.tex`/`.md`/PDFs of key cited works (e.g. Falcon, ENMuS³), at repo root.

## Hard constraints

These override convenience. Violating them corrupts the paper or the citation graph.

- **Never modify `ref4ral.bib` or `ref4all.bib`.** They are managed externally by Zotero. Only cite existing citekeys; never invent or hallucinate a citation. `ref4ral.bib` (~60 curated refs) is what the paper compiles against; `ref4all.bib` (~160) is the larger pool.
- **Experimental numbers come only from `drafts/exp_data-sim.md` and `drafts/exp_data-real.md`.** Both are author-verified; the results tables in `05-experiments.tex` must match them exactly. Never recompute, extrapolate, or recall values from any other source.
- **Never reference anything under `drafts/outdated/` or `figures/outdated/`.** That content is stale.
- **Terminology and symbols sync to `drafts/glossary.md`.** Register a new term/acronym/symbol there *before* using it in the body. On conflict, the glossary wins and the prose is corrected to match.
- **Global consistency.** The chain motivation → definition → method → experiment → conclusion must stay aligned. When you change a core setting, term, symbol, or contribution, proactively check and update the other sections (intro ↔ method ↔ dataset ↔ experiments ↔ conclusion), not just the local passage.

## Writing rules

Full rules live in `.github/instructions/` — read them before substantive edits:

- [style.instructions.md](.github/instructions/style.instructions.md) — *how to write*: capitalization (sentence case for internal module names; official case for external names like `ImageBind`), acronym scopes (whole body is one scope; abstract/each caption/each table are independent), math (`\mathbf{}` vectors, `\mathcal{}` sets, `\,` before `\mathrm{}` units), `~` before refs/cites, captions must be self-contained, no `\textbf{}` for emphasis.
- [terminology.instructions.md](.github/instructions/terminology.instructions.md) — *what to call things*.

Key naming (from terminology rules): `SAVNav` = whole system/task; `the SAVNav task` = the benchmark; `SAVNav policy` = the planner; `SAVMap` = the acoustic-to-spatial social mapping module. Banned variants include: `sound target`/`audio goal`/`sounding object` (use `acoustic target`); `visible humans` (use `LOS humans`); `invisible`/`hidden`/`unseen`/`hallucination` for inferred risks (use `NLOS`, `inferred entity`, `topology-aware acoustic anticipation`); `moving person` (use `dynamic pedestrian`). The Introduction may use intuitive descriptive language during motivation, but terms tighten to the registered forms from the Method section onward and must not loosen again.

Note: `GEMINI.md` and `.github/copilot-instructions.md` carry the same mandate for other assistants. If you change a core rule (terminology, constraints, section roles), keep all three in sync.
