# SAVNav Glossary

本文档是 SAVNav 论文的**唯一术语登记表**。它只维护三类内容：术语、缩写、数学符号。

- 术语写法与排版规范见 .github/instructions/style.instructions.md。
- 术语命名与禁用变体见 .github/instructions/terminology.instructions.md。
- 新术语、新缩写、新符号应先在此登记，再进入正文。
- 若正文、图注、表注与本表冲突，以本表为准，并回查相关章节统一修正。

## 1. Ground Truth (GT) Layer (客观环境设定)

描述环境中客观存在的实体与事件设定。

| Term                            | Abbrev. | Definition (ZH)                                                                         |
| :------------------------------ | :------ | :-------------------------------------------------------------------------------------- |
| SAVNav                          | SAVNav  | 整个 socially-aware audio-visual navigation 任务、方法与系统的统称                      |
| embodied agent                  | -       | 具身智能体（任务定义阶段，泛指执行该类任务的 AI 系统）                                  |
| robot                           | -       | 机器人（方法与实验阶段，特指执行导航策略的实体，代表自我视角）                          |
| human actor                     | -       | 环境中客观存在的人类个体（符号 $h$），其行为模式必然隶属于 DP 或 SCG 两类之一           |
| static object                   | -       | 源于环境本身的静态物理对象（符号 $o$），如门、电视等，可作为目标声音的对应源            |
| acoustic target                 | -       | 指代导航最终目标                                                                        |
| sound event                     | -       | 客观发生的声音事件实例（符号 $a$），由 $h$ 或 $o$ 产生，其语义类别属于 target 或 social |
| target sound event              | -       | 声音类别的大类之一（类标属于 $\mathcal{L}_{\mathrm{target}}$的事件，全局至有且只有1个） |
| social sound event              | -       | 声音类别的大类之一（类标属于 $\mathcal{L}_{\mathrm{social}}$的事件）                    |
| stationary conversational group | SCG     | 静态交谈群体                                                                            |
| dynamic pedestrian              | DP      | 运动中的行人                                                                            |
| social boundary                 | -       | 机器人应避免侵犯的社会规矩边界                                                          |
| line-of-sight                   | LOS     | 视距内，指实体在视觉传感器的直接可视范围内                                              |
| non-line-of-sight               | NLOS    | 非视距，指实体被遮挡或尚未进入视觉传感器视野的状态                                      |

## 2. Perception Layer (感知层)

描述机器人通过传感器获得的观测以及实例化的感知实体。

| Term                   | Abbrev. | Definition (ZH)                                                   |
| :--------------------- | :------ | :---------------------------------------------------------------- |
| multi-modal perception | -       | 多模态感知模块，负责处理 RGB-D 与音频输入并提取实体               |
| multimodal observation | -       | 机器人在单个时间步周期内接收的多模态观测输入集合（RGB-D、音频等） |
| human entity           | -       | 视觉检测并跟踪的实例化人类（感知层概念，对应 $E_{\mathrm{hum}}$） |
| acoustic entity        | -       | 听觉定位并跟踪的实例化声音（感知层概念，对应 $E_{\mathrm{aud}}$） |
| first-order Ambisonics | FOA     | 一阶 Ambisonics 空间音频格式                                      |
| direction-of-arrival   | DOA     | 声音到达方向                                                      |
| cross-modal similarity | -       | 视觉与听觉嵌入特征之间的余弦相似度，用于衡量语义一致性            |
| depth projection       | -       | 将 2D 像素坐标与深度图结合，投影得到 3D 空间位置的过程            |

## 3. Mapping and Policy Layer (映射与策略层)

描述系统内部的核心机制、状态维护以及导航规划。

| Term                                 | Abbrev. | Definition (ZH)                                                    |
| :----------------------------------- | :------ | :----------------------------------------------------------------- |
| acoustic-to-spatial social mapping   | SAVMap  | 核心映射模块，负责将声学事件映射为可用于规划的连续空间代价场       |
| audio-visual anchoring               | -       | 将声学实体与视觉实体进行跨模态空时绑定的机制                       |
| anchoring confidence                 | -       | 衡量音视频实体绑定强弱、随时间更新的信度状态                       |
| topological node                     | -       | 环境拓扑图上的节点（如走廊拐角、门口），作为潜在的人类出现位置候选 |
| topology-aware acoustic anticipation | -       | 利用拓扑节点外推未见（NLOS）声音可能来源并评估风险的机制           |
| NLOS risk belief                     | -       | 维持在各个拓扑节点上、表示潜在未见风险强弱的信度状态               |
| social cost field                    | -       | 综合视距内外的社会规范约束，编码为空间中连续的代价场表示           |
| SAVNav policy                        | -       | 负责信息收集（主动探索）与路径生成（规避风险）的自主导航策略模块   |
| active sensory exploration           | -       | 机器人为寻找目标、消除歧义，主动规划并移动到高信息增益视点的行为   |
| target belief map                    | -       | 维护目标隐现位置概率分布的信念网格                                 |
| socially-compliant navigation        | -       | 在靠近目标的过程中，严格遵守所维护社会边界的空间路径规划行为       |

