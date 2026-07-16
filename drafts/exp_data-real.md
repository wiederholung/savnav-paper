# SAVNav 实机实验结果（最终均值，人工校对版）

来源与口径：

- 实机平台 Stretch 3，2 方法 × 3 场景 × 每组 6 episodes，共 36 episodes。
- 方法映射：`ours` = SAVNav (Ours)；`ours_wo_audcost` = w/o Topology-Aware Anticipation（消融，代码 `no_audio_cost`）。
- 场景映射：`los` = Crowded Social；`nlos` = Hidden Boundary；`mixed` = Mixed Home Activity。
- 指标为分数（0–1），保留 4 位小数；列序与论文结果表一致（SR | SPL | STL | Progress | HCR | NCR | PSC）。

> ⚠️ 数据沿革（2026-07-15）：原 `drafts/exp_data-real.xlsx` 由此前仓库 agent 整理，其 **episode 级数值系幻觉产物，不可信**（曾出现重复占位三元组等）；作者发现后仅人工逐值校对了各组**最终均值**，确认无误（与论文 `tab:real_results` 完全一致），episode 级数值未修。该 xlsx 已删除，本文件为实机结果的唯一数据依据。
> episode 级原始数据存于 Stretch 3 实机，暂不便拷贝；如需 per-episode 分析（显著性、误差棒等）需先从机器人取数。

## By scenario

### scenario = los (Crowded Social)

| method          | n   | SR     | SPL    | STL    | Progress | HCR    | NCR    | PSC    |
| --------------- | --- | ------ | ------ | ------ | -------- | ------ | ------ | ------ |
| ours            | 6   | 0.6667 | 0.4957 | 0.2085 | 0.8168   | 0.0000 | 0.0000 | 0.9315 |
| ours_wo_audcost | 6   | 0.6667 | 0.5223 | 0.2232 | 0.8115   | 0.1667 | 0.1667 | 0.9207 |

### scenario = nlos (Hidden Boundary)

| method          | n   | SR     | SPL    | STL    | Progress | HCR    | NCR    | PSC    |
| --------------- | --- | ------ | ------ | ------ | -------- | ------ | ------ | ------ |
| ours            | 6   | 0.5000 | 0.2890 | 0.1370 | 0.6580   | 0.5000 | 0.5000 | 0.8597 |
| ours_wo_audcost | 6   | 0.0000 | 0.0000 | 0.0000 | 0.4323   | 1.0000 | 1.0000 | 0.7602 |

### scenario = mixed (Mixed Home Activity)

| method          | n   | SR     | SPL    | STL    | Progress | HCR    | NCR    | PSC    |
| --------------- | --- | ------ | ------ | ------ | -------- | ------ | ------ | ------ |
| ours            | 6   | 0.3333 | 0.2197 | 0.0898 | 0.5933   | 0.5000 | 0.5000 | 0.8230 |
| ours_wo_audcost | 6   | 0.0000 | 0.0000 | 0.0000 | 0.3972   | 1.0000 | 1.0000 | 0.7375 |
