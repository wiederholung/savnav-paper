# SAVNav: Socially-Aware Audio-Visual Navigation

## 1. 术语与定义 (Terminology & Definitions)

### 1.1 时间与频率

- **Step (仿真步)**：仿真环境的最小离散时间单位。Agent 在每个 Step 接收一次观测并执行一次动作。
- **Update Delta (`update_dt`)**：仿真引擎每 Step 推进的物理时间，当前设定为 **0.048s**。
- **FPS (帧率)**：仿真运行的逻辑帧率，`FPS = 1 / update_dt ≈ 20.83 Hz`。
- **Module Frequency (模块频率)**：视觉模块和音频模块均每 Step 运行 (约 20.83 Hz)，保持同步。

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

### 1.3 坐标变换公式 (Coordinate Transformations)

#### Ego Frame → World Frame

给定传感器在世界坐标系下的位置 $\mathbf{t}_{sensor} = [t_x, t_y, t_z]^T$ 和旋转四元数 $q = (w, x, y, z)$：

1. **构建旋转矩阵** $\mathbf{R}$：
   $$ \mathbf{R} = \begin{bmatrix} 1-2(y^2+z^2) & 2(xy-wz) & 2(xz+wy) \\ 2(xy+wz) & 1-2(x^2+z^2) & 2(yz-wx) \\ 2(xz-wy) & 2(yz+wx) & 1-2(x^2+y^2) \end{bmatrix} $$

2. **世界坐标计算**：
   $$ \mathbf{p}_{world} = \mathbf{R} \cdot \mathbf{p}_{ego} + \mathbf{t}_{sensor} $$

#### 图像坐标 → Ego Frame (反投影)

给定像素坐标 $(u, v)$、深度值 $Z$、相机内参 $(f_x, f_y, c_x, c_y)$：

$$ x_{ego} = \frac{(u - c_x) \cdot Z}{f_x}, \quad y_{ego} = -\frac{(v - c_y) \cdot Z}{f_y}, \quad z_{ego} = -Z $$

> **注意**：$y$ 和 $z$ 的负号源于图像坐标系 (v 向下) 与 Ego Frame (Y 向上, -Z 向前) 的差异。

#### DoA (Ego Frame) → World Frame 方向向量

给定 Ego Frame 下的 DoA $(\theta_{azi}, \theta_{ele})$：

1. **Ego Frame 方向向量**：
   $$ \mathbf{d}_{ego} = [\sin(\theta_{azi}) \cos(\theta_{ele}), \sin(\theta_{ele}), -\cos(\theta_{azi}) \cos(\theta_{ele})]^T $$

2. **World Frame 方向向量**：
   $$ \mathbf{d}_{world} = \mathbf{R} \cdot \mathbf{d}_{ego} $$

## 2. 系统架构 (System Architecture)

系统采用分层架构，主要包含三层：

1.  **感知层 (Perception Layer)**：负责多模态数据的采集、处理与初步抽象 (Visual Detection, SELD)。
2.  **建图层 (Mapping Layer - SAVMap)**：维护环境的时空表征，融合静态语义与动态视听信息。
3.  **规划层 (Planning Layer - SAVNav)**：基于 SAVMap 生成社交合规的导航动作。

### 2.1 设计规约

- **输入假设**：
  - 机器人：Stretch 3 构型 (RGB-D Camera + 4-Channel Mic Array + Odometry)。
  - 环境：室内场景，含少量动态人类 (≤5 人, 速度 ≤2m/s)。
  - 环境动态性假设：除人类 Agent 外，场景中的家具、结构等静态物体假设位置固定不变。
  - 预置数据：已构建的静态语义地图 (Static Semantic Map)。
  - 视觉检测假设：假设 YOLO 能完美处理遮挡情况，不考虑人类遮挡导致的检测失败。

- **任务定义**：
  - **目标**：根据自然语言指令，导航至发出特定声音的目标位置。
  - **声音类别** (共 6 类)：
    | 类型 | class_name | 声源实体 | 说明 |
    |:---:|:---:|:---:|:---|
    | 目标 | doorbell | StaticEntity (door) | 门铃声 |
    | 目标 | help | VisualEntity (静止人类) | 呼唤声 |
    | 目标 | music | StaticEntity (tv_monitor) | 音乐声 |
    | 目标 | water | StaticEntity (sink) | 流水声 |
    | 干扰 | chat | VisualEntity (静止人类) | 聊天声 |
    | 干扰 | footstep | VisualEntity (移动人类) | 脚步声 |
  - **声源特性**：所有目标声音持续 (间隔) 循环播放，不存在声源永久消失的情况。

- **输出目标**：
  - 生成无碰撞、符合社交规范 (Socially Compliant) 的导航路径，最终到达目标声源位置。

## 3. 感知层：多模态数据处理 (Perception Layer)

### 3.1 视觉感知 (Visual Perception)

- **运行频率**：1 Step (约 20.83 Hz)
- **功能**：检测视野内的人类并提取其三维空间与语义特征。

#### 数据流

