# SAVNav Glossary

本文档是 SAVNav 论文的**唯一术语登记表**。它只维护三类内容：术语、缩写、数学符号。

- 术语写法与排版规范见 `.github/instructions/style.instructions.md`。
- 术语命名与禁用变体见 `.github/instructions/terminology.instructions.md`。
- 新术语、新缩写、新符号应先在此登记，再进入正文。
- 若正文、图注、表注与本表冲突，以本表为准，并回查相关章节统一修正。

## 1. Core Task and Entity Terms

| Term                            | Abbrev. | Definition (ZH)                                                    |
| :------------------------------ | :------ | :----------------------------------------------------------------- |
| SAVNav                          | SAVNav  | 整个 socially-aware audio-visual navigation 方法与系统             |
| the SAVNav task                 | -       | 论文定义的社会感知音视频导航任务与 benchmark                       |
| acoustic target                 | -       | 导航目标对应的发声对象，如 doorbell、calling、music、running water |
| social acoustic event           | -       | 由人类活动产生、需要建模为社会风险或交互边界的声音事件             |
| stationary conversational group | SCG     | 静态交谈群体，对应局部静态社会边界                                 |
| dynamic pedestrian              | DP      | 运动中的行人，对应动态风险区域                                     |
| social boundary                 | -       | 机器人应避免侵犯的社会边界                                         |
| line-of-sight                   | LOS     | 视距内、未被遮挡的视觉感知状态                                     |
| non-line-of-sight               | NLOS    | 非视距、被遮挡或尚未视觉确认的状态                                 |
| inferred entity                 | -       | 基于音频与拓扑信息推断出的实体                                     |

## 2. System Modules and Mechanisms

| Term                                    | Abbrev. | Definition (ZH)                                       |
| :-------------------------------------- | :------ | :---------------------------------------------------- |
| multi-modal perception                  | -       | 多模态感知模块，处理 RGB-D 与音频输入                 |
| acoustic-to-spatial social mapping      | SAVMap  | 将声学事件映射为可规划的空间社会结构                  |
| sparse audio-visual anchoring           | -       | 将声学事件与视觉实体进行稀疏稳定关联的机制            |
| anchoring confidence                    | -       | 衡量声学事件与视觉实体匹配强度的分数                  |
| topology-aware acoustic anticipation    | -       | 借助拓扑结构推断 NLOS 风险来源与位置的机制            |
| social cost field                       | -       | 将社会风险编码为空间连续代价场的表示                  |
| SAVNav policy                           | -       | 主动搜索与社会合规规划的决策模块                      |
| active sensory exploration              | -       | 为消除目标歧义而主动移动到有信息增益位置的行为        |
| target spatial belief map               | -       | 对 acoustic target 位置分布进行维护的空间 belief 表示 |
| socially-compliant precision navigation | -       | 在满足社会约束前提下执行精确到达的导航阶段            |

## 3. Perception and Representation Terms

| Term                            | Abbrev. | Definition (ZH)                      |
| :------------------------------ | :------ | :----------------------------------- |
| first-order Ambisonics          | FOA     | 一阶 Ambisonics 空间音频格式         |
| direction-of-arrival            | DOA     | 声源到达方向估计                     |
| azimuth / elevation             | -       | 方位角 / 俯仰角                      |
| confidence score                | -       | 置信度分数                           |
| joint embedding space           | -       | 跨模态语义对齐的联合嵌入空间         |
| depth projection                | -       | 利用深度图恢复三维位置的过程         |
| occlusion detection             | -       | 遮挡检测                             |
| segmentation mask               | -       | 实例分割掩码                         |
| spatial uncertainty             | -       | 视觉位置估计的不确定性               |
| angular uncertainty             | -       | 声学方向估计的不确定性               |
| cosine similarity               | -       | 语义相似性度量                       |
| angular deviation               | -       | 实体与 DOA 射线之间的角偏差          |
| topological node                | -       | 角点、门口、走廊交叉点等拓扑关键位置 |
| isotropic Gaussian              | -       | 各向同性高斯场                       |
| anisotropic Gaussian            | -       | 各向异性高斯场                       |
| longitudinal / lateral variance | -       | 纵向 / 横向方差                      |
| protective spear                | -       | 动态行人前向延展的风险形状           |

## 4. External Models and Platforms

