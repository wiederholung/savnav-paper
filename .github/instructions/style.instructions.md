---
description: "Use when writing or editing LaTeX paper files. Enforces strict typographic guidelines, math notations, abbreviations, unit formats, and layout styles for the SAVNav paper to meet top-tier robotics conference/journal standards."
applyTo: "**/*.tex"
---

# LaTeX Formatting & Stylistic Guidelines

在撰写和修改 LaTeX 源文件（特别是 .tex 格式文件）时，必须严格遵循以下格式与风格约定，确保整篇论文呈现高度一致且专业的顶级会议/期刊水平。对于术语的具体选择和消歧，请完全参照 `drafts/glossary.md` 和 `terminology.instructions.md`，本文件仅规范其字体、大小写和排版风格。

## 1. 字体排版与缩写规范 (Typography & Abbreviations)

- **术语大小写通用法则**：
  - **缩略语与专有模块**保持原有大小写或系统指定格式（如框架名词、模块缩写）。
  - **一般概念与机制特征**（如物理现象、事件类别、策略动作）：**一律采用全小写首字母**。严禁将普通技术复合词使用大驼峰（CamelCase）或首字母大写。
  - **首次使用说明**：任何带有首字母缩写（Acronyms）的复合术语在正文中首次出现时，必须给出全拼（遵从小写规则）并附带带括号的缩写，后续行文**直接且仅使用**该缩写。
- **状态指令与类别标签**：必须使用 `\texttt{}` 包裹，且无需任何多余引号。例如分类标签、状态机指令等。

## 2. 数学符号与物理单位体系 (Math Notations & Units)

- **向量与坐标**：采用加粗方式，如 `\mathbf{p}_{vis}`, `\mathbf{v}_{infer}`, `\mathbf{d}_{world}`。
- **标量与参数**：常规模板，如 `$z$`, `$\gamma_{mask}$`, `$k_d$`。
- **空间/集合**：大写手写体（Calligraphic），如 `\mathcal{E}`, `\mathcal{H}`, `\mathcal{O}_{static}`。
- **带下标的变量**：论文中保持**全斜体下标**，不要混用（即统一写作 `$C_{soc}$`, `\mathbf{p}_{robot}`，不要用 `\text{soc}`）。
- **🏆 物理单位绝对红线（严禁出现 1m 或 1 m）**：
  - 数值与单位之间**必须添加极小空格 `\,` 并且单位使用 `\mathrm{}` 正体**。
  - 示例：`1.0\,\mathrm{m}`，`2.55\,\mathrm{s}`，`20\,\mathrm{Hz}`。

## 3. 按语与强调规范 (Formatting & Typographical Marks)

- **斜体 (`\textit{}`)**：
  - **禁止斜体强调用途**：不再对概念和专有名词加斜体。一律使用正常字体。
  - **拉丁短语**：学术常见词汇如 e.g., 或 i.e.,，**直接用正体**即可（不需斜体），但注意其后必须带逗号（如 e.g., a ringing doorbell）。
- **粗体 (`\textbf{}`)**：
  - 🔴 **绝对禁止在正文句子内部作为情绪强调或事实强调使用**。
  - ✅ 可接受场景一：表格中的**最佳结果加粗**。
  - ✅ 可接受场景二：段首引导词（Run-in Headings）。段首的 `\textbf{引导词.}` 后必须紧接标点（句号或冒号），随后空一格接正文。
- **引号**：
  - 避免滥用引号，更避免用其做主观强调。
  - 必须使用标准 LaTeX 引号格式，即左侧双撇号 ` `` `，右侧单双撇号 `''`。正确形式如：` ``deaf'' `。

## 4. 交叉引用与连词号 (References & Dashes)

- **不可断行空（Tie/Tilde `~`）**：所有对图、表、章节的交叉引用，以及文献引用之前**必须**加 `~`。
  - 示例：`Table~\ref{tab:benchmark_tiers}`，Scene A 之间可用 `Scene~A`，`Method~\cite{OpenvocabularySoundEvent2025}`。
- **连字符**：
  - **复合词定语**使用单连字符 `-`：如 Audio-Visual, human-populated, state-of-the-art。
  - **数字范围**强制使用双连字符 `--` (En-dash)：如 3--5 humans, `1.0--2.0\,\mathrm{m}`。

## 5. 论文结构与列表规约 (Lists & Sentences)

- **无脑多重嵌套括号**：克制使用括号 `()`。括号仅限做极为简短的举例补充（如 (e.g., walls, furniture)），长说明请分离成独立从句或新句。不要出现括号套括号的情况。
- **列表内容 (itemize)**：
  - 在撰写 Contribution、Benchmark 设定、Limitation 等部分时，每项 item 首先应以一个带冒号的粗体短语作为总起（如 `\item \textbf{Acoustic-to-Spatial Social Mapping (SAVMap):} We propose...`）。
  - 引导词后需接完整的、语法完善的句子，最后以句号结尾，不要写成散漫的碎语段落。
