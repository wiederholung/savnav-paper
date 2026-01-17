# SAVNav: Socially-Aware Audio-Visual Navigation

## 1. 术语与定义 (Terminology & Definitions)

### 1.1 时间与频率

- **Step (仿真步)**：仿真环境的最小离散时间单位。Agent 在每个 Step 接收一次观测并执行一次动作。
- **Update Delta (`update_dt`)**：仿真引擎每 Step 推进的物理时间，当前设定为 **0.048s**。
- **FPS (帧率)**：仿真运行的逻辑帧率，`FPS = 1 / update_dt ≈ 20.83 Hz`。
- **Module Frequency (模块频率)**：各子模块的运行间隔，例如视觉模块每 Step 运行 (20Hz)，音频模块每 0.5s 运行 (2Hz)。

### 1.2 坐标系 (Coordinate Systems)

- **World Frame (世界坐标系)**：
  - **原点**：场景中心。
  - **轴定义**：X-东, Y-上, Z-南。
  - **朝向 (Yaw)**：绕 Y 轴旋转，0° 面向 -Z (北)，逆时针为正。
- **Ego Frame (自我中心坐标系)**：
  - **原点**：机器人几何中心。
  - **轴定义**：X-右, Y-上, Z-后 (-Z 为前)。
  - **方位角 (Azimuth)**：绕 Y 轴旋转，0° 面向 -Z (前)，逆时针为正。
  - **仰角 (Elevation)**：绕 X 轴旋转，0° 为水平面，正值向上。

## 2. 系统架构 (System Architecture)

系统采用分层架构，主要包含三层：

1.  **感知层 (Perception Layer)**：负责多模态数据的采集、处理与初步抽象 (Visual Detection, SELD)。
2.  **建图层 (Mapping Layer - SAVMap)**：维护环境的时空表征，融合静态语义与动态视听信息。
3.  **规划层 (Planning Layer - SAVNav)**：基于 SAVMap 生成社交合规的导航动作。

### 2.1 设计规约

- **输入假设**：
  - 机器人：Stretch 3 构型 (RGB-D Camera + 4-Channel Mic Array + Odometry)。
  - 环境：室内场景，含少量动态人类 (≤5 人, 速度 ≤2m/s)。
  - 环境动态性假设：除人类 Agent 外，场景中的家具、结构等静态物体假设位置固定不变，不考虑家具搬动等情况。
  - 预置数据：已构建的静态语义地图 (Static Semantic Map)。
- **输出目标**：
  - 生成无碰撞、符合社交规范 (Socially Compliant)、满足自然语言指令的导航路径。

## 3. 感知层：多模态数据处理 (Perception Layer)

### 3.1 视觉感知 (Visual Perception)

- **运行频率**：1 Step (约 20.83 Hz)
- **功能**：检测视野内的人类并提取其三维空间与语义特征。

#### 数据流

1.  **输入**：RGB-D 图像 (1280×720, HFOV 87°, VFOV 56.19°)。
2.  **检测 (Detection)**：采用 **YOLOv11** 模型进行人体目标检测，生成 2D Bounding Box 和 Segmentation Mask。
3.  **状态估计 (State Estimation)**：
    - 利用 Depth 图像与 Mask 计算目标在 Ego Frame 下的坐标。
    - 变换至 World Frame，计算位置坐标 `(x, y, z)` 及位置不确定性 `position_uncertainty` ($\sigma_p$)。
      > **算法 3.1: 位置不确定性估计**
      > $$ \sigma_p = \sigma_{sensor} + \sigma_{occ} = (k_d \cdot z^2) + (k_{occ} \cdot (1 - \frac{N_{mask}}{N_{box}})) $$
      > 其中，$z$ 为目标深度，$k_d$ 为由深度相机特性决定的系数 (例如 0.005)，$k_{occ}$ 为遮挡惩罚系数，$N_{mask}/N_{box}$ 为分割区域占比（近似遮挡度）。