| Term                                   | Abbrev. | Definition (ZH)                      |
| :------------------------------------- | :------ | :----------------------------------- |
| YOLO26                                 | -       | 视觉检测与实例分割模型               |
| ImageBind                              | -       | 统一多模态表征模型                   |
| embed-ACCDOA                           | -       | 开放词汇声事件定位与检测模型         |
| contrastive language-audio pretraining | CLAP    | 对比语言-音频预训练模型              |
| Habitat 3.0                            | -       | 3D 具身智能仿真平台                  |
| SoundSpaces 2.0                        | -       | 物理声学渲染平台                     |
| Fast Marching Method                   | FMM     | 用于异质代价场路径规划的快速推进方法 |
| Eikonal equation                       | -       | FMM 对应求解的方程                   |

## 5. Evaluation Terms

| Term                            | Abbrev. | Definition (ZH)    |
| :------------------------------ | :------ | :----------------- |
| success rate                    | SR      | 成功率             |
| success weighted by path length | SPL     | 路径长度加权成功率 |
| human collision rate            | HCR     | 人机碰撞率         |
| NLOS collision rate             | NCR     | 非视距碰撞率       |
| personal space violation        | PSV     | 个人空间侵犯率     |
| dynamic proxemics               | -       | 动态近体学约束     |
| static interaction zone         | -       | 静态交互区域约束   |

## 6. Mathematical Symbols

| Symbol                             | Meaning                                       |
| :--------------------------------- | :-------------------------------------------- |
| $\mathcal{E}$                      | 连续三维导航环境                              |
| $\mathcal{O}_{static}$             | 静态障碍物集合                                |
| $\mathcal{H}$                      | 动态人类集合                                  |
| $\mathbf{p}_{robot}^{(t)}$         | 机器人在时刻 $t$ 的位姿或位置状态             |
| $A_{target}$                       | acoustic target 对应的目标声事件              |
| $\mathbf{p}_{target}$              | 目标声源的真实位置                            |
| $d_{success}$                      | 判定成功的距离阈值                            |
| $O^{(t)}$                          | 时刻 $t$ 的多模态观测                         |
| $\mathbf{v}^{(t)}$                 | 机器人控制指令或速度命令                      |
| $\mathbf{p}_{vis}$                 | 视觉检测实体的三维位置                        |
| $\sigma_{vis}$                     | 视觉位置不确定性                              |
| $k_d, k_{occ}$                     | 深度项与遮挡项系数                            |
| $\gamma_{mask}$                    | 分割掩码占比                                  |
| $\theta_{azi}, \theta_{ele}$       | 声学 DOA 的方位角与俯仰角                     |
| $\sigma_{ang}$                     | 声学方向不确定性                              |
| $\mathbf{d}_{world}$               | 变换到世界坐标系的 DOA 方向向量               |
| $S_{anchor}^{(t)}(E_i)$            | 时刻 $t$ 对实体 $E_i$ 的 anchoring confidence |
| $sim$                              | 音频与视觉嵌入的余弦相似度                    |
| $\theta_{dev}$                     | 实体到 DOA 射线的角偏差                       |
| $\alpha$                           | anchoring 更新步长                            |
| $\tau_{anchor}, \tau_{deanchor}$   | anchoring / de-anchoring 迟滞阈值             |
| $\mathbf{p}_{inferred}$            | NLOS 推断位置                                 |
| $\mathbf{v}_{infer}$               | NLOS 动态行人的推断速度                       |
| $v_{walk}$                         | 参考人类行走速度                              |
| $C_{soc}(\mathbf{x})$              | 位置 $\mathbf{x}$ 处的社会代价                |
| $d_{long}, d_{lat}$                | 相对速度方向的纵向 / 横向距离                 |
| $\sigma_{long}, \sigma_{base}$     | 动态社会场纵向 / 基础尺度参数                 |
| $\mathcal{M}_{belief}(\mathbf{x})$ | target spatial belief map                     |
| $p_i, p^*$                         | 候选观察位姿 / 最优观察位姿                   |
| $U(p_i)$                           | 候选位姿的信息效用                            |
| $\mathcal{S}(p_i)$                 | 位姿 $p_i$ 的可见区域                         |
| $L(\cdot)$                         | 测地路径长度                                  |
| $\beta$                            | 探索收益与路径代价权衡系数                    |
| $S(\mathbf{x})$                    | FMM 规划使用的速度场                          |
| $S_{max}, S_{min}$                 | 速度场上界 / 下界                             |
| $w_{soc}$                          | 社会代价权重                                  |

## 7. Maintenance Notes

- 本表登记的是**主术语**，不是可自由替换的同义词集合。
- 若某术语需要新增别名、禁用变体或缩写边界，优先更新 `.github/instructions/terminology.instructions.md`，而不是在正文中临时处理。
- 若某符号只在局部小节出现但与全局符号系统可能冲突，也应先在此表核对是否已有占用。
