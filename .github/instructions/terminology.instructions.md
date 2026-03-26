---
description: "Use when writing or editing LaTeX paper files, defining methodology, or introducing new technical concepts. Enforces strict terminology and glossary syncing."
applyTo: "**/*.tex, drafts/**/*.md"
---

# Terminology & Glossary Workflow

在撰写和修改 LaTeX 章节或起草方法时，必须严格遵守术语规范，绝不可为求词汇丰富而随意变换学术专有名词。

## 1. 强制对齐唯一术语表 (Strict Consistency)

- **唯一事实来源**：动笔撰写 `**/*.tex` 之前，必须查阅 `drafts/glossary.md`。
- **一词一义 (One Concept, One Term)**：禁止在同篇论文中用不同词汇指代同一概念。
  - _反面示例_：随意混用 `target source`, `target audio`, `semantic target`。
  - _正确规范_：统一使用 `acoustic target`。

## 2. 新概念命名的四大原则 (Principles for Naming)

为新增模块、变量或逻辑命名时，遵循以下准则：

- **正交且具象的前缀修饰 (Orthogonal Modifiers)**
  - 弃用笼统/口语化词汇，使用严谨的物理/状态前缀。
  - _示例_：将泛泛的 `unseen human` 改为精准的 `NLOS dynamic pedestrian`。
- **杜绝变量重载 (No Variable Overloading)**
  - 相同的核心词干严禁用于表达不同的数学概念。
  - _反面示例_：将映射置信度 $S_{belief}$ 和地图概率分布 $\mathcal{M}_{belief}$ 都称为“Belief”。
  - _正确规范_：分离为 `anchoring confidence` 和 `target spatial belief`。
- **精确优于简短 (Precision Over Brevity)**
  - 术语必须直观反映内在机制，避免宽泛词汇（如用 `success rate` 替代笼统的 `performance`）。
- **规避学术雷区与负面词汇 (Avoid Taboos & Negative Buzzwords)**
  - 禁用带有负面技术偏见或严重歧义的词汇。
  - _反面示例_：使用 `hallucination / hallucinated momentum` 指代盲区行人推测。在当前语境下，"hallucination (幻觉)" 专指 AI 的致命编造缺陷，严重有损方法的严谨性。
  - _正确规范_：更正为 `topology-aware acoustic anticipation / inferred entities`。

## 3. 术语池同步维护 (Synchronous Maintenance)

- 新增术语并写入正文后，**必须立即**将其英文原名、中文解释及 LaTeX 数学符号更新至 `drafts/glossary.md`，确保全局一致。