4.  **特征提取 (Feature Extraction)**：
    - **Visual Embedding**: 使用 **ImageBind** 提取视觉语义特征。
    - **ReID Embedding**: 提取外观特征用于帧间关联。

#### 输出结构 (VisualDetection)

```python
@dataclass
class VisualDetection:
    timestamp: float                  # 数据采集时间戳
    confidence: float                 # 检测置信度 [0, 1]
    box                               # 2D 边界框 xyxy
    mask                              # 2D 分割掩码 xy
    reid_embedding: np.ndarray        # 用于 ReID 的外观特征
    position: np.ndarray              # [x, y, z] World Frame
    position_uncertainty: float       # 位置估计标准差 (meters)
    visual_embedding: np.ndarray      # ImageBind 语义向量
```

### 3.2 听觉感知 (Audio Perception)

- **运行频率**：每 0.5s (约 2 Hz)
- **功能**：定位环境声源并识别其语义类别。

#### 数据流

1.  **输入**：4 通道一阶 Ambisonics 音频流 (24kHz)。
    - 通道定义：W (Omni), Y (+Up/-Down), Z (-Front/+Back), X (-Left/+Right).

2.  **SELD 推理 (Inference)**：
    - **缓冲机制 (Buffered Input)**: Habitat 每 Step 输出音频数据并存入缓冲区。音频模块每 0.5s 被唤醒一次，每次提取缓冲区中最近 5s 的数据作为输入。这种滑动窗口机制 (Sliding Window, Stride=0.5s) 确保了需输入长时序的模型能被周期性调用。
    - **模型调用**: 采用 **Embed-ACCDOA** 模型处理该 5s 音频窗口。
    - **输出**: 生成窗口内每帧 (0.1s/frame) 的 ACCDOA 向量与 CLAP 语义特征。推理结果同样存入结果缓冲区供下游模块异步获取。
3.  **后处理与映射 (Post-processing & Mapping)**：
    - **时间戳对齐**：计算事件发生时间 $T_{event} = T_{current} - 5.0s + n \cdot 0.1s$ ($n$ 为帧索引)。
    - **延迟分析**: 尽管输入窗口长达 5s，但由于窗口每 0.5s 滑动更新一次，且下游模块始终获取最近的推理结果，系统对声音事件的平均响应感知滞后 (Latency) 约为 0.5s (即更新周期)，而非 5s。
    - **语义分类与对齐**：
      - CLAP Matching: 将 CLAP 特征与预置文本原型对比，确定声音类别 (Label)。
      - Embedding Generation: 将 Label 输入 **ImageBind** 提取语义向量。
    - **空间变换与不确定性**：
      - 解析 ACCDOA 获取 Ego Frame 下的方位角/仰角：必须查询 $T_{event}$ 时刻的历史机器人位姿 $T_{robot}(t_{event})$ (而非当前位姿)，将 Ego Frame 坐标精确变换至 World Frame。
      - 生成世界坐标系下的声源不确定性参数。
        > **算法 3.2: 不确定性参数计算 (Uncertainty Parameters)**
        >
        > 1. **角度不确定性 ($\sigma_{ang}$)**:
        >    采用 Embed-ACCDOA 论文 reported 的定位误差作为基准 (e.g., $10^\circ \sim 20^\circ$)，并结合检测置信度 $c$ 进行动态缩放：
        >    $$ \sigma_{ang} = \sigma_{base} \cdot (1 + k_{unc} \cdot (1 - c)) $$
          >    其中 $c = \|\text{ACCDOA}\|$，$\sigma_{base}$ 为模型验证集平均误差。
        > 2. **距离不确定性 ($\sigma_{dist}$)**: 当前 SELD 模型无法进行距离估计，该项暂为开环参数 (设为 $R_{max}$)。

#### 输出结构 (AudioDetection)