1.  **输入**：RGB-D 图像 (1280×720, HFOV 87°, VFOV 56.19°)。
2.  **检测 (Detection)**：采用 **YOLOv11** ([checkpoints](../data/checkpoints/ultralytics/yolo/)) 模型进行人体目标检测，生成 2D Bounding Box 和 Segmentation Mask。
3.  **状态估计 (State Estimation)**：
    - 利用 Depth 图像与 Mask 计算目标在 Ego Frame 下的坐标。
    - 变换至 World Frame (参考 [mask_to_world_coords.ipynb](../tests/utils/mask_to_world_coords.ipynb))，计算位置坐标 `(x, y, z)` 及位置不确定性 `position_uncertainty` ($\sigma_p$)。
      > **算法 3.1: 位置不确定性估计**
      > $$ \sigma_p = \sigma_{sensor} + \sigma_{occ} = (k_d \cdot z^2) + (k_{occ} \cdot (1 - \frac{N_{mask}}{N_{box}})) $$
      > 其中，$z$ 为目标深度，$k_d$ 为由深度相机特性决定的系数 (例如 0.005)，$k_{occ}$ 为遮挡惩罚系数，$N_{mask}/N_{box}$ 为分割区域占比（近似遮挡度）。
4.  **特征提取 (Feature Extraction)**：
    - **Visual Embedding**: 使用 **ImageBind** 提取视觉语义特征。

#### 输出结构 (VisualDetection)

```python
@dataclass
class VisualDetection:
    timestamp: float                  # 数据采集时间戳
    confidence: float                 # 检测置信度 [0, 1]
    box                               # 2D 边界框 xyxy
    mask                              # 2D 分割掩码 xy
    reid_embedding: np.ndarray        # 用于 ReID 的外观特征 (原型阶段为 None)
    position: np.ndarray              # [x, y, z] World Frame
    position_uncertainty: float       # 位置估计标准差 (meters)
    visual_embedding: np.ndarray      # ImageBind 语义向量
```

最后输出 List[VisualDetection]，len(list) = 当前帧检测到的数量。

### 3.2 听觉感知 (Audio Perception)

- **运行频率**：每 0.5s (约 2 Hz)
- **功能**：定位环境声源并识别其语义类别。

#### 数据流

1.  **输入**：4 通道一阶 Ambisonics 音频流 (24kHz)，N3D 归一化，每次输入前 update_dt 秒 (0.048s) 音频。

    一直是世界坐标系下的 Ambisonics 编码，不是 Ego Frame 下的。定义如下：
    
    | Channel Index | ACN | 球谐函数分量        | 方向意义 (在 Y-Up, -Z 正前方坐标系) |
    | ------------- | --- | ------------------- | ----------------------------------- |
    | 0             | 0   | W (omnidirectional) | 全向分量                            |
    | 1             | 1   | Y                   | 沿 Y 轴（向上）                     |
    | 2             | 2   | Z                   | 沿 Z 轴（向后，因为 -Z 是正前方）   |
    | 3             | 3   | X                   | 沿 X 轴（向右）                     |

2.  **SELD 推理 (Inference)**：
    - **缓冲机制 (Buffered Input)**: Habitat 每 Step 输出音频数据并存入缓冲区。音频推理模块每 0.5s 被唤醒一次，每次提取缓冲区中最近 2.55s 的数据作为输入。这种滑动窗口机制 (Sliding Window, Stride=0.5s) 确保了需输入长时序的模型能被周期性调用。
    - **模型调用**: 采用 **Embed-ACCDOA** 模型处理该 2.55s 音频窗口。
    - **输出**: 生成窗口内每帧 (0.1s/frame) 的 ACCDOA 向量与 CLAP 语义特征。推理结果同样存入结果缓冲区供下游模块异步获取。
3.  **后处理与映射 (Post-processing & Mapping)**：
    - **时间戳对齐**：计算事件发生时间 $T_{event} = T_{current} - 2.55s + n \cdot 0.1s$ ($n$ 为帧索引)。
    - **延迟分析**: 尽管输入窗口长达 2.55s，但由于窗口每 0.5s 滑动更新一次，且下游模块始终获取最近的推理结果，系统对声音事件的平均响应感知滞后 (Latency) 约为 0.5s (即更新周期)，而非 2.55s。
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
    semantic_embedding: np.ndarray    # ImageBind 特征向量 跟据 category_name 计算
    position: np.ndarray              # [x, y, z] 中心坐标
    obb: habitat_sim._ext.habitat_sim_bindings.OBB # 有向包围盒 (OBB)

class StaticSemanticLayer:
    navigable_map: np.ndarray         # 布尔矩阵 [H, W]，表示物理可达性
    obstacle_distance_field: np.ndarray # 浮点矩阵 [H, W]，到最近障碍物的欧氏距离
    topology_nodes: np.ndarray        # 拓扑点坐标 [N, 2]，XZ 平面投影 (忽略高度)
    static_entities: List[StaticEntity]