## 4. Evaluation Terms (评估指标)

| Term                            | Abbrev. | Definition (ZH)                                                    |
| :------------------------------ | :------ | :----------------------------------------------------------------- |
| success rate                    | SR      | 成功率（在无碰撞前提下，规定步数内抵达目标周围判定为成功的数据比） |
| success weighted by path length | SPL     | 考虑路径长度最优性的加权成功率                                     |
| human collision rate            | HCR     | 发生人机碰撞的 episode 比例                                        |
| NLOS collision rate             | NCR     | 视野内人类出现时间短于1秒（突发）导致的避让不及碰撞比例            |
| personal space compliance       | PSC     | 遵守个人空间规定（全程与人类保持安全距离以上）的时间步比例         |

## 5. External Models and Protocols (外部模型与方法)

| Term                                   | Abbrev. | Definition (ZH)                        |
| :------------------------------------- | :------ | :------------------------------------- |
| YOLO26                                 | -       | 视觉对象检测与实例分割模型             |
| ImageBind                              | -       | 统一多模态语义联合嵌入空间模型         |
| sound event localization and detection | SELD    | 声音事件定位与检测任务 / 框架          |
| embed-ACCDOA                           | -       | 开放词汇SELD模型，输出CLAP embedding   |
| contrastive language-audio pretraining | CLAP    | 音频与文本对齐的预训练模型             |
| Habitat 3.0                            | -       | 支持多智能体及物理交互的 3D 具身仿真器 |
| SoundSpaces 2.0                        | -       | 为3D环境提供实时动态几何音频渲染的平台 |
| Fast Marching Method                   | FMM     | -                                      |

## 6. Mathematical Symbols (数学符号)

为避免符号撞车与不规范排版，本项目的数学符号遵循以下学术规范：

1. **Set (集合)**：一律使用大写书法体，如 $\mathcal{E, H, O, A, N}$。
2. **Entity Instance (实体与元素)**：集合内的实体或元素实例一律采用小写斜体（如 $h_i \in \mathcal{H}, o_j \in \mathcal{O}, a_k \in \mathcal{A}$）。
3. **Vector (空间向量)**：在 3D 几何和特征空间中的向量，一律使用粗体小写（如 $\mathbf{p, d, v, e}$）。
4. **Field / State (状态与场)**：代价、速度、得分等标量场或状态维护量，采用大写/小写斜体，依据习惯划分以消除同一字母代指多类的歧义。

### 6.1 Spaces, Sets & Instances (集合与实体)

| Symbol                                                         | Meaning                                                                                                                        |
| :------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| $\mathcal{W}$                                                  | 连续的三维导航物理环境                                                                                                         |
| $\mathcal{M}_{\mathrm{nav}}, \mathcal{N}_{\mathrm{topo}}$      | 预加载的二维可行驶网格地图与拓扑节点集合                                                                                       |
| $\mathcal{H}, h_i$                                             | 人类参与者集合及其个体实例 ($h_i \in \mathcal{H}$)。其行为属于 DP 或 SCG                                                       |
| $\mathcal{O}, o_j$                                             | 静态物理对象集合及其实例 ($o_j \in \mathcal{O}$，如门、电视等对声音有掩蔽/声源作用的物理对象)                                  |
| $\mathcal{A}, a_k$                                             | 客观发生物理声音事件集合及其实例 ($a_k \in \mathcal{A}$)                                                                       |
| $\mathcal{L}_{\mathrm{target}}, \mathcal{L}_{\mathrm{social}}$ | 目标与社交类声音事件的语义类别标签集合 Label (剥离原先的区分与代价 Cost 撞车的 $\mathcal{C}$ 及与物理事件撞车的 $\mathcal{A}$) |
| $n_j, n^*$                                                     | 拓扑节点集合中的第 $j$ 个节点与目标/关键节点 ($n_j, n^* \in \mathcal{N}_{\mathrm{topo}}$)                                      |

### 6.2 Observations & Belief States (观测、感知与状态)

