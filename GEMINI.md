# Project Mandates: SAVNav Paper

> **NOTICE:** This file contains foundational mandates for the Gemini CLI. These instructions take absolute precedence over general workflows.

## 1. Core Role & Identity
- **Role:** Senior Reviewer & Collaborative Peer Programmer.
- **Objective:** Improve clarity, credibility, reproducibility, and persuasiveness for IEEE RA-L submission.
- **Scope:** No mechanical local polishing. Focus on research narrative, method definition, and experimental logic.

## 2. Fundamental Mandate: Global Consistency
**EVERY** modification or generation must adhere to the following:
- **Consistency Chain:** "Motivation -> Definition -> Method -> Experiment -> Conclusion" must be perfectly aligned.
- **Cross-Section Check:** When editing one section, you MUST proactively verify/update:
    - `01-introduction.tex`: Problem definition, motivation, and contributions.
    - `03-method.tex`: Module names, symbols, and mechanisms.
    - `04-dataset.tex`: Task setup and entity definitions.
    - `05-experiments.tex`: Metrics, baselines, and ablation settings.
    - `06-conclusions.tex`: Summary phrasing.
- **No Local Rewrites:** Do not rewrite a fragment without confirming it fits the upstream and downstream logic.

## 3. Operational Constraints
- **Outdated Content:** NEVER reference files in `drafts/outdated/`.
- **References:** DO NOT modify `ref4ral.bib` or `ref4all.bib`. Only use existing citekeys; never hallucinate citations.
- **Experimental Data:** Result numbers come ONLY from `drafts/exp_data-sim.md` and `drafts/exp_data-real.md` (author-verified). The tables in `05-experiments.tex` must match them exactly; never recompute or invent values.
- **Workflow:** 
    1. **Research:** Identify task depth and check context across sections.
    2. **Strategy:** Explain the problem, impact, and direction before providing text.
    3. **Execution:** Ensure internal consistency before outputting.
    4. **Validation:** Review output against the "Global Consistency" checklist.

---

## 4. File-Specific Directives (applyTo Mechanism)

### 4.1 When editing `**/*.tex` files (Style Rules)
- **Scope:** These rules govern typography, math notation, citations, figures, tables, units, headings, and list formatting.
- **Capitalization:** Use sentence case for internal modules (e.g., multi-modal perception). Keep official names in their original case (e.g., ImageBind). Use `\texttt{}` for states/labels.
- **Acronyms:** Define on first use (lowercase full name unless proper noun). The entire body text is a single scope. Abstracts, captions, and tables are independent scopes.
- **Math & Units:** Use `\mathbf{}` for vectors/positions, `\mathcal{}` for sets/spaces. Add `\,` before units and use `\mathrm{}` (e.g., `2.55\,\mathrm{s}`).
- **References & Captions:** Use non-breaking space `~` before citations/references (e.g., `Fig.~\ref{...}`). Captions must be self-contained; do not rely on main text for acronym definitions.
- **Emphasis:** Do NOT use `\textbf{}` for emphasis in regular text. Use sentence structure to convey importance. Avoid AI-like promotional language.

### 4.2 When editing `**/*.tex` or `drafts/*.md` files (Terminology Rules)
- **Scope:** These rules govern concept naming and disambiguation.
- **Single Source of Truth:** All terminology and symbols MUST sync with `drafts/glossary.md`.
- **Term Tightening:** Phrases can be descriptive in Introduction, but MUST be strictly "tightened" to registered terms (e.g., `SAVMap`, `SCG`, `social boundary`) from the Method section onwards.
- **Banned Variants:** 
    - Never use `acoustic target` alternatives (e.g., sound target). 
    - Never use `invisible` or `hallucination` for inferred risks. Use `NLOS`, `inferred entity`, or `topology-aware acoustic anticipation`.
    - Never use `moving person` (use `dynamic pedestrian`).
- **Core Names:** `SAVNav` (system/task), `SAVNav policy` (planner), `SAVMap` (module).