```

- **Navigable Map**: bool 矩阵，表示物理可达性。
- **Obstacle Distance Field**: float 矩阵，表示到最近障碍物的欧氏距离。
- **Topology Nodes**: 预计算的拓扑点（拐角、门口、走廊交叉点等），用于规划层候选视点生成和 NLOS 拓扑吸附。
- **Static Entities**: 包含门、家具等静态对象，附带 ImageBind Embedding。

注意：

- 地图加载方法见 [read_semantic_data.ipynb](../tests/utils/map/read_semantic_data.ipynb)
- 拓扑点预计算参考 [get_wall.ipynb](../tests/utils/map/get_wall.ipynb)
- 获取静态实体的id、category_name、position（世界坐标）、obb方法见 [plg_avh.ipynb](../tests/plg_avh.ipynb)

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
    reid_embedding: np.ndarray        # 用于跟踪的外观特征 (原型中设为 None)
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
  > 将emb权重设小点(因为visual_embedding用于匹配没那么准)。
- **状态更新**：
  - **位置滤波**：位置使用卡尔曼滤波 (Kalman Filter) 或滑动窗口平滑，减少检测噪声。
  - **特征更新 (Feature Update)**：采用置信度加权的移动平均 (EMA) 更新 Visual Embedding。
    > **算法 4.3: 视觉特征平滑**
    > $$ \mathbf{e}_{new} = \alpha \cdot \mathbf{e}_{obs} + (1 - \alpha) \cdot \mathbf{e}_{hist} $$
    > 其中更新系数 $\alpha$ 与当前帧检测置信度正相关 (e.g., $\alpha = 0.6 \cdot \text{conf}$)，确保高质量观测主导特征更新，适应视角变化。
  - **速度估计**：速度矢量 `velocity` 根据平滑轨迹的历史差分计算。
  - **置信度管理 (Confidence Management)**：
    - **匹配更新**: $C_{t} = \min(1.0, \beta \cdot C_{t-1} + (1 - \beta) \cdot C_{obs} \cdot (1 + \log(1 + N_{match})))$。
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
    associated_visual_id: Optional[int] # 关联的动态视觉实体 ID (人类)
    associated_static_id: Optional[int] # 关联的静态实体 ID (door/tv_monitor/sink)
    position: Optional[np.ndarray]    # 位置 [x, y, z] (若已关联或估算)
    hallucinated_velocity: Optional[np.ndarray] # 虚拟动量 [vx, vy, vz]
    position_uncertainty: Optional[float] # 位置不确定性 (meters)
    audio_embedding: np.ndarray       # 平滑后的特征
    confidence: float                 # 追踪置信度 [0, 1]
    last_heard_timestamp: float       # 最后听到时间

class DynamicAudioLayer:
    entities: Dict[int, AudioEntity]
```

**position_estimate 计算**：由 `AudioDetection` 的 `doa`、`agent_state`、`uncertainty_params` 综合计算：
```python
position_estimate = {
    "origin": agent_state["position"],           # 机器人位置 (World Frame)
    "direction": doa_to_world(doa, agent_state), # DoA 转换为世界方向向量 (见 1.3 节)
    "aperture": uncertainty_params["azimuth_std"] # 张角 = 方向角不确定性 (°)
}
```

其中 `doa_to_world()` 使用 1.3 节公式，将 Ego Frame 下的 $(\theta_{azi}, \theta_{ele})$ 先转换为方向向量 $\mathbf{d}_{ego}$，再通过 $\mathbf{R}$ 旋转得到 $\mathbf{d}_{world}$。

- **关联策略 (Association)**：

  - **匹配准则**：基于 **DoA 角度距离** (优先) 和 **语义一致性** (辅助)。若新检测帧的 DoA 与现有声源偏差小于角度阈值 (e.g., $15^\circ$) 且语义标签相同，则关联为同一 **AudioEntity** ID。