```python
@dataclass
class AudioDetection:
    timestamp: float                  # 声音事件发生时间戳
    confidence: float                 # 检测置信度 [0, 1]
    doa: Tuple[float, float]          # (azimuth, elevation) Ego Frame
    agent_state: Dict[str, list]      # {"position": [x, y, z], "rotation": [w, x, y, z]}
    class_name: str                   # 声音类别 (e.g., "footstep")
    audio_embedding: np.ndarray       # ImageBind 语义向量
    uncertainty_params: Dict[str, float] # {azimuth_std, distance_std}
```

## 4. 建图层：社交视听地图 (SAVMap)

SAVMap 是感知的时空记忆容器，分辨率 grid_size=0.05m。

**数据输入 (Data Inputs)**:

- **感知层缓冲区 (Perception Buffer)**: 存储最近 $N=1000$ 条观测记录，包括 `VisualDetection` 和 `AudioDetection`。
- **静态语义地图 (Static Semantic Map)**: 场景初始化预加载的静态物体位置与语义信息。

### 4.1 核心数据结构

```python
class SAVMap:
    def __init__(self):
        self.resolution: float = 0.05
        self.layers: Dict[str, MapLayer] = {
            "static_semantic": StaticSemanticLayer(),  # 静态环境（墙、门、家具）
            "dynamic_visual": DynamicVisualLayer(),    # 视觉追踪的人类实体
            "dynamic_audio": DynamicAudioLayer(),      # 听觉定位的声源
            "social_cost": SocialCostLayer()           # 综合社交代价场
        }
```

### 4.2 图层详述

#### A. 静态语义层 (StaticSemanticLayer)

**内容**：预加载的不可移动物体。

```python
@dataclass
class StaticEntity:
    id: int
    category_name: str
    semantic_embedding: np.ndarray    # ImageBind 特征向量
    position: np.ndarray              # [x, y, z] 中心坐标
    obb: np.ndarray                   # 有向包围盒 (OBB)

class StaticSemanticLayer:
    navigable_map: np.ndarray         # 布尔矩阵 [H, W]，表示物理可达性
    obstacle_distance_field: np.ndarray # 浮点矩阵 [H, W]，到最近障碍物的欧氏距离
    static_entities: List[StaticEntity]
```

- **Navigable Map**: bool 矩阵，表示物理可达性。
- **Obstacle Distance Field**: float 矩阵，表示到最近障碍物的欧氏距离。
- **Static Entities**: 包含门、家具等静态对象，附带 ImageBind Embedding。

#### B. 动态视觉层 (DynamicVisualLayer)

**功能**：多目标跟踪 (MOT)。

```python
@dataclass
class VisualEntity:
    id: int                           # 唯一跟踪 ID
    class_name: str                   # e.g. "person"
    position: np.ndarray              # 滤波后的位置 [x, y, z]
    position_uncertainty: float       # 位置不确定性 (meters)
    velocity: np.ndarray              # 速度矢量 [vx, vy, vz]
    visual_embedding: np.ndarray      # 平滑后的 ImageBind 特征
    reid_embedding: np.ndarray        # 用于跟踪的外观特征
    confidence: float                 # 跟踪置信度 [0, 1]
    last_seen_timestamp: float        # 最后更新时间

class DynamicVisualLayer:
    entities: Dict[int, VisualEntity]
    next_id: int = 0
```

- **关联策略**：基于 Position (欧氏距离) 和 Embedding (余弦相似度) 的加权代价矩阵，使用匈牙利算法匹配。 
  > **算法 4.2: 混合关联代价 (Hybrid Cost)**
  > $$ C_{ij} = w_{pos} \cdot \frac{\| \mathbf{p}_i - \mathbf{p}_j \|}{d_{thres}} + w_{emb} \cdot (1 - \cos(\mathbf{e}_i, \mathbf{e}_j)) $$
  > 其中 $d_{thres} = 2.0m$ 为最大允许跃变距离。若 $C_{ij} > \text{Threshold}$ 则拒绝匹配。
