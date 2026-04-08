---
description: "Use when writing or editing LaTeX for the SAVNav paper. Covers typography, math notation, citations, figures, tables, units, headings, and list formatting."
applyTo: "**/*.tex"
---

# LaTeX Style Rules

Version: 1.2.1

本文件只约束**写法与排版**，不定义具体术语。术语命名与消歧统一遵循 `terminology.instructions.md`，术语条目统一维护在 `drafts/glossary.md`。

## 0. Role of This File

- 本文件回答“怎么写更一致”，不回答“术语叫什么”。
- 全局一致性流程与多章节同步修改的要求，见 `copilot-instructions.md`。
- 风格优化服务于信息传达，不服务于华丽改写。

## 1. Scope and Priority

- 本文件只规定作者可直接控制的写法决策：大小写、数学排版、列表写法、缩写展开、caption 自洽、引用呈现。
- 具体术语命名不在本文件定义；术语选择以 `terminology.instructions.md` 和 `drafts/glossary.md` 为准。
- 能交给 LaTeX 模板、文档类、既有环境或宏自动处理的版式，不在本文件中重复规定实现细节。

### Editing Principle

- 优先减少歧义、跳跃和信息拥挤，而不是单纯追求句子更长或更“学术”。
- 若一句话同时承担定义、对比、贡献、结果解释四种功能，应优先拆分，而不是堆叠修饰。
- 若某段逻辑已清楚，不要只为风格变化而大改。

## 2. Capitalization and Naming Form

- 外部专有名称保持官方大小写，如 `ImageBind`、`YOLO26`、`AudioGoal`；如有缩写，首次出现时写全称加缩写，如 `contrastive language-audio pretraining (CLAP)`。
- 正文中的内部模块名、机制名、地图名、代价场名使用 sentence case；禁止为强调而写成 Title Case 或 CamelCase。
- 内部术语在正文首次引入缩写时，全称仍保持小写，如 `multi-modal perception (MMP)`；不要写成 `Multi-Modal Perception (MMP)`，除非该短语位于标题、列表引导短语或图中标签。
- 标题与列表引导短语中的标题性短语可使用 Title Case；普通叙述句中的内部术语保持小写。
- 状态名、离散类别名、指令标签使用 `\texttt{}`，如 `\texttt{doorbell}`、`\texttt{stop}`。
- 不为避免重复而随意替换同一概念的表面写法；若同一对象已有固定写法，优先复用既有表达。
- 不把普通描述性短语包装成看似专有名词的写法；只有已登记的固定名称或缩写才应表现为专名。

### Preferred Sentence Texture

- 优先使用具体主语和明确谓语，少用空泛主语如 `this`, `it`, `they` 指代整句复杂内容。
- 优先把比较对象、条件和结果写明，避免只写抽象判断如 `is effective`, `is robust`, `is better`。
- 少用连续名词堆叠；修饰链过长时优先拆句。

## 3. Acronyms and Independent Scopes

- 缩写首次出现时写全称加缩写，且**全称若非专有名词须保持小写**；之后在同一作用域中统一只用缩写。
- 正文（从 Introduction 到 Conclusion）、摘要、图、表和每一张图、表的 Caption 是彼此独立的缩写作用域。
- 整个正文是一个**单一的全局缩写作用域**，绝不能把每个单独的 Section（如 Method）当作独立作用域。
- 若已使用 `NLOS`，通常也应对称使用 `line-of-sight (LOS)`，随后统一写 `LOS` 与 `NLOS`。
- 仅在确有阅读收益时引入新缩写；若术语仅出现少数几次且缩写不会明显减轻行文负担，则优先保留全称。
- 不为局部简洁而创造临时缩写；同一缩写在全文中只能对应一个明确概念。
- 图中或表中可以直接使用缩写以节省空间，但对应 caption 或表注必须自洽，不能依赖正文中的定义。
- 图注中首次出现的关键缩写，优先在句内直接写全称加缩写；若缩写较多，可在 caption 末尾或表下注释中集中释义。
- 表格若包含多个缩写，优先在表下注释统一解释，而不是在 caption 主句中堆叠定义。
- teaser figure 的 caption 必须单独解释关键缩写。
- 若某缩写只出现在单个图表内，也仍需在该图表的 caption 或注释中解释一次。
- 正文中不要反复写“全称（缩写）”；首次定义后，除进入新作用域外直接使用缩写。

### Acronym Restraint

- 不要为局部段落临时引入只出现一两次的缩写。
- 若一句话已有两个以上非通用缩写，优先回退其中一个为全称。

## 4. Headings, Lists, and Run-in Phrases