- **视听融合 (AV-Fusion)**：

  **声音类别及锚定规则**：见 **2.1 任务定义** 中的声音类别表。

  - **锥体范围检查**：计算实体位置与 DoA 主方向的夹角 $\theta_{dev}$，若 $\theta_{dev} < \text{aperture}/2$ 则认为实体在锥内。
  - **关联逻辑**：若 AudioDetection 的 DoA 指向锥内存在符合条件的实体：
    - **静态实体匹配**：计算 `audio_embedding` 与 `static_entity.semantic_embedding` 的余弦相似度，阈值 $\tau_{static}$ (e.g., 0.6)。
    - **动态人类匹配**：
      - `footstep` → 仅锚定 $\|\mathbf{v}\| \ge v_{thres}$ (e.g., 0.3m/s) 的移动人类。
      - `help` / `chat` → 仅锚定 $\|\mathbf{v}\| < v_{thres}$ 的静止人类。
    - **去歧义**：若锥内有多个候选实体，选择与 DoA 射线角距离最小 (Nearest Neighbor) 的实体。
  - **融合操作 (Anchoring)**：将声源 **Anchor** 到匹配实体位置，`position_uncertainty` 继承实体的估计值（静态实体为 0）。
  - **解锚机制 (De-anchoring)**：引入时效性检查，解锚阈值 $T_{break}$ 应**小于**置信度衰减清理时间：
    $$ T_{break} = \frac{\ln(C_{init} / T_{thres})}{-\ln(\lambda_{vis})} \cdot \Delta t \cdot 0.8 $$
    例如 $C_{init}=1.0, T_{thres}=0.1, \lambda_{vis}=0.95, \Delta t=0.048s$ 时，$T_{break} \approx 1.76s$。
    若关联的 VisualEntity 超过 $T_{break}$ 未被重新观测到，强制断开锚定。
  - **状态回退**：解锚后的 AudioEntity 退化为 **Unanchored Audio**，其在 Social Cost Layer 中的表征自动从确定的高斯场切换回概率锥体场。
  - **未锚定声音 (Unanchored Audio)**：若无匹配或已解锚，保留纯听觉定位估计 `position_estimate`。
    - **拓扑感知虚拟动量 (Topology-Aware Hallucinated Momentum)**: 对于未锚定的需避让声源 (`footstep` 和 `chat`)，执行 NLOS 预判：
      1.  **射线探测**: 从机器人位置 $\mathbf{p}_{robot}$ 沿 DoA 方向发出射线。
      2.  **拓扑吸附**: 若射线与墙壁相交于点 $\mathbf{p}_{hit}$，查询静态地图找到最近的**拓扑点**（拐角点），记为 $\mathbf{p}_{hallucinated}$。
      3.  **速度注入**: 赋予虚拟实体速度矢量：
          $$ \mathbf{v}_{virt} = v_{walk} \cdot \frac{\mathbf{p}_{robot} - \mathbf{p}_{hallucinated}}{\|\mathbf{p}_{robot} - \mathbf{p}_{hallucinated}\|} $$
          其中 $v_{walk} \approx 1.2 \text{m/s}$。即速度方向**从虚拟位置指向机器人**，模拟潜在来人。
    - **注意**: 目标声源 (`doorbell`, `help`, `music`, `water`) 不生成虚拟动量，因为它们不需要避让。

- **状态更新 (State Update)**：
  - **时序聚合**：对连续关联到的声源位置 (DoA) 进行平滑，抑制单帧定位跳变。
  - **特征更新**：同样采用 EMA 策略更新 AudioEmbedding，使得特征向量能反映声源在时间维度上的变化 (如语调起伏)。
- **置信度管理 (Confidence Management)**：
  - **匹配更新**: $C_{t} = \min(1.0, \beta \cdot C_{t-1} + (1 - \beta) \cdot C_{obs} \cdot (1 + \log(1 + N_{match})))$。
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

针对人类可能发出的需要避让的声音 (`chat`, `footstep`) 及其本身的存在，根据可见性分为四种情况，建模三种代价场：

| 情况 | 声音类型 | 可见性 | 代价场类型 |
|:---:|:---:|:---:|:---|
| 1 | chat / 静音 | 可见 (VisualEntity - 静止) | 各向同性高斯 |
| 2 | footstep | 可见 (VisualEntity - 移动) | 非对称各向异性高斯 |
| 3 | chat | 不可见 (未锚定) | NLOS Anticipation |
| 4 | footstep | 不可见 (未锚定) | NLOS Anticipation |

所有代价场的幅值 $A$ 与分布范围 $\sigma$ 均为动态参数，以反映感知的不确定性。

1.  **可见静止人类 (Visible Stationary Person)** — (锚定的 `chat` 声源或静音人类)：
    
    - **参数定义**:
      - 统一使用 **VisualEntity** 参数（位置 $\mathbf{p}_{entity}$、位置不确定性 $\sigma_{pos}$、置信度 $C_{conf}$）。
      - 幅值 $A = A_{base} \cdot C_{conf}$ (正比于检测置信度)。
      - 基础方差 $\sigma_{base} = \max(\sigma_{min}, k_{\sigma} \cdot \sigma_{pos})$ (正比于位置不确定性)。
    - **算法**: **各向同性高斯 (Isotropic Gaussian)**
      $$ Cost_{static}(\mathbf{x}) = A \cdot \exp \left( - \frac{\|\mathbf{x} - \mathbf{p}_{entity}\|^2}{2\sigma_{base}^2} \right) $$

2.  **可见移动人类 (Visible Moving Person)** — (锚定的 `footstep` 声源)：
    
    - **参数定义**: 同上，使用 **VisualEntity** 参数（包含速度 $\mathbf{v}$）。
    - **算法**: **非对称各向异性高斯 (Asymmetric Anisotropic Gaussian)**。仅沿速度方向 $\mathbf{v}$ 的前方进行延展。
      $$ Cost_{moving}(\mathbf{x}) = A \cdot \exp \left( - \left( \frac{d_{long}^2}{2\sigma_{long}^2} + \frac{d_{lat}^2}{2\sigma_{base}^2} \right) \right) $$
      - **投影计算**: $d_{long} = (\mathbf{x} - \mathbf{p}_{entity}) \cdot \hat{\mathbf{v}}$，$d_{lat} = \|(\mathbf{x} - \mathbf{p}_{entity}) - d_{long} \cdot \hat{\mathbf{v}}\|$。
      - 若 $d_{long} > 0$ (前方): $\sigma_{long} = \sigma_{base} \cdot (1 + k_{vel} \cdot \|\mathbf{v}\|)$ (延展程度正比于速度)。
      - 若 $d_{long} \le 0$ (后方): $\sigma_{long} = \sigma_{base}$ (不延展)。

