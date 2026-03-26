---
description: "Use when writing or editing SAVNav terminology, method text, or drafts. Covers naming consistency, glossary sync, and banned variants such as acoustic target, SAVMap, and NLOS."
applyTo: "**/*.tex, drafts/*.md"
---

# Terminology Rules

Version: 1.0.0

本文件只约束**概念命名与消歧**。`drafts/glossary.md` 是术语条目与符号条目的唯一登记处；本文件不重复维护术语表。

## 1. Single Source of Truth

- 写作前先对齐 `drafts/glossary.md`。
- 同一概念全篇只保留一个主术语，不为同一对象制造近义替换。
- 若新增术语、缩写或符号，先补充 `drafts/glossary.md`，再在正文中使用。

## 2. Core Naming Decisions

- `SAVNav`：整个方法/系统。
- `the SAVNav task`：论文定义的任务或 benchmark。
- `SAVNav policy`：规划与决策模块。
- `SAVMap`：`acoustic-to-spatial social mapping` 模块。

## 3. Preferred and Banned Variants

- 目标发声对象统一写 `acoustic target`，不要改写成 `target source`、`target audio`、`semantic target` 等。
- 对视距外风险统一使用 `NLOS`、`inferred entity`、`topology-aware acoustic anticipation` 这组表述。
- 不使用 `hallucination`、`hallucinated` 描述推断出的实体、速度或风险。
- 不用宽泛词替代已定义术语，如用 `dynamic pedestrian` 代替 `unseen human`、`moving person` 之类临时说法。

## 4. Naming Principles for New Concepts

- 名称应优先表达物理属性、感知来源或功能角色，避免空泛修辞。
- 若两个概念功能不同，则名称词干也应不同，避免一词多义。
- 论文正文中的模块名、机制名、地图名、代价场名应与 glossary 条目完全一致。

## 5. Synchronization Rule

- 当术语、缩写、符号、中文释义发生变化时，只在 `drafts/glossary.md` 维护主记录。
- `style.instructions.md` 负责写法，`terminology.instructions.md` 负责命名原则，`drafts/glossary.md` 负责词条内容。
