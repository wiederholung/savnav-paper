# SAVNav 术语表与概念字典

本文档提取了 SAVNav 论文各个章节的关键术语、细粒度概念、模型、数据集和评测指标，全部采用分类建表的形式，供撰写、翻译和校对使用。

## 1. 核心概念与任务领域 (Core Concepts)

| 英文术语 (English Term)                         | 中文精炼描述                                       |
| :---------------------------------------------- | :------------------------------------------------- |
| Socially-Aware Audio-Visual Navigation (SAVNav) | 社会感知音视频导航（融合听视觉与社会规范）         |
| Embodied AI                                     | 具身智能（处于动态物理环境中的智能体）             |
| Multi-modal perception & fusion                 | 多模态感知与融合（音视频信息的对齐）               |
| Social norms & proxemics compliance             | 遵守社会规范与人际空间距离                         |
| Non-line-of-sight (NLOS) risk anticipation      | 非视距风险预判（听声辨位以防盲区碰撞）             |
| Real-time sensorimotor navigation               | 实时感知运动导航                                   |
| Social Navigation                               | 传统的社会导航（常依赖纯视觉，忽略声音盲区）       |
| Audio-Visual Navigation                         | 传统的音视频导航（视声音为纯几何目标，无社会语义） |
| ObjectNav / AudioGoal                           | 目标导航 / 音频目标导航（对比基准任务）            |

## 2. 多模态感知模块 (Multi-Modal Perception Layer)

| 英文术语 (English Term)              | 中文精炼描述                      |
| :----------------------------------- | :-------------------------------- |
| Direction of Arrival (DoA)           | 波达方向估计（声源到达方向）      |
| Azimuth / Elevation                  | 方位角 / 俯仰角                   |
| Confidence score                     | 置信度得分                        |
| Joint embedding space                | 联合嵌入空间（用于实现语义对齐）  |
| Depth projection                     | 深度投影（从RGB-D恢复3D空间位置） |
| Occlusion detection                  | 遮挡检测                          |
| Segmentation masks                   | 实例分割掩码                      |
| Spatial uncertainty ($\sigma_{vis}$) | 视觉空间不确定性                  |
| Angular uncertainty                  | 音频角度不确定性                  |

## 3. 声学-空间社会建图模块 (SAVMap)

| 英文术语 (English Term)                                  | 中文精炼描述                                      |
| :------------------------------------------------------- | :------------------------------------------------ |
| Acoustic-to-Spatial Social Mapping                       | 声学到空间的社会建图（SAVMap全称）                |
| Sparse Belief Anchoring                                  | 稀疏信念锚定机制                                  |
| Audio-to-entity mapping                                  | 声音到视觉实体的映射                              |
| Recursive belief score                                   | 递归信念得分（综合视觉声学的一致性）              |
| Cosine similarity / Angular deviation                    | 语义余弦相似度 / 空间角度偏差                     |
| Hysteresis thresholds ($\tau_{anchor}, \tau_{deanchor}$) | 迟滞阈值（防止频繁锚定/解除锚定）                 |
| Exponential decay                                        | 指数衰减（实体离开视野后的信念值衰减）            |
| Topology-Aware Hallucinated Momentum                     | 拓扑感知幻觉动量（处理视野外未看见的声源）        |
| Ray casting / NLOS event intersection                    | 射线投射 / 非视距事件声学交点                     |
| Virtual velocity ($\mathbf{v}_{virt}$)                   | 虚拟速度（推测行人的运动矢量）                    |
| Topological nodes                                        | 拓扑节点（如拐角、门口）                          |
| Anisotropic Social Cost Fields                           | 各向异性社会成本场                                |
| Isotropic / Anisotropic Gaussians                        | 各向同性（处理静止） / 各向异性高斯场（处理动态） |
| Longitudinal / Lateral variance                          | 纵向方差 / 侧向方差（定义高斯场形状）             |
| Protective spear                                         | 保护矛（动态行人前方延伸的惩罚区域形状）          |