3.  **不可见声源 (Unseen Sources)** — 未锚定的 `chat` 和 `footstep`：
    
    **Hearing before Seeing (NLOS Anticipation)** 的核心实现。
    - **输入**: $\mathbf{p}_{hallucinated}$ (虚拟源点), $\mathbf{v}_{virt}$ (虚拟速度), $\text{aperture}$ (源不确定性)。
    - **参数**:
      - 幅值 $A = A_{base} \cdot C_{conf}$。
      - 横向方差 $\sigma_{lat} = k_{lat} \cdot \text{aperture}$ (角度不确定性决定长矛粗细)。
      - **类型缩放**: 为体现 `footstep` 相对更紧迫的避让，可对幅值使用系数 $s_{type}$：
        $s_{type}=s_{chat}$ 或 $s_{footstep}$，最终 $A = A_{base} \cdot s_{type} \cdot C_{conf}$。
    - **算法**: 生成沿虚拟速度方向（指向机器人）单向延伸的**非对称长矛状场**。
      $$ Cost_{NLOS}(\mathbf{x}) = A \cdot \exp \left( - \left( \frac{d_{long}^2}{2\sigma_{front}^2} + \frac{d_{lat}^2}{2\sigma_{lat}^2} \right) \right) \cdot \mathbb{I}(d_{long} > 0) $$
      - **投影计算**: $d_{long} = (\mathbf{x} - \mathbf{p}_{hallucinated}) \cdot \hat{\mathbf{v}}_{virt}$，$d_{lat} = \|(\mathbf{x} - \mathbf{p}_{hallucinated}) - d_{long} \cdot \hat{\mathbf{v}}_{virt}\|$。
      - $\sigma_{front}$ 设定较大以覆盖潜在碰撞路径。
      - 仅在虚拟速度前方生效 ($\mathbb{I}(d_{long} > 0)$)，不惩罚墙后的"声源身后"区域。

4.  **目标豁免 (Target Immunity)**：
    - 若某个实体（Visual 或 Audio）被识别为当前的导航目标（Target），则其产生的 Social Cost 将被**掩码屏蔽 (Masked)** (强制置为 0)。这防止了导航目标本身产生排斥力导致机器人无法靠近。

5.  **聚合 (Aggregation)**：
    $$ C_{social}(\mathbf{x}) = \text{clip}\left(\sum_{i} w_i \cdot C_i(\mathbf{x}), 0, 1\right) $$
    - 各代价场权重 $w_i = 1.0$（等权重叠加）。
    - 归一化采用 clip 到 $[0, 1]$。

## 5. 规划层：SAVNav 规划器 (Planning Layer)

引入双模式状态机，解决“查不准”的问题，在“精确导航”与“主动搜索”模式间动态切换。

任务假设：查询一定包含声音描述（显式或隐式）。

### 5.1 目标仲裁与状态机 (Target Arbitration & State Machine)

1.  **查询解析 (Query Parsing)**:
    - MLLM 解析用户指令 $\rightarrow$ Query $\langle \text{Content}, \text{Modality} \rangle$ (e.g., "Help", "Audio").
2.  **实体匹配 (Entity Matching)**:
    - 在 SAVMap 各层搜索匹配实体。
    - **Visual/Static Layer**: 计算 Query embedding 与实体 embedding 的余弦相似度。
    - **Audio Layer**: 计算 Query embedding 与 AudioEntity 的 audio_embedding 的余弦相似度。
    - **匹配规则**: 选择相似度最高且 $\ge \tau_{match}$ (e.g., 0.5) 的实体作为目标。若无匹配，进入 Idle 状态等待声源出现。
3.  **状态仲裁 (State Arbitration)**:
    
    **锚定判定**：`is_anchored = (associated_visual_id != None) or (associated_static_id != None)`
    
    - **State A (Precision Nav)**:
      - 条件: 目标 AudioEntity 已锚定 (`is_anchored == True`)。
      - 行为: 规划至明确的坐标点 $\mathbf{x}_{goal} = \mathbf{p}_{entity}$。
    - **State B (Active Search)**:
      - 条件: 目标仅匹配到 AudioEntity 且未锚定 (`is_anchored == False`)，即"只闻其声，不见其源"。
      - 行为: 基于目标信念图 (Belief Map) 规划视点，最大化目标发现概率，试图锚定声源。

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
-   **初始化**: 全局初始化为低均匀概率 $P_{init}$ (e.g., 0.01)。
-   **听觉更新 (Audio Positive Update)**:
    获取由 5.1 节锁定的目标 `AudioEntity`，提取其 `position_estimate` 属性（包含原点、主方向、张角）生成声源不确定性锥体，在声源方向锥内注入概率质量。
    $$ \mathcal{M}_{belief}^{(t)}(c) = \text{clip}(\mathcal{M}_{belief}^{(t-1)}(c) + \alpha_{audio} \cdot G(c \mid \Omega_{ROI}), 0, 1) $$
    其中 $\alpha_{audio}$ (e.g., 0.3) 控制听觉正向更新强度，$\Omega_{ROI}$ 为声源不确定性锥体与可通行区域的交集。定义
    $$ G(c \mid \Omega_{ROI}) = \exp\left( -\frac{d_{ray}(c)^2}{2\sigma_{ray}^2} \right) \cdot \mathbb{I}(c \in \Omega_{ROI}) $$
    其中 $d_{ray}(c)$ 为栅格中心 $c$ 到声源射线的垂直距离，$\sigma_{ray}$ 为射线扩散尺度 (默认与 $\text{aperture}$ 成正比)。
    记录本帧听觉更新区域: $\Omega_{audio}^{(t)} = \Omega_{ROI}$。