- **状态更新**：
  - **位置滤波**：位置使用卡尔曼滤波 (Kalman Filter) 或滑动窗口平滑，减少检测噪声。
  - **特征更新 (Feature Update)**：采用置信度加权的移动平均 (EMA) 更新 Visual/ReID Embedding。
    > **算法 4.3: 视觉特征平滑**
    > $$ \mathbf{e}_{new} = \alpha \cdot \mathbf{e}_{obs} + (1 - \alpha) \cdot \mathbf{e}_{hist} $$
    > 其中更新系数 $\alpha$ 与当前帧检测置信度正相关 (e.g., $\alpha = 0.6 \cdot \text{conf}$)，确保高质量观测主导特征更新，适应视角变化。
  - **速度估计**：速度矢量 `velocity` 根据平滑轨迹的历史差分计算。
  - **置信度管理 (Confidence Management)**：
    - **匹配更新**: $C_{t} = \min(1.0, \beta \cdot C_{t-1} + (1 - \beta) \cdot C_{obs} \cdot (1 + \log(N_{match})))$。
      - 结合了**观测质量** ($C_{obs}$) 和**跟踪连续性** ($N_{match}$)。连续匹配次数越多，置信度累积越快且越稳定。
    - **未匹配衰减**: $C_{t} = C_{t-1} \cdot \lambda_{vis}$ (e.g., $\lambda_{vis} = 0.95$)。
      - 指数衰减，保留时间较长以应对视觉遮挡。
    - **清理**: 若 $C_t < T_{thres}$ (e.g. 0.1) 则移除实体。

#### C. 动态听觉层 (DynamicAudioLayer)

**功能**：声源持续追踪与视听融合。

```python
@dataclass
class AudioEntity:
    id: int                           # 唯一 ID
    class_name: str                   # e.g. "footstep"
    position_estimate: dict           # World Frame 方向锥 {origin, direction, aperture}
    associated_visual_id: Optional[int] # 关联的视觉实体 ID
    position: Optional[np.ndarray]    # 位置 [x, y, z] (若已关联或估算)
    hallucinated_velocity: Optional[np.ndarray] # 虚拟动量 [vx, vy, vz]
    position_uncertainty: Optional[float] # 位置不确定性 (meters)
    audio_embedding: np.ndarray       # 平滑后的特征
    confidence: float                 # 追踪置信度 [0, 1]
    last_heard_timestamp: float       # 最后听到时间

class DynamicAudioLayer:
    entities: Dict[int, AudioEntity]
```

- **关联策略 (Association)**：

  - 由于 SELD 仅输出帧级检测，需在层内进行跨时间窗口的实体维护。
  - **匹配准则**：基于 **DoA 角度距离** (优先) 和 **语义一致性** (辅助)。若新检测帧的 DoA 与现有声源偏差小于角度阈值 (e.g., $15^\circ$) 且语义标签相同，则关联为同一 **AudioEntity** ID。

- **视听融合 (AV-Fusion)**：
  - **关联逻辑**：若 AudioDetection 的 DoA 指向锥内存在语义匹配的 VisualEntity (如 "speech" match "person")。
    - **去歧义**：若锥内有多个候选视觉实体，选择与 DoA 射线角距离最小 (Nearest Neighbor) 且语义相似度最高的实体。
  - **融合操作 (Anchoring)**：将声源 **Anchor** 到视觉实体位置，`position_uncertainty` 也继承视觉实体的估计值，若是静态实体则为 0。此时 AudioEntity 实际上成为 VisualEntity 的一个属性。
  - **解锚机制 (De-anchoring)**：为了解决“离开视野后位置不可信”的问题，引入时效性检查。若关联的 VisualEntity 在 $T_{break}$ (e.g., 2.0s) 内未被重新观测到（即离开 FOV），系统强制断开锚定 (`associated_visual_id = None`)。
  - **状态回退**：解锚后的 AudioEntity 退化为 **Unanchored Audio**，其在 Social Cost Layer 中的表征自动从确定的高斯场切换回 **概率锥体场 (Probabilistic Cone Field)** 或虚拟动量场，以反映位置的不确定性。
  - **未锚定声音 (Unanchored Audio)**：若无视觉匹配或已解锚，保留纯听觉定位估计 `position_estimate`。
    - **拓扑感知虚拟动量 (Topology-Aware Hallucinated Momentum)**: 对于移动声源（如 "footstep"），执行 NLOS 预判：
      1.  **射线探测**: 沿 DoA 发出射线。
      2.  **拓扑吸附**: 若射线与墙壁相交，查询静态地图找到最近的**拓扑关键点**（如拐角点、门口中心），记为 $\mathbf{p}_{hallucinated}$。
      3.  **速度注入**: 赋予该虚拟实体一个指向机器人的速度矢量 $\mathbf{v}_{virt}$ ($|\mathbf{v}| \approx 1.2m/s$)，用于后续生成动态代价。
  - **状态标记**: 一旦 AudioEntity 被成功 Anchor 到 VisualEntity，该 AudioEntity 在后续规划中被标记为 **Merged**，不再独立参与 Costmap 计算，以避免双重惩罚。