## 4. 主动导航策略模块 (SAVNav Policy)

| 英文术语 (English Term)                                | 中文精炼描述                             |
| :----------------------------------------------------- | :--------------------------------------- |
| Proactive Socially-Aware Navigation                    | 主动社会感知导航（SAVNav Policy全称）    |
| Active Sensory Exploration                             | 主动感官探索（解决目标位置歧义）         |
| Information-theoretic viewpoint selection              | 信息论视角选择（最大化获取信息的收益）   |
| Information-theoretic utility                          | 信息论效用函数                           |
| Target belief map ($\mathcal{M}_{belief}(\mathbf{x})$) | 目标概率信念图                           |
| Socially-Compliant Precision Navigation                | 符合社会规范的精确导航                   |
| Fast Marching Method (FMM)                             | 快速推进算法（处理异质成本场的路径规划） |
| Eikonal equation                                       | 程函方程（通过其求解到达时间场）         |
| Speed field inversion                                  | 速度场求逆（结合社会成本进行换算）       |
| Arrival-time field / Gradient descent                  | 到达时间场 / 梯度下降求最优路径          |

## 5. 模型与架构 (Models & Architectures)

| 英文术语 (English Term) | 中文精炼描述                                |
| :---------------------- | :------------------------------------------ |
| YOLOv11                 | 视觉检测与实例分割模型（处理人类实体）      |
| ImageBind               | 统一特征提取模型（提取视觉实体语义）        |
| Embed-ACCDOA            | 声音定位与事件检测模型（输出听边定位结果）  |
| CLAP                    | 对比语言-音频预训练模型（提取音频语义特征） |
| First-order Ambisonics  | 一阶环境音效（支持声源定位的全景音频格式）  |

## 6. 环境、数据集与硬件 (Environments & Setup)

| 英文术语 (English Term) | 中文精炼描述                         |
| :---------------------- | :----------------------------------- |
| Habitat 3.0             | 3D具身智能仿真器（天然支持人类动态） |
| SoundSpaces 2.0         | 高保真物理声学渲染引擎               |
| Matterport3D (MP3D)     | 大规模3D室内场景数据集               |
| Stretch 3 Robot         | 实体测试运行的机器人平台             |

## 7. 评测场景与声学目标 (Scenarios & Targets)

| 英文术语 (English Term)               | 中文精炼描述                                              |
| :------------------------------------ | :-------------------------------------------------------- |
| Scene A: Crowded Social               | 人群拥挤场景（狭窄可见空间下的静态/动态避障）             |
| Scene B: Hidden Boundary              | 隐藏边界场景（典型未见其人先闻其声的盲区应对）            |
| Scene C: Mixed Home                   | 混合家庭场景（日常复杂环境综合评测）                      |
| Stationary Conversational Group (SCG) | 静态交谈群体（构成固定的互动成本区）                      |
| Dynamic Pedestrians (DP)              | 动态行人（产生移动的物理风险区）                          |
| Semantic targets                      | 导航的声学目标（Doorbell，Calling，Music，Running water） |
| Distractor social sounds              | 社会干扰声（如 Chat交谈声，Footsteps脚步声）              |

## 8. 评估指标 (Evaluation Metrics)

| 英文术语 (English Term)               | 中文精炼描述                                          |
| :------------------------------------ | :---------------------------------------------------- |
| Success Rate (SR)                     | 成功率（限定600步内，停在目标1.0米以内即算成功）      |
| Success weighted by Path Length (SPL) | 路径长度加权的成功率（评估路线是否为测地线最优）      |
| Human Collision Rate (HCR)            | 人机物理碰撞率                                        |
| NLOS Collision Rate (NCR)             | 非视距碰撞率（发生于视觉真正确认实体1.0秒之前的碰撞） |
| Personal Space Violation (PSV)        | 个人空间侵入率                                        |
| Dynamic proxemics                     | 动态人际距离限制（通常半径设定为 0.8 米）             |
| Static interaction zones              | 静态交互区限制（针对群体的半径 1.2 米）               |



