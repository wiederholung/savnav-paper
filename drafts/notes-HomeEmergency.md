# HomeEmergency - Using Audio to Find and Respond to Emergencies in the Home

- 题目思路：方法 - 功能
- 所见略同："Additionally, no known tasks allow prior exploration of the scene, which a home robot will have." savnav同样认为家庭机器人可以预探索并保持地图。
- 任务：HomeEmergency，挑战/价值：非周期性声音、多房间、环境部分可观测
  - 启发：可以加任务对比图？证明savnav任务的价值。
    - e.g., HomeEmergency 依赖先验知识(人类活动时间规律)来定位人类，当人类活动时间不规律时，HomeEmergency 的表现会大幅下降。"A 2-D occupancy map of free space and occupied space, a 2-D map of room definitions, and a room-based heatmap of human activity with added Gaussian noise is provided to the agent. In the real world, it is assumed that the agent can develop this model of human activity over time."
    - savnav的任务：给定语义地图，挑战/价值：动态多声音、非周期性声音、多房间、环境部分可观测，机器人需要定位声源并进行响应。
- 方法：
  - P-DSG：稀疏的，不确定性通过概率边表示，savnav的belive map是稠密的，直接表示不确定性。
- 是否作为baseline跟savnav比较？（最好不比了）

## 补充阅读笔记 (基于论文内容提取)

### 1. 任务设定 (Task Setup)
- **目标**: 使用音频检测家庭中的紧急情况，导航到声源，并确定是否为真实的紧急情况。
- **声音分类**: 
  - **跌倒 (Falls)**: 主要是非周期性/瞬态声音，直接与人相关。
  - **火灾 (Fires)**: 可能是周期性或非周期性声音，与特定物体（如炉子、报警器）相关。
- **真假紧急情况**: 引入了负样本（如掉落的盒子或手提箱），要求机器人不仅要找到声源，还要能区分真假紧急情况（避免假阳性报警）。

### 2. 方法模块 (Method Modules)
- **Mapping (P-DSG, 概率动态场景图)**: 
  - 包含房间、位置和对象层。
  - 对象层分为静态对象 $o_o$（如火灾报警器）和动态代理 $o_{ag}$（如人）。
  - 动态代理节点包含在特定房间的概率（基于预先提供的人类活动热力图）。
- **Audio Perception**: 
  - 使用 Whisper-AT 识别音频标签 $a_l$（如 'thud'）。
  - 获取音频方向 $a_{dir}$（**注意**：在仿真中他们作弊了，使用了“伪真实”的音频方向，即通向声源的最短路径上的房间边界方向）。
- **Inference (贝叶斯推理)**: 
  - 更新房间包含声源的概率: $\mathcal{P}(r_i|a) \propto \mathcal{P}(r_i)\mathcal{P}(a_l|r_i)\mathcal{P}(a_{dir}|r_i)$。
  - $\mathcal{P}(a_l|r_i)$: 对于人的声音，直接使用 P-DSG 中的人类活动概率；对于物体的声音，使用 LLM 评估物体引起该声音的概率。
  - $\mathcal{P}(a_{dir}|r_i)$: 基于音频方向和房间路径的几何关系（简单的阶跃函数）。
- **Emergency Identification**: 
  - 使用多模态大模型 LLaVA 1.6 处理第一人称视角图像和进入新房间时的 360 度图像，判断是否存在紧急情况。

### 3. 实验与结果 (Experiments & Results)
- **Baselines**: Direction Following (DF), Finding Fallen Objects (FFO), PPO (RL)。
- **发现**:
  - 现有的 FFO 和 PPO 在多房间、非周期性声音的复杂任务中表现极差（AG SR 仅 10\% 左右）。
  - 他们的完整方法在 Falls 任务上 AG SR 为 0.75，Fires 任务上为 0.86。
  - **失败的主要原因**: 导航超时/次优导航（74%），碰撞导致仿真失败（21%），VLM 视觉误判（<5%）。

### 4. 对savnav论文的借鉴与对比思路 (Inspiration for Our Paper)
- **音频方向的获取 (Audio Direction)**: 他们在仿真中使用了“伪真实”的音频方向，这在现实中很难完美实现，且忽略了多路径效应和混响。savnav的方法如果能更真实地处理声学特性或音频方向的不确定性，将是一个巨大的优势。
- **先验知识的依赖 (Prior Knowledge)**: 他们的方法强依赖于预先提供的“人类活动热力图”（Human Heatmap）来定位跌倒的人。如果savnav的方法不需要这种强先验，或者能处理更动态、无规律的声源，可以作为savnav的一大卖点。
- **任务复杂性**: 他们的负样本（假紧急情况）处理逻辑是：如果在这个房间没看到人，就继续找其他房间。savnav的任务（动态多声音）比他们更复杂，savnav可以强调在多声源干扰下的导航能力。
- **视觉确认**: 他们依赖 LLaVA 1.6 进行视觉确认，耗时且可能存在幻觉。savnav的视觉模块（如基于语义地图的确认）与之相比的效率和准确性可以探讨。