| Symbol                                            | Meaning                                                                                                                                         |
| :------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| $O^{(t)}$                                         | 时刻 $t$ 接收的多模态观测元组 $(I^{(t)}, D^{(t)}, A^{(t)})$ (注意：为 $O$ 斜体，严禁与物体集合 $\mathcal{O}$ 混淆)                              |
| $c_{\mathrm{aud}}^{(t)}$                          | 时刻 $t$ 声音类别的预测标签，$c_{\mathrm{aud}}^{(t)} \in \mathcal{L}_{\mathrm{target}} \cup \mathcal{L}_{\mathrm{social}}$                      |
| $E_{\mathrm{hum}}^{(t)}, E_{\mathrm{aud}}^{(t)}$  | **[感知]** 维护的 Perception Entity：时刻 $t$ 实例化持续追踪的视觉与听觉实体                                                                    |
| $B_{\mathrm{anch}}^{(t)}(E_{\mathrm{vis}}^{(t)})$ | **[映射]** (取代原 $S_{\mathrm{anch}}$) 刻画时刻 $t$ 实体绑定的锚定置信度状态，采用 $B$ (Belief) 防止与特征相似度 ($s$) 或规划速度场 ($S$) 混淆 |
| $B_{\mathrm{nlos}}^{(t)}(n_j)$                    | **[映射]** (取代原 $S_{\mathrm{nlos}}$) 维持在拓扑节点上的 NLOS 风险置信度状态                                                                  |
| $\lambda_{\mathrm{anch}}, \eta_{\mathrm{anch}}$   | 锚定信念或风险置信度更新过程中的自然衰减系数 (decay rate) 与观测更新率 (innovation rate)                                                        |
| $\tau_{\mathrm{anch}}, \tau_{\mathrm{nlos}}$      | 触发确立锚定关联或激活拓扑节点 NLOS 风险的判定阈值参数                                                                                          |

### 6.3 Spatial & Geometric Vectors (空间分布与几何特征向量)

| Symbol                                                                                        | Meaning                                                                                                                     |
| :-------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| $\mathbf{p}_{\mathrm{target}}, \mathbf{p}_{\mathrm{robot}}^{(t)}$                             | 目标真实 3D 位置，以及机器人在时刻 $t$ 的中心位置坐标                                                                       |
| $\mathbf{p}_{\mathrm{hum}}^{(t)}, \mathbf{p}_{\mathrm{obj}}$                                  | 时刻 $t$ 经深度图投影后获得的人类感知实体的 3D 中心坐标，与静态对象实体的 3D 坐标 (常量)                                    |
| $\mathbf{v}^{(t)}, \mathbf{v}_*^{(t)}$                                                        | 时刻 $t$ 机器人的底盘偏航/线速度控制指令 (输出)，及推测出的人类动态运动速度假设向量 (hypothesis)                            |
| $v_{\mathrm{walk}}$                                                                           | 标量形式的参考人类步行速率 (静态参考量，用于计算 $\mathbf{v}_*^{(t)}$)                                                      |
| $\mathbf{d}_{\mathrm{aud}}^{(t)}$                                                             | 时刻 $t$ 声学实体由于到达方向在世界坐标系下算出的方向向量 (DOA vector)                                                      |
| $\mathbf{e}_{\mathrm{hum}}^{(t)}, \mathbf{e}_{\mathrm{aud}}^{(t)}, \mathbf{e}_{\mathrm{obj}}$ | 经由时刻 $t$ 跨模态表征模型提取的视觉或听觉对象的语义级别嵌入向量 (对于静态物体 $\mathbf{e}_{\mathrm{obj}}$ 为全局给定常数) |
| $s^{(t)}$                                                                                     | 时刻 $t$ 特征端之间的余弦相似度 (cosine similarity，小写斜体独立使用)                                                       |
| $\sigma_{\mathrm{hum}}^{(t)}, \sigma_{\mathrm{aud}}^{(t)}$                                    | 时刻 $t$ 视觉深度定位带来的空间方差与声音 DOA 定位带来的角度不确定性误差                                                    |
| $\Delta\theta_{\mathrm{vis}}^{(t)}, \Delta\theta_j^{(t)}$                                     | 时刻 $t$ 视觉实体或拓扑节点相对于机器人的空间方向，与预测声音 DOA 射线之间的角度偏差                                        |

### 6.4 Cost & Planning Fields (连续场与规划代价)

| Symbol                                  | Meaning                                                                                                                         |
| :-------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| $C_{\mathrm{social}}^{(t)}(\mathbf{x})$ | 时刻 $t$ 综合的空间连续代价场 (social cost field)，含可见惩罚分量 $C_{\mathrm{los}}^{(t)}$ 与未见分量 $C_{\mathrm{nlos}}^{(t)}$ |
| $B^{(t)}(\mathbf{x})$                   | 时刻 $t$ 目标信念网格 (target belief map)，用于维护空域上目标隐现概率的对数赔率 (log-odds)                                      |
| $F(\mathbf{x}), F_{\max}, F_{\min}$     | (取代原 $S(\mathbf{x})$) FMM 前向波传播规划所用的可行驶速度场 (speed map)，采用 Fast Marching 标准                              |
| $U^{(t)}(\mathbf{p}_i)$                 | 时刻 $t$ 对候选视点 $\mathbf{p}_i$ 计算的综合主动探索效用得分 (utility score)                                                   |
| $T, d_{\mathrm{success}}$               | episode 最大时间步数；判断任务成功时，机器人与认定目标的静态距离阈值参数                                                        |

## 7. Maintenance Notes

- 本表登记的是**主术语**，不是可自由替换的同义词集合。
- 若某术语需要新增别名、禁用变体或缩写边界，优先更新 .github/instructions/terminology.instructions.md，而不是在正文中临时处理。
- 方法之后章节严格对齐术语表。