## 9. 数学符号与定义 (Symbols & Mathematical Notations)

| 符号 (Symbol) | 中文精炼描述 |
| :--- | :--- |
| $\mathcal{E}$ | 连续3D导航环境 |
| $\mathcal{O}_{static}$ | 静态障碍物集合（如墙壁、家具） |
| $\mathcal{H}$ | 动态人类智能体集合 |
| $\mathbf{p}_{robot}^{(t)}$ | 机器人在 $t$ 时刻的三维位姿 |
| $A_{target}$ | 语义声学目标（领航终点声源） |
| $\mathbf{p}_{target}$ | 目标声源的真实物理坐标 |
| $d_{success}$ | 判定导航成功的最大距离阈值 |
| $O^{(t)}$ | $t$ 时刻的多模态观测数据（RGB图像、深度图、音频波形） |
| $\mathbf{v}^{(t)}$ | 机器人被期望输出的速度序列指令 |
| $\mathbf{p}_{vis}$ | 视觉模块检测到的行人三维物理位置 |
| $\sigma_{vis}$ | 视觉深度的空间不确定性得分 |
| $k_d, k_{occ}$ | 视觉空间不确定性相关的深度与遮挡方差缩放系数 |
| $\gamma_{mask}$ | 实例分割掩码占据的比例 |
| $\theta_{azi}, \theta_{ele}$ | 自我中心坐标系下的音频波达方向（方位角与俯仰角） |
| $\sigma_{ang}$ | 声学方向估计的角度不确定性 |
| $\mathbf{d}_{world}$ | 转换到全局世界坐标系下的音频方向向量 |
| $S_{belief}^{(t)}(E_i)$ | 将未知声学事件锚定到特定视觉实体 $E_i$ 上的稀疏信念得分 |
| $sim$ | 视觉与音频语义嵌入（Embedding）的余弦相似度 |
| $\theta_{dev}$ | 实体偏离音频 DoA 射线的角度偏差 |
| $\alpha$ | 锚定信念得分的更新步长大小 |
| $\tau_{anchor}, \tau_{deanchor}$ | 防止状态高频切换的锚定/解除锚定迟滞阈值 |
| $\mathbf{p}_{hallucinated}$ | 遇到墙壁阻挡后，检索出的盲区(NLOS)拓扑节点位置 |
| $\mathbf{v}_{virt}$ | 遇非视距情况时推测出的视野外行人“虚拟速度” |
| $v_{walk}$ | 假定的标准人类平均步行速度 |
| $C_{soc}(\mathbf{x})$ | 位置 $\mathbf{x}$ 处的连续社会风险成本场 |
| $d_{long}, d_{lat}$ | 距离行人运动速度向量方向的纵向与侧向距离 |
| $\sigma_{long}, \sigma_{base}$ | “保护矛”（动态社会场）的前向纵向方差与侧向基础方差 |
| $\mathcal{M}_{belief}(\mathbf{x})$ | 基于后验更新的目标概率信念图（用于解决方位歧义） |
| $p_i, p^*$ | 消除歧义用的候选探测视角 / 最终选定的最优视角 |
| $U(p_i)$ | 候选视角 $p_i$ 能带来的信息论效用收益函数 |
| $\mathcal{S}(p_i)$ | 从视角 $p_i$ 观察时处于可视范围内的视锥体区域 |
| $L(\cdot)$ | 两点间的测地线（导航最优）路径长度 |
| $\beta$ | 用于平衡“探索信息增益”与“行驶时间”的权重系数 |
| $S(\mathbf{x})$ | Fast Marching Method (FMM) 路径规划依靠的底层速度场 |
| $S_{max}, S_{min}$ | 基础设定的规划允许最大与最小速度 |
| $w_{soc}$ | 社会成本对应在速度场反演中的惩罚缩放权重 |
