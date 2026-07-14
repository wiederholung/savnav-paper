# TODO

## 数据集

[] 更新数据集表述，跟最新test_v6同步
[] 更新enmus专用数据集描述
[] 补充数据集统计图片
[] 补充新指标 Progress, STL

## 实验

[] 仿真实验最新结果以 ./drafts/exp_data-sim.md 为准(只报告SR到PSC的指标)，更新/重写所有相关内容
[] w/o tp anticip... 消融变体有调整，改为不计算任何视线外声音产生的cost，跟代码 no_audio_cost 对齐，但这个消融的名字不变
[] 仿真定性分析节插入新图 figures/exp-q-sim.pdf
[skip_need_human] 仿真定性分析需要读图分析重写，先跳过
[] 添加实机实验节，在los、nlos、mixed 3个设置下测了ours、ours_no_aud_cost 2个方法，每方法每场景设置各6个episode，共2x3x6=36 episode，结果在 ./drafts/exp_data-real.xlsx；
   [] 实验设置：室内环境尺寸参数、Stretch 3机器人平台（头部竖置Intel RealSense D435if+ReSpeaker 4ch MicArray V2用于导航，外部Intel RealSense D435i用于计算声音方向GT）、声源设置细节（便携音响播放数据集内声音...）、声源有tv doorbell conv. foot.；等等等等可能还有我没考虑到的；有条理地讲清楚
   [] 对比仿真实验的简化：听觉感知模块只做声音类别识别，声音方向给GT
[] 生成实机仿真实验定性分析图 figures/exp-q-real.pdf
   [x] 更新前两张mix step，不要是1
[skip_need_human] 实机定性分析需要读图理解，先跳过

[ignore] 数据集展示图片过时，要更新，以后再说

## 图片

[] 完善2张定性分析图