-   **视觉更新 (Visual Negative Information)**:
    当相机视场扫过某区域 $c$ 且检测器未输出目标时，根据"未观测到"这一事实降低信念值。
    **关键约束**：视觉负向更新应**排除**当前帧有听觉正向更新的区域，防止概率被不当压制：
    $$ \mathcal{M}_{belief}^{(t)}(c) = \mathcal{M}_{belief}^{(t-1)}(c) \cdot \lambda_{neg} \quad \text{if } c \in (\text{FOV}_{free} \setminus \Omega_{audio}^{(t)}) $$
    其中 $\lambda_{neg} \in (0, 1)$ 为遗忘因子 (e.g., 0.3)，$\text{FOV}_{free}$ 表示当前相机视锥体内的无遮挡区域。

#### 2. 增强型候选视点生成 (Enhanced Candidate Viewpoint Generation)

构建候选视点集 $\mathcal{P} = \{p_1, p_2, \dots, p_N\}$，每个视点包含**位置** $(x, y)$ 和**朝向** $\psi$ (Yaw)：

**朝向规则**：所有候选视点的默认朝向指向 Belief Map 的**概率质量中心**（XZ 平面投影）：
$$ \mathbf{c}_{belief} = \frac{\sum_{c} \mathcal{M}_{belief}(c) \cdot c}{\sum_{c} \mathcal{M}_{belief}(c)}, \quad \psi_i = \text{atan2}(c_{belief,x} - p_{i,x}, -(c_{belief,z} - p_{i,z})) $$

> **注意**：Yaw 角定义为 0° 面向 -Z，逆时针为正，因此使用 `atan2(Δx, -Δz)`。
>
> **边界处理**：若 $\sum_c \mathcal{M}_{belief}(c) < \epsilon$ (e.g., $10^{-6}$)，使用目标 AudioEntity 的 DoA 方向作为默认朝向。

1.  **拓扑节点**: 来源于静态地图预计算的拓扑点（拐角、门口等）。
2.  **ROI 区域采样 (ROI-Guided Sampling)**:
    直接在声源不确定性锥体与可通行地图的交集 $\Omega_{ROI}$ 及其周边进行均匀采样。
    -   **算法**: 在 $\Omega_{ROI}$ 区域内生成栅格采样点 $\{s_1, \dots, s_k\}$，并滤除离最近障碍物距离小于 $d_{safe}$ 的点。
    -   **作用**: 弥补拓扑节点的稀疏性。如果声源位于房间深处的角落，拓扑节点可能无法提供清晰视线，此策略允许 Agent 深入目标区域进行确认。
3.  **原地重定位采样 (In-situ Reorientation)**:
    在机器人当前位置 $R_{local}$ (e.g., 0.5m) 范围内采样，朝向同样指向 $\mathbf{c}_{belief}$。
    -   **目的**: 允许 Agent 执行低代价的原地旋转或微调，以解决“刚经过声源但视场未覆盖”的问题，避免舍近求远。

#### 3. 信息论效用评估 (Information-Theoretic Utility Evaluation)

对每个候选视点 $p_i$ 进行评分，旨在最大化**有效观测范围内**的目标发现期望，同时最小化移动代价。

$$ U(p_i) = \mathcal{I}_{gain}(p_i) - \beta_{cost} \cdot \mathcal{C}_{cost}(p_i) $$

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

$$ \mathcal{C}_{cost}(p_i) = \frac{L(\mathbf{p}_{robot}, p_i)}{v_{avg}} $$

**符号定义**:
*   $L(\cdot)$: 测地距离 (Geodesic Distance)，通过 Habitat PathFinder 接口计算的实际路径长度，见 [get_geodesic_distance.md](../tests/utils/map/get_geodesic_distance.md)。
*   $v_{avg}$: 机器人平均移动速度。
*   $\beta_{cost}$: 调节搜索收益与时间成本的权重系数。
  - **物理意义**: $\beta_{cost}$ 表示每秒移动时间等价于多少概率收益的损失。例如 $\beta_{cost}=0.1$ 表示移动 10 秒等价于损失 1.0 的概率收益。

#### 4. 决策

选择 $p^* = \arg\max_{p \in \mathcal{P}} U(p)$ 作为局部导航目标 $\mathbf{x}_{search}$。
    -   若 $p^*$ 为原地旋转点，则直接下发 Velocity Command。
    -   若 $p^*$ 为远端点，则调用 Planner 生成路径。

### 5.4 状态转换逻辑 (State Transition Logic)

引入**滞后机制 (Hysteresis)** 防止状态震荡：

**锚定判定**：`is_anchored = (associated_visual_id != None) or (associated_static_id != None)`