- **状态更新 (State Update)**：
  - **时序聚合**：对连续关联到的声源位置 (DoA) 进行平滑，抑制单帧定位跳变。
  - **特征更新**：同样采用 EMA 策略更新 AudioEmbedding，使得特征向量能反映声源在时间维度上的变化 (如语调起伏)。
- **置信度管理 (Confidence Management)**：
  - **匹配更新**: $C_{t} = \min(1.0, \beta \cdot C_{t-1} + (1 - \beta) \cdot C_{obs} \cdot (1 + \log(N_{match})))$。
    - 同样结合 SELD 置信度和连续观测时长，但对 $C_{obs}$ 依赖更强。
  - **未匹配衰减**: $C_{t} = C_{t-1} \cdot \lambda_{audio}$ (e.g., $\lambda_{audio} = 0.8$)。
    - **快速衰减**：由于声源具有瞬态性且易受噪声干扰，$\lambda_{audio} < \lambda_{vis}$，使其能更快遗忘失效声源。
  - **清理**: 若 $C_t < T_{thres}$ (e.g. 0.1) 则移除实体。

#### D. 社交代价层 (SocialCostLayer)

**功能**：生成由人类活动引起的导航代价场 (Costmap)。

```python
class SocialCostLayer:
    cost_map: np.ndarray              # [H, W], 值域 [0, 1]
    last_update_time: float
```

**触发机制**：Event-Driven (当 Visual/Audio 层更新时触发)。

**代价模型 (Cost Models)**：

所有代价场的幅值 $A$ 与分布范围 $\sigma$ 均为动态参数，以反映感知的不确定性。

1.  **可见人类 (Visual Entities)**：
    
    - **参数定义**:
      - 幅值 $A = A_{base} \cdot C_{conf}$ (正比于检测置信度)。
      - 基础方差 $\sigma_{base} = \max(\sigma_{min}, k_{\sigma} \cdot \sigma_{pos})$ (正比于位置不确定性)。
    - **静态/观察中的人类**: 使用 **各向同性高斯 (Isotropic Gaussian)**，$\sigma = \sigma_{base}$。
    - **移动中的人类**: 使用 **非对称各向异性高斯 (Asymmetric Anisotropic Gaussian)**。仅沿速度方向 $\mathbf{v}$ 的前方进行延展。
      - $$ Cost_{vis}(\mathbf{x}) = A \cdot \exp \left( - \left( \frac{d_{long}^2}{2\sigma_{long}^2} + \frac{d_{lat}^2}{2\sigma_{base}^2} \right) \right) $$
      - 其中 $d_{long}$ 为位移矢量在 $\mathbf{v}$ 方向的投影距离。
        - 若 $d_{long} > 0$ (前方): $\sigma_{long} = \sigma_{base} \cdot (1 + k_{vel} \cdot \|\mathbf{v}\|)$ (延展程度正比于速度)。
        - 若 $d_{long} \le 0$ (后方): $\sigma_{long} = \sigma_{base}$ (不延展)。

