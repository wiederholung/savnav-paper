---
description: "Use when writing or editing SAVNav terminology, method text, or drafts. Covers naming consistency, glossary sync, and banned variants such as acoustic target, SAVMap, and NLOS."
applyTo: "**/*.tex, drafts/*.md"
---

# Terminology Rules

Version: 1.2.1

本文件只约束**概念命名与消歧**。`drafts/glossary.md` 是术语条目与符号条目的唯一登记处；本文件不重复维护术语表。

## 0. Role of This File

- 本文件回答“概念叫什么”，不负责排版。
- 大小写、缩写展开、caption、列表和数学写法交给 `style.instructions.md`。
- 全局一致性流程或多章节同步修改的要求，见 `copilot-instructions.md`。

## 1. Single Source of Truth

- 写作前先对齐 `drafts/glossary.md`。
- 同一概念全篇只保留一个主术语，不为同一对象制造近义替换（见下方特例：认知梯度与过渡）。
- **认知梯度与过渡特例：** 允许在 Introduction（特别是 Motivation 阶段）使用符合直觉的自然描述性语言（如 `implicit social norms`, `people engaged in conversation`）平滑初读者的认知负荷。术语的“严格收紧”应通过自然桥接的方式在“概念注册时刻”（如贡献声明或任务定义处）完成。一旦注册到系统表示（如 `social boundary`, `SCG`），后续正文（特别是 Method 和 Experiments 中）必须**绝对收紧**，禁止退回泛化描述。此外，绝不将其高层动机（norms）与系统实现约束（boundaries）混淆并机械互换。
- 若新增术语、缩写或符号，先补充 `drafts/glossary.md`，再在正文中使用。
- 若某节改动涉及术语边界或定义范围，应同步检查整篇论文中对应写法是否仍一致。
- 若正文收紧区（Method及以后）与 glossary 冲突，应修正文稿，不做局部折中。

## 2. Core Naming Decisions

- `SAVNav`：整个方法/系统。
- `the SAVNav task`：论文定义的任务或 benchmark。
- `SAVNav policy`：规划与决策模块。
- `SAVMap`：`acoustic-to-spatial social mapping` 模块。
- 除已登记的固定名称外，不将普通描述性短语写成看似专有名词的形式。

### Usage Boundary

- `SAVNav` 只指整个系统、方法或主框架。
- `SAVNav policy` 只指规划与决策层。
- `SAVMap` 是模块名；功能描述写作 `acoustic-to-spatial social mapping`，不要混写成多个变体。

## 3. Preferred and Banned Variants

- 目标发声对象统一写 `acoustic target`，不要改写成 `target source`、`target audio`、`semantic target` 等。
- 视距内、未遮挡的视觉感知统一使用 `line-of-sight (LOS)`。不要使用 `visible` 后接实体词（如 `visible humans`，应替换为 `LOS humans`）。
- 对视距外风险统一使用 `NLOS`、`inferred entity`、`topology-aware acoustic anticipation` 这组表述。不使用 `invisible` 等模糊表达。
- 不使用 `hallucination`、`hallucinated` 描述推断出的实体、速度或风险。
- 若指代“运动中的行人”这一已登记概念，统一使用 `dynamic pedestrian`；不要改写成 `moving person`、`walking human` 等临时说法。
- 不为追求语言变化而在相邻段落中切换同一概念的命名形式。

### Additional Banned Patterns

- 不用 `audio goal`、`sound target`、`sounding object` 等词替代 `acoustic target`。
- 不用 `unseen`、`hidden human`、`occluded person` 泛化替代 `NLOS` 或 `inferred entity`，除非确实只在描述视觉状态。
- 不用 `social map` 泛指 `SAVMap` 或 `social cost field`；这两者在功能上不同，不能混用。
- 不用 `planner`、`navigation head`、`controller` 等松散词替代 `SAVNav policy`，除非明确只在描述一般功能。

## 4. Naming Principles for New Concepts

- 名称应优先表达物理属性、感知来源或功能角色，避免空泛修辞。
- 若两个概念功能不同，则名称词干也应不同，避免一词多义。
- 论文正文中的模块名、机制名、地图名、代价场名应与 glossary 条目完全一致。
- 新名称应先判断是否真是新概念；若只是已有概念的局部描述、阶段描述或视角变化，不额外造新名。
- 新缩写只在确有阅读收益时引入；同一缩写在全文中只能对应一个明确概念。

### Decision Rule Before Coining a New Term

新增名称前，先问四个问题：

1. 这是否真的是一个独立概念，而不是已有概念的属性、阶段或结果？
2. 它是否会在多处反复出现，值得命名？
3. 它是否与现有 glossary 条目在功能边界上清晰区分？
4. 它是否会迫使 Introduction、Method、Experiments、Conclusion 同步补定义？

只要其中任一答案偏否定，就优先复用已有术语。

## 5. Synchronization Rule

- 当术语、缩写、符号、中文释义发生变化时，只在 `drafts/glossary.md` 维护主记录。
- `style.instructions.md` 负责写法，`terminology.instructions.md` 负责命名原则，`drafts/glossary.md` 负责词条内容。
- 若 `drafts/glossary.md` 与正文、图注或表注出现冲突，以 glossary 为准，并回查相关章节统一修正。