- 三级标题统一使用 `\subsubsection{}`，并使用 Title Case。
- 不用 `\textbf{...}` 在段首伪造小标题。
- 在 contribution、design choices、feature breakdown 等列举场景中，优先使用 `enumerate`。
- 列表引入句应为完整陈述，并以冒号结尾，如 ``The main contributions of this letter are summarized as follows:''。
- 若 `\item` 以引导短语开头，该短语使用 `\textit{}`、Title Case，并以冒号或句号结束。
- 若列表项为完整句，则各项写成完整句并以句号结束；若列表项仅为并列短语，则各项保持平行结构，并在全列表中统一标点方式。
- 列表只在确有并列结构、贡献概述或设计拆分时使用；若内容本质上是连续论证，优先保留普通段落。
- 不把一个自然段硬拆成列表来制造“贡献感”或“结构感”；列表应服务于信息组织，而非语气强化。
- 同一列表内不要混用完整句、短语、问题句等不同语法层级。

### Contribution Writing

- 贡献列表中的每一项都应对应论文中可定位的实质内容：任务、方法、机制、数据、指标或实验发现。
- 不把“进行了大量实验”“验证了有效性”单独写成空泛贡献；要说明验证了什么、相对谁、通过哪些设置。
- 若贡献点之间存在依赖关系，列表顺序应体现从任务定义到方法，再到验证的叙事顺序。

## 5. Math and Units

- 向量、位置、方向使用粗体，如 `\mathbf{p}_{vis}`、`\mathbf{d}_{world}`。
- 标量与参数使用普通数学斜体，如 `$z$`、`$k_d$`、`$\gamma_{mask}$`。
- 环境、集合、映射空间使用 `\mathcal{}`，如 `\mathcal{E}`、`\mathcal{H}`。
- 下标保持数学写法，不混用 `\text{}`，如 `$C_{soc}$`、`\mathbf{p}_{robot}`。
- 数值与单位之间使用 `\,`，单位使用 `\mathrm{}`，如 `2.55\,\mathrm{s}`、`20\,\mathrm{Hz}`、`1.0\,\mathrm{m}`。
- 数学符号一旦在某节定义，应尽量在全文保持同一字母、下标和含义，不为局部措辞方便而改写符号系统。

### Math Prose Coupling

- 引入公式前先说明该式解决什么问题；公式后说明关键变量、结构含义或优化直觉。
- 不要让一组符号只在公式中出现而无文字解释。
- 若公式只是把前文直觉形式化，正文中仍应保留直觉说明。

## 6. References, Captions, and Punctuation

- 图、表、章节、公式、文献引用前使用不可断行空格 `~`，如 `Fig.~\ref{...}`、`Table~\ref{...}`、`Section~\ref{...}`、`Eq.~\eqref{...}`、`Method~\cite{...}`。
- 关键外部方法、模型或数据集在每个主要章节首次出现时重新给出 `\cite{...}`，便于跳读；但同一段落或紧邻上下文中避免重复堆叠引用。
- 图注或表注中提及关键外部方法、模型或数据集时，若该信息对独立理解图表是必要的，应在该 caption 中补上 `\cite{...}`。
- 图表 caption 应尽量做到脱离正文也能理解；不要让 caption 依赖正文中的缩写定义、术语解释或文献上下文。
- caption 优先用信息密度高的陈述句，先说明图表展示了什么，再补必要条件、缩写解释或比较对象。
- 不在同一句中同时堆叠过多括号、缩写展开和文献编号；若信息过载，应拆分 caption 结构或改用表下注释。
- 不把正文中的完整论证搬进 caption；caption 负责说明内容、对象和必要条件，不承担长篇分析。
- 同一段内不要连续堆叠多个引用块；若确需并列多篇文献，先保证叙述主干清楚，再附引用。
- 引号使用 LaTeX 标准形式 ``...''。
- 复合定语使用单连字符 `-`，如 `audio-visual`、`state-of-the-art`。
- 数值范围使用双连字符 `--`，如 `3--5`、`1.0--2.0\,\mathrm{m}`。

### Caption Standard

- caption 第一分句应直接回答“图/表展示了什么”。
- caption 第二层信息再说明比较对象、场景条件、颜色含义、缩写解释或结论线索。
- 若图表承担关键论证作用，caption 至少要让读者不回正文也能看懂对象、任务和评价维度。

## 7. Emphasis

- 不在正文中使用 `\textbf{}` 做语气强调。
- `\textbf{}` 仅用于表格中的最佳或次佳结果等少数版式场景。
- 不滥用 `\textit{}` 强调普通概念；`e.g.,`、`i.e.,` 等保持正体并跟逗号。
- 通过句子结构、信息顺序和术语一致性表达重点，而不是依赖视觉强调。
- 避免为了“更像论文”而引入空泛的强调词；优先用更具体的对象、条件、比较和结论支撑重点。
- 避免 AI 痕迹明显的空泛套话、机械排比和过度包装；保持表达具体、克制、信息导向。

## 8. Final Quality Check

在提交一段新文本前，至少自检以下问题：

- 这段话是否清楚回答了它在本节中的功能？
- 是否复用了 glossary 中的主术语，而不是临时换说法？
- 是否引入了不必要的新缩写、长修饰链或空泛评价词？
- 是否与相邻段落在贡献、设定、符号和结论上保持一致？
- 删掉形容词后，句子是否仍然具体、成立、可验证？