2.  **未见移动声源 (Unseen Moving Sources)** (e.g., footstep only)：
    
    **Hearing before Seeing (NLOS Anticipation)** 的核心实现。
    - **输入**: $\mathbf{p}_{hallucinated}$ (源点), $\mathbf{v}_{virt}$ (虚拟速度), $\text{aperture}$ (源不确定性)。
    - **参数**:
      - 幅值 $A = A_{base} \cdot C_{conf}$。
      - 横向方差 $\sigma_{lat} = k_{lat} \cdot \text{aperture}$ (即声源定位的角度不确定性决定了长矛的粗细)。
    - **算法**: 生成沿虚拟速度方向（指向机器人）单向延伸的**非对称长矛状场**。
    - $$ Cost_{step}(\mathbf{x}) = A \cdot \exp \left( - \left( \frac{d_{long}^2}{2\sigma_{front}^2} + \frac{d_{lat}^2}{2\sigma_{lat}^2} \right) \right) \cdot \mathbb{I}(d_{long} > 0) $$
      - $\sigma_{front}$ 设定较大以覆盖潜在碰撞路径。
      - 仅在虚拟速度前方生效 ($\mathbb{I}(d_{long} > 0)$)，不惩罚墙后的“声源身后”区域。

3.  **未见静止声源 (Unseen Stationary Sources)** (e.g., speech)：
    
    - **输入**: 声源 DoA 锥体 $\mathcal{C}_{audio}$。
    - **算法**: **动态概率锥体场 (Dynamic Probabilistic Cone Field)**。
    - $$ Cost_{speech}(\mathbf{x}) = \mathbb{I}(\mathbf{x} \in \Omega_{cone}) \cdot \frac{A_{base} \cdot C_{conf}}{1 + \gamma \cdot \|\mathbf{x} - \mathbf{p}_{source}\|} \cdot \exp\left(-\frac{\theta_{dev}^2}{2\sigma_{aperture}^2}\right) $$
    - **参数**:
        - 幅值 $A = A_{base} \cdot C_{conf}$。
        - 角度分布方差 $\sigma_{aperture} = k_{ang} \cdot \text{aperture}$。
    - **效果**: 形成一个随距离衰减且边缘模糊的扇形斥力场。
4.  **目标豁免 (Target Immunity)**：
    - 若某个实体（Visual 或 Audio）被识别为当前的导航目标（Target），则其产生的 Social Cost 将被**掩码屏蔽 (Masked)** (强制置为 0)。这防止了导航目标本身产生排斥力导致机器人无法靠近。

5.  **聚合 (Aggregation)**：
    - 按权重叠加所有代价场并归一化。
    - **Geodesic Constraints**：使用测地距离传播代价，防止穿墙效应。

## 5. 规划层：SAVNav 规划器 (Planning Layer)

引入双模式状态机，解决“查不准”的问题，在“精确导航”与“主动搜索”模式间动态切换。

任务假设：查询一定包含声音描述（显式或隐式）。

### 5.1 目标仲裁与状态机 (Target Arbitration & State Machine)

1.  **查询解析 (Query Parsing)**:
    - MLLM 解析用户指令 $\rightarrow$ Query $\langle \text{Content}, \text{Modality} \rangle$ (e.g., "Help", "Audio").
2.  **实体匹配 (Entity Matching)**:
    - 在 SAVMap 各层搜索匹配实体。
    - **Visual/Static Layer**: 计算 Embedding 余弦相似度。
    - **Audio Layer**: 计算 DoA 方向匹配度。
3.  **状态仲裁 (State Arbitration)**:
    - **State A (Precision Nav)**:
      - 条件: 目标已锚定视觉实体 (`associated_visual_id != None`)。
      - 行为: 规划至明确的坐标点 $\mathbf{x}_{goal}$。
    - **State B (Active Search)**:
      - 条件: 目标仅匹配到 Audio Entity 且未锚定 (`associated_visual_id == None`)，即“只闻其声，不见其人”。
      - 行为: 基于目标信念图 (Belief Map) 规划视点，最大化目标发现概率，试图将目标转化为 Visual Entity。

