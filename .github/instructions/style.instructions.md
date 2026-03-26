---
description: "Use when writing or editing LaTeX for the SAVNav paper. Covers typography, math notation, citations, figures, tables, units, headings, and list formatting."
applyTo: "**/*.tex"
---

# LaTeX Style Rules

Version: 1.0.0

本文件只约束**写法与排版**，不定义具体术语。术语命名与消歧统一遵循 `terminology.instructions.md`，术语条目统一维护在 `drafts/glossary.md`。

## 1. Typography and Capitalization

- 外部专有名称保持官方大小写，如 `ImageBind`、`YOLO26`、`AudioGoal`。
- 内部通用模块名在正文中使用 sentence case，不写成 CamelCase；仅保留固定名称或缩写，如 `SAVNav`、`SAVMap`。
- 缩写首次出现时写全称加缩写，后文统一只用该缩写。
- 状态名、离散类别名、指令标签使用 `\texttt{}`，如 `\texttt{doorbell}`、`\texttt{STOP}`。

## 2. Math and Units

- 向量、位置、方向使用粗体，如 `\mathbf{p}_{vis}`、`\mathbf{d}_{world}`。
- 标量与参数使用普通数学斜体，如 `$z$`、`$k_d$`、`$\gamma_{mask}$`。
- 环境、集合、映射空间使用 `\mathcal{}`，如 `\mathcal{E}`、`\mathcal{H}`。
- 下标保持数学写法，不混用 `\text{}`，如 `$C_{soc}$`、`\mathbf{p}_{robot}`。
- 数值与单位之间使用 `\,`，单位使用 `\mathrm{}`，如 `2.55\,\mathrm{s}`、`20\,\mathrm{Hz}`、`1.0\,\mathrm{m}`。

## 3. Headings and Lists

- 三级标题统一使用 `\subsubsection{}`。
- `\subsubsection{}` 标题使用 Title Case。
- 不用 `\textbf{...}` 在段首伪造小标题。
- 在 contribution、design choices、feature breakdown 等列举场景中，优先使用 `enumerate`。
- 若 `\item` 以引导短语开头，该短语使用 `\textit{}`、Title Case，并以冒号或句号结束。

## 4. References and Punctuation

- 图、表、章节、公式、文献引用前使用不可断行空格 `~`，如 `Fig.~\ref{...}`、`Table~\ref{...}`、`Sec.~\ref{...}`、`Eq.~\eqref{...}`、`Method~\cite{...}`。
- 引号使用 LaTeX 标准形式 ``...''。
- 复合定语使用单连字符 `-`，如 `audio-visual`、`state-of-the-art`。
- 数值范围使用双连字符 `--`，如 `3--5`、`1.0--2.0\,\mathrm{m}`。

## 5. Emphasis

- 不在正文中使用 `\textbf{}` 做语气强调。
- `\textbf{}` 仅用于表格中的最佳或次佳结果等少数版式场景。
- 不滥用 `\textit{}` 强调普通概念；`e.g.,`、`i.e.,` 等保持正体并跟逗号。
