# SAVNav Comparison Methods + ENMuS (test_v6) collated

来源：

- `20260706_174507/comparison.md` — ours / ours_no_active / ours_no_audio_cost / reactive / falcon_oracle / falcon_ours_goal（test_v6 主数据集，n=1008，SELD 推理 use_gt_audio=False）
- `20260708_100737/comparison.md` — enmus（test_v6 的 watertap+television 子集 `test_v6_enmus_watertap_tv`，n=504）

> 注：两者 episode 集合不同（主集 1008，enmus 子集 504，且 los/nlos/mixed 各 168），口径不完全可比；enmus 行仅供参考。
>
> 指标为分数（0–1），保留 4 位小数。SR/SPL/HCR/NCR/PSC 取自各方法 `merged_<method>/metrics_summary.json`
> 的 overall / by_scenario 桶（与各自 comparison.md 完全一致）；Progress 及其后 extras（distance_to_goal /
> min_distance_to_goal / num_steps / … / elapsed_s）为逐 episode 均值。
> STL（Success weighted by Time Length）= mean(success × T*/max(T*, num_steps))，T\* = geodesic_distance / 0.0816
> （每步平移 = lin_speed/ctrl_freq = 9.792/120 = 0.0816 m；仅计平移不计转身）。⚠️ STL 非自动产出指标——
> `run_experiments.py` / `eval_summary.py` 均不出该列，此处由逐 episode geodesic_distance / success / num_steps
> 后处理算得，尚未固化进代码。
> 列顺序参照旧版 `comparison_final.md`（method | n | SR | SPL | STL | Progress | HCR | NCR | PSC | …）

## By scenario

### scenario = los

| method             | n    | SR     | SPL    | STL    | Progress | HCR    | NCR    | PSC    |
| ------------------ | ---- | ------ | ------ | ------ | -------- | ------ | ------ | ------ |
| ours               | 336  | 0.3780 | 0.3420 | 0.2568 | 0.4977   | 0.1220 | 0.0565 | 0.9475 |
| ours_no_active     | 336  | 0.3750 | 0.3380 | 0.2536 | 0.5105   | 0.1190 | 0.0536 | 0.9498 |
| ours_no_audio_cost | 336  | 0.3839 | 0.3523 | 0.2496 | 0.5181   | 0.1190 | 0.0506 | 0.9444 |
| reactive           | 336  | 0.2321 | 0.2093 | 0.1562 | 0.4209   | 0.1280 | 0.0685 | 0.9419 |
| falcon_oracle      | 336  | 0.0804 | 0.0581 | 0.0273 | 0.3471   | 0.3095 | 0.1101 | 0.8982 |
| falcon_ours_goal   | 336  | 0.0774 | 0.0662 | 0.0353 | 0.3027   | 0.3333 | 0.1220 | 0.8783 |
| enmus              | 168  | 0.0000 | 0.0000 | 0.0000 | 0.0993   | 0.1488 | 0.0536 | 0.9567 |

### scenario = nlos

| method             | n    | SR     | SPL    | STL    | Progress | HCR    | NCR    | PSC    |
| ------------------ | ---- | ------ | ------ | ------ | -------- | ------ | ------ | ------ |
| ours               | 336  | 0.3750 | 0.3568 | 0.2828 | 0.5158   | 0.1429 | 0.0565 | 0.9762 |
| ours_no_active     | 336  | 0.3601 | 0.3385 | 0.2704 | 0.5059   | 0.1458 | 0.0655 | 0.9662 |
| ours_no_audio_cost | 336  | 0.3423 | 0.3248 | 0.2613 | 0.5149   | 0.1905 | 0.0685 | 0.9597 |
| reactive           | 336  | 0.2262 | 0.2102 | 0.1630 | 0.4309   | 0.1339 | 0.0595 | 0.9666 |
| falcon_oracle      | 336  | 0.1399 | 0.1112 | 0.0541 | 0.3979   | 0.2530 | 0.0833 | 0.9501 |
| falcon_ours_goal   | 336  | 0.1042 | 0.0817 | 0.0437 | 0.3487   | 0.2708 | 0.1131 | 0.9482 |
| enmus              | 168  | 0.0000 | 0.0000 | 0.0000 | 0.1805   | 0.1012 | 0.0179 | 0.9899 |

### scenario = mixed

| method             | n    | SR     | SPL    | STL    | Progress | HCR    | NCR    | PSC    |
| ------------------ | ---- | ------ | ------ | ------ | -------- | ------ | ------ | ------ |
| ours               | 336  | 0.3929 | 0.3605 | 0.2808 | 0.5139   | 0.1339 | 0.0565 | 0.9617 |
| ours_no_active     | 336  | 0.3601 | 0.3347 | 0.2634 | 0.4948   | 0.1429 | 0.0625 | 0.9583 |
| ours_no_audio_cost | 336  | 0.3839 | 0.3556 | 0.2709 | 0.5129   | 0.1458 | 0.0655 | 0.9551 |
| reactive           | 336  | 0.2500 | 0.2264 | 0.1731 | 0.4305   | 0.1577 | 0.0595 | 0.9503 |
| falcon_oracle      | 336  | 0.1042 | 0.0784 | 0.0370 | 0.3251   | 0.3899 | 0.1131 | 0.8744 |
| falcon_ours_goal   | 336  | 0.0655 | 0.0555 | 0.0288 | 0.2987   | 0.3869 | 0.1161 | 0.8850 |
| enmus              | 168  | 0.0000 | 0.0000 | 0.0000 | 0.1662   | 0.2679 | 0.0417 | 0.9384 |