### 5.2 状态 A: 精确导航 (Precision Navigation)

**目标**: 前往确定的目标坐标 $\mathbf{x}_{goal} = \mathbf{p}_{entity}$。

**算法**: **快速行进法 (FMM)**
将路径规划建模为非均匀介质中的波传播问题。

1.  **速度场构建 (Speed Map)**：
    - $S(\mathbf{x}) = S_{max} \cdot (1 - w_{soc} \cdot \text{clip}(C_{social}(\mathbf{x}), 0, 1)) + S_{min}$。
    - 引入 $S_{min}$ (e.g., $0.1 \cdot S_{max}$) 确保即使在高代价区域（如人群密集处），只要物理可通行，目标依然在数学上可达（避免 Soft Cost 变为 Hard Obstacle）。
    - 结合了上一节定义的**各向异性 NLOS 代价**，使得波传播自动避开潜在危险区（如拐角内侧）。
2.  **到达时间场求解 (Eikonal Equation)**：
    - 求解 $\| \nabla T(\mathbf{x}) \| \cdot S(\mathbf{x}) = 1$，得到 $T(\mathbf{x})$ 场。
3.  **梯度下降 (Gradient Descent)**：
    - $\mathbf{x}_{next} = \mathbf{x}_{curr} - \delta \cdot \nabla T(\mathbf{x}_{curr})$。生成平滑且合规的轨迹。

### 5.3 状态 B: 主动视听搜索 (Active Audio-Visual Search)

**目标**: 最大化利用听觉线索发现目标的概率 (Probability of Detection)，解决“环境空间已知但目标位置未知”的搜索问题。

**算法**: **基于信念图的主动搜索 (Belief-Driven Active Search)**

#### 1. 动态目标信念图 (Target Belief Map)

系统维护一个与栅格地图同分辨率 (0.05m) 的概率分布图 $\mathcal{M}_{belief}$，用于表征目标在环境中存在的空间后验概率。

-   **数据结构**: 二维浮点矩阵，值域 $[0, 1]$。
-   **初始化**: 全局初始化为低均匀概率 $P_{init}$。
-   **听觉更新 (Audio Positive Update)**:
    获取由 5.1 节锁定的目标 `AudioEntity`，提取其 `position_estimate` 属性（包含原点、主方向、张角）生成声源不确定性锥体，在声源方向锥内注入概率质量。
    $$ \mathcal{M}_{belief}^{(t)}(c) = \text{clip}(\mathcal{M}_{belief}^{(t-1)}(c) + \alpha_{audio} \cdot G(c \mid \Omega_{ROI}), 0, 1) $$
    其中 $G(\cdot)$ 为以声源射线为中心的 2D 高斯分布衰减函数，$\Omega_{ROI}$ 为声源不确定性锥体与可通行区域的交集。
-   **视觉更新 (Visual Negative Information)**:
    当相机视场扫过某区域 $c$ 且检测器未输出目标时，根据“未观测到”这一事实降低信念值。
    $$ \mathcal{M}_{belief}^{(t)}(c) = \mathcal{M}_{belief}^{(t-1)}(c) \cdot \lambda_{neg} \quad \text{if } c \in \text{FOV}_{free} $$
    其中 $\lambda_{neg} \in (0, 1)$ 为遗忘因子 (e.g., 0.3)，$\text{FOV}_{free}$ 表示当前相机视锥体内的无遮挡区域。

#### 2. 增强型候选视点生成 (Enhanced Candidate Viewpoint Generation)

构建候选视点集 $\mathcal{P} = \{p_1, p_2, \dots, p_N\}$，涵盖长距离导航点与局部姿态调整点：