- **B → A (Capture)**:
  - 条件: 目标 AudioEntity 的 `is_anchored == True` 且**持续** $T_{stable}$ (e.g., 0.5s)。
  - 计数器: `capture_counter += 1` 每帧；若中途断开则重置为 0。
  - 触发: `capture_counter * Δt >= T_stable`。

- **A → B (Lost)**:
  - 条件: 目标 AudioEntity 的 `is_anchored == False` 且**持续** $T_{lost}$ (e.g., 1.0s)。
  - 计数器: `lost_counter += 1` 每帧；若重新锚定则重置为 0。
  - 触发: `lost_counter * Δt >= T_lost`。
  - **注意**: 静态实体锚定后不会自动解锚（位置恒定），仅动态人类锚定可能触发 Lost。

- **A/B → Idle (等待声源)**:
  - 条件: 目标 AudioEntity 的 `confidence < T_{thres}` 被清理。
  - 行为: 输出静止速度 `[0.0, 0.0]`，原地等待声源再次响起。
  - **说明**: 任务中所有目标声音持续循环播放，声源消失仅为暂时性，等待重新检测到后自动恢复导航。

- **Idle → A/B (Resume)**:
  - 条件: 新的 AudioEntity 匹配到目标查询 (embedding 余弦相似度 $\ge \tau_{query}$)。
  - 行为: 若新 AudioEntity 已锚定 (`is_anchored == True`) 则直接进入 State A；否则进入 State B。

### 5.5 动作执行 (Action Execution)

参考 [velocity_planner.py](../tests/utils/velocity_planner.py)，支持：
- **移动控制**: 沿 FMM 规划路径的速度控制。
- **旋转控制**: 旋转到指定 Yaw 角度（用于原地重定位）。

**输出格式**：
```python
{
    "action": "agent_0_base_velocity",
    "action_args": {
        "agent_0_base_vel": [v_linear, ω_angular],  # 归一化到 [-1, 1]
    },
}
```
- `v_linear`: 前进速度，归一化值 $\in [0, 1]$（$1.0$ 对应 `max_linear_speed`）。
- `ω_angular`: 角速度，归一化值 $\in [-1, 1]$（正值为左转，$1.0$ 对应 `max_angular_speed`）。
- **Idle 状态**: 输出 `[0.0, 0.0]` 表示静止。

---

## 附录 A: 参数汇总表 (Parameter Summary)

以下为系统所有可调参数的默认值汇总，按模块分类。

### A.1 系统参数 (System Parameters)

| 参数 | 符号 | 默认值 | 单位 | 说明 |
|:---|:---:|:---:|:---:|:---|
| 仿真步长 | `update_dt` | 0.048 | s | Habitat 仿真引擎每步推进时间 |
| 栅格分辨率 | `grid_size` | 0.05 | m | SAVMap 栅格地图分辨率 |
| 感知缓冲区大小 | `N_buffer` | 1000 | - | 感知层历史记录最大条数 |

### A.2 视觉感知参数 (Visual Perception)

| 参数 | 符号 | 默认值 | 单位 | 说明 |
|:---|:---:|:---|:---:|:---|
| 深度不确定性系数 | $k_d$ | 0.005 | m⁻¹ | 深度相机误差随距离平方增长的系数 |
| 遮挡惩罚系数 | $k_{occ}$ | 0.5 | m | 遮挡导致的位置不确定性惩罚 |

### A.3 音频感知参数 (Audio Perception)

| 参数 | 符号 | 默认值 | 单位 | 说明 |
|:---|:---:|:---:|:---:|:---|
| 角度基准误差 | $\sigma_{base}$ | 15.0 | ° | SELD 模型的基准定位误差 |
| 不确定性缩放系数 | $k_{unc}$ | 0.5 | - | 低置信度时的不确定性放大因子 |
| 最大距离估计 | $R_{max}^{audio}$ | 10.0 | m | 声源距离估计的开环上界 |

### A.4 动态视觉层参数 (DynamicVisualLayer)

| 参数 | 符号 | 默认值 | 单位 | 说明 |
|:---|:---:|:---:|:---:|:---|
| 最大跃变距离 | $d_{thres}$ | 2.0 | m | 关联匹配的最大允许位置跳变 |
| 位置权重 | $w_{pos}$ | 0.7 | - | 混合代价中位置项权重 |
| 嵌入权重 | $w_{emb}$ | 0.3 | - | 混合代价中嵌入项权重 |
| 关联代价阈值 | $C_{thres}^{assoc}$ | 0.8 | - | 超过此值拒绝匹配 |
| EMA 基础系数 | $\alpha_{base}$ | 0.6 | - | 特征更新 EMA 系数 (乘以 conf) |
| 置信度平滑系数 | $\beta$ | 0.8 | - | 置信度更新的历史权重 |
| 视觉衰减因子 | $\lambda_{vis}$ | 0.95 | - | 未匹配时置信度指数衰减率 |
| 清理阈值 | $T_{thres}$ | 0.1 | - | 置信度低于此值时移除实体 |

### A.5 动态听觉层参数 (DynamicAudioLayer)

