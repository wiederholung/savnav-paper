# TODO

## 数据集

[x] 更新数据集表述，跟最新test_v6同步
[x] 更新enmus专用数据集描述
[x] 补充数据集统计图片
[x] 补充新指标 Progress, STL
[x] (0715复查新发现) Hidden Boundary 范围自洽性：正文/表格 "1--3" + 构成 "0--1 SCG + 1 DP"，但 SCG 定义为 2--3 人，组合上限应为 4；已核实生成代码该场景 SCG 定死 2 人，正文已补 "two-person conversational group" 限定，"1--3" 保持

## 实验

[x] 仿真实验最新结果以 ./drafts/exp_data-sim.md 为准(只报告SR到PSC的指标)，更新/重写所有相关内容（0715 复查：表格+正文全部数字与 exp_data-sim.md 逐格核对一致，加粗正确）
[x] w/o tp anticip... 消融变体有调整，改为不计算任何视线外声音产生的cost，跟代码 no_audio_cost 对齐，但这个消融的名字不变
[x] 仿真定性分析节插入新图 figures/exp-q-sim.pdf
[x] 仿真定性分析需要读图分析重写（已按新版三场景对比图重写正文与 caption）
[x] 添加实机实验节，在los、nlos、mixed 3个设置下测了ours、ours_no_aud_cost 2个方法，每方法每场景设置各6个episode，共2x3x6=36 episode，结果在 ./drafts/exp_data-real.md（原 xlsx 已删，见下）；（0715 复查：tab:real_results 与数据均值逐格一致，正文数字一致）
   [x] 实验设置：室内环境尺寸参数、Stretch 3机器人平台（头部竖置Intel RealSense D435if+ReSpeaker 4ch MicArray V2用于导航，外部Intel RealSense D435i用于计算声音方向GT）、声源设置细节（便携音响播放数据集内声音...）、声源有tv doorbell conv. foot.；等等等等可能还有我没考虑到的；有条理地讲清楚
   [x] 对比仿真实验的简化：听觉感知模块只做声音类别识别，声音方向给GT
[x] (0715复查确认，已解决) exp_data-real.xlsx 疑似占位数据：已查明 episode 级数值系此前仓库 agent 整理时幻觉产生，不可信；作者人工逐值校对了各组最终均值，确认无误（与 tab:real_results 一致），实机结果可信任。均值已固化到 drafts/exp_data-real.md（含数据沿革说明），xlsx 已删除；episode 级原始数据在 Stretch 3 实机上，暂不便拷贝
[x] 生成实机仿真实验定性分析图 figures/exp-q-real.pdf
   [x] 更新前两张mix step，不要是1
[x] 实机定性分析需要读图理解（已插入 exp-q-real.pdf 并撰写定性小节与 caption）

[ignore] 数据集展示图片过时，要更新，以后再说

## 图片

[x] 完善2张定性分析图
[x] 术语格式check（0715 复查完成：exp-q-sim / exp-q-real / method 主体术语均与术语表一致，ImageBind 方向已正；遗留待改项见下）
   [x] dataset_stats 面板(d)：横轴 "distance to goal sound (m)" 与标注 "goal closer" → 改 "target sound"（caption 与术语表均用 target sound，goal 系近禁用变体）；面板(a)(c) 刻度 "Mixed Home" → 补全 "Mixed Home Activity"（0715 已重新出图，读图确认）
   [x] teaser 右下 footsteps 气泡病句 "should yield during when it detects" → "should yield when it detects"（0715 已改 pptx 重导出，读图确认）
   [x] method 图三个波形框的 c_aud 下标为斜体，与相邻 E_aud 元组的正体（\mathrm）下标不一致 → 统一为正体（0715 已改 pptx 重导出，读图确认）
[x] 数据集统计图 仿真分析图 实机分析图 检查caption（0715 复查：三条 caption 自洽、缩写各自展开、与图内容相符；结果表指标缩写不加表下注释系已记录的判断项，维持）