1.  **拓扑节点 (GVD Nodes)**: 来源于静态地图的广义 Voronoi 图节点，提供全局视野。
2.  **ROI 区域采样 (ROI-Guided Sampling)**:
    直接在声源不确定性锥体与可通行地图的交集 $\Omega_{ROI}$ 及其周边进行均匀采样。
    -   **算法**: 在 $\Omega_{ROI}$ 区域内生成栅格采样点 $\{s_1, \dots, s_k\}$，并滤除离最近障碍物距离小于 $d_{safe}$ 的点。
    -   **作用**: 弥补 GVD 节点的稀疏性。如果声源位于房间深处的角落，GVD 节点（通常在房间中心）可能无法提供清晰视线，此策略允许 Agent 深入目标区域进行确认。
3.  **原地重定位采样 (In-situ Reorientation)**:
    在机器人当前位置 $R_{local}$ (e.g., 0.5m) 范围内采样，并强制生成指向 $\mathcal{M}_{belief}$ 峰值方向的偏航角 (Yaw)。
    -   **目的**: 允许 Agent 执行低代价的原地旋转或微调，以解决“刚经过声源但视场未覆盖”的问题，避免舍近求远。

#### 3. 信息论效用评估 (Information-Theoretic Utility Evaluation)

对每个候选视点 $p_i$ 进行评分，旨在最大化**有效观测范围内**的目标发现期望，同时最小化移动代价。

$$ U(p_i) = \mathcal{I}_{gain}(p_i) - \beta \cdot \mathcal{C}_{cost}(p_i) $$

**A. 期望观测收益 ($\mathcal{I}_{gain}$)**

$$ \mathcal{I}_{gain}(p_i) = \sum_{c \in \mathcal{S}(p_i)} \left[ \mathcal{M}_{belief}(c) \cdot \text{Vis}(p_i, c) \cdot \gamma(\| c - p_i \|) \right] $$

**符号定义**:
*   $\mathcal{S}(p_i)$: 候选视点 $p_i$ 的相机视锥体 (Frustum) 在栅格地图上的投影区域。
*   $\text{Vis}(p_i, c)$: **可见性检查函数** (Ray-casting)。若从 $p_i$ 到栅格中心 $c$ 的连线无障碍物阻挡，则为 1，否则为 0。此步骤解决了仅检测 ROI 几何中心导致的鲁棒性问题。
*   $\gamma(d)$: **分辨率/距离衰减因子** (Resolution Decay Factor)。
    $$ \gamma(d) = \exp \left( - \frac{d^2}{2\sigma_{sensor}^2} \right) \cdot \mathbb{I}(d < R_{max}) $$
    -   **作用**: 模拟传感器在远距离下的检测能力下降，并引入硬截断 $R_{max}$ (e.g. 5.0m)。
    -   **数学修正**: 此项抑制了 Agent 为了最大化投影面积 $Area \propto d^2$ 而无限后退的行为，迫使 Agent 选择“既能看到 ROI 又处于有效检测距离内”的位置。

**B. 移动代价 ($\mathcal{C}_{cost}$)**

$$ \mathcal{C}_{cost}(p_i) = \frac{L(\mathbf{p}_{robot}, p_i)}{v_{avg}} + \frac{|\Delta \theta|}{w_{avg}} $$

**符号定义**:
*   $L(\cdot)$: 测地距离 (Geodesic Distance)，即通过 FMM 计算的实际路径长度。
*   $\Delta \theta$: 需要旋转的角度差。
*   $\beta$: 调节搜索收益与时间成本的权重系数。

#### 4. 决策

选择 $p^* = \arg\max_{p \in \mathcal{P}} U(p)$ 作为局部导航目标 $\mathbf{x}_{search}$。
    -   若 $p^*$ 为原地旋转点，则直接下发 Velocity Command。
    -   若 $p^*$ 为远端点，则调用 Planner 生成路径。

### 5.4 状态转换逻辑 (State Transition Logic)

- **B $\rightarrow$ A (Capture)**: 当前目标的 Audio Entity 的 `associated_visual_id != None`
- **A $\rightarrow$ B (Lost)**: 当前目标的 Audio Entity 的 `associated_visual_id == None`

### 5.5 反应式控制 (Reactive Control)

- **Emergency Stop**: 若检测到 Dynamic Obstacle 的 TTC (Time-To-Collision) < 1.0s，立即制动。