| 参数 | 符号 | 默认值 | 单位 | 说明 |
|:---|:---:|:---:|:---:|:---|
| DoA 匹配角度阈值 | $\theta_{match}$ | 15.0 | ° | 声源关联的最大角度偏差 |
| 静态实体匹配阈值 | $\tau_{static}$ | 0.6 | - | 音频与静态实体 embedding 余弦相似度阈值 |
| 速度阈值 | $v_{thres}$ | 0.3 | m/s | 区分静止/移动人类的速度边界 |
| 虚拟行走速度 | $v_{walk}$ | 1.2 | m/s | NLOS 虚拟动量的速度大小 |
| 音频衰减因子 | $\lambda_{audio}$ | 0.8 | - | 未匹配时置信度指数衰减率 |
| 解锚安全系数 | - | 0.8 | - | $T_{break}$ 计算中的安全裕度 |

### A.6 社交代价层参数 (SocialCostLayer)

| 参数 | 符号 | 默认值 | 单位 | 说明 |
|:---|:---:|:---:|:---:|:---|
| 基础幅值 | $A_{base}$ | 1.0 | - | 代价场的归一化基准幅值 |
| 最小方差 | $\sigma_{min}$ | 0.3 | m | 高斯场的最小空间方差 (约人体半径) |
| 方差缩放系数 | $k_{\sigma}$ | 2.0 | - | 位置不确定性到方差的缩放因子 |
| 速度延展系数 | $k_{vel}$ | 1.5 | s | 移动人类前向方差延展系数 |
| 横向方差系数 | $k_{lat}$ | 0.5 | m/° | 角度不确定性到横向方差的转换系数 |
| 前向方差 (NLOS) | $\sigma_{front}$ | 3.0 | m | 未见声源的前向覆盖范围 |
| 类型幅值缩放 (chat) | $s_{chat}$ | 1.0 | - | 未见 `chat` 的幅值缩放 |
| 类型幅值缩放 (footstep) | $s_{footstep}$ | 1.2 | - | 未见 `footstep` 的幅值缩放 |
| 代价场权重 | $w_i$ | 1.0 | - | 各代价场叠加权重 (等权重) |
| 社交权重 | $w_{soc}$ | 0.8 | - | FMM 速度场中社交代价的权重 |

### A.7 规划层参数 (Planning Layer)

| 参数 | 符号 | 默认值 | 单位 | 说明 |
|:---|:---:|:---:|:---:|:---|
| 最大速度 (FMM) | $S_{max}$ | 1.0 | - | FMM 速度场的归一化最大值 |
| 最小速度 (FMM) | $S_{min}$ | 0.1 | - | FMM 速度场的下界 ($0.1 \cdot S_{max}$) |
| 初始信念概率 | $P_{init}$ | 0.01 | - | Belief Map 全局初始化值 |
| 听觉正向更新强度 | $\alpha_{audio}$ | 0.3 | - | 声源方向锥内的概率注入强度 |
| 视觉负向遗忘因子 | $\lambda_{neg}$ | 0.3 | - | 视野内未检测到目标时的概率衰减 |
| 除零阈值 | $\epsilon$ | 1e-6 | - | Belief Map 质心计算的分母下界 |
| 安全距离 | $d_{safe}$ | 0.3 | m | 候选视点到障碍物的最小距离 |
| 原地采样半径 | $R_{local}$ | 0.5 | m | 原地重定位采样的范围 |
| 传感器衰减方差 | $\sigma_{sensor}$ | 3.0 | m | 距离衰减因子的特征尺度 |
| 检测截断距离 | $R_{max}^{detect}$ | 5.0 | m | 超过此距离认为无法有效检测 |
| 平均移动速度 | $v_{avg}$ | 0.5 | m/s | 移动代价计算中的参考速度 |
| 代价权重 | $\beta_{cost}$ | 0.1 | - | 效用函数中移动代价的权重 |

### A.8 状态机参数 (State Machine)

| 参数 | 符号 | 默认值 | 单位 | 说明 |
|:---|:---:|:---:|:---:|:---|
| 实体匹配阈值 | $\tau_{match}$ | 0.5 | - | 查询与实体 embedding 相似度阈值 |
| 锚定稳定时间 | $T_{stable}$ | 0.5 | s | B→A 状态转换所需的持续锚定时间 |
| 丢失确认时间 | $T_{lost}$ | 1.0 | s | A→B 状态转换所需的持续丢失时间 |
| 查询匹配阈值 | $\tau_{query}$ | 0.5 | - | Idle→A/B 恢复时的 embedding 相似度阈值 |

### A.9 动作执行参数 (Action Execution)

| 参数 | 符号 | 默认值 | 单位 | 说明 |
|:---|:---:|:---:|:---:|:---|
| 最大线速度 | `max_linear_speed` | 10.0 | m/s | 机器人前进的最大速度 |
| 最大角速度 | `max_angular_speed` | 10.0 | rad/s | 机器人旋转的最大角速度 |
| 目标到达容差 | `goal_tolerance_m` | 0.2 | m | 判定到达目标的距离阈值 |

---

**注**：以上参数均为建议默认值，实际部署时应根据具体场景、传感器特性和任务需求进行调优。
