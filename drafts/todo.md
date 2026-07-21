# SAVNav 论文 Todo List

## 图片

### Figure 1 (Teaser Figure)

根据确定的核心贡献（解决失聪社交导航与非社会化视听导航的局限），结合现有草图，计划进行以下修改：

<!-- - [ ] **转换第一人称视角 (The robot -> I)**: 将说明性文本改为智能体的思考，增强具身表现力。参考文案：
  - _Help_: "I hear someone calling for help behind the wall. I should explore there."
  - _Chatting_: "I hear them chatting. I should keep a polite distance and not interrupt."
  - _Footsteps (visible)_: "I hear footsteps and see a person. I should yield to avoid collision."
  - _Footsteps (unseen)_: "I hear footsteps around the corner. I should be cautious." -->
- [x] **改为思考气泡 (Thought Bubbles)**: 将现有的蓝色方框替换成漫画式的思考气泡（），从机器人头部冒出，分别指向不同的声音事件，体现机器人的多线程感知与推理。
- [x] **补充干扰声的声音锥体 (Social/Risk Cones)**: 图中目前仅为目标(Help)画了橙色声音锥体。为了体现社交合规性，应为 _Chatting_ 和 _Footsteps_ 也添加声音锥体/波纹（建议用区别于目标的颜色，如黄色或红色半透明），直观表现被声音扩张的社交空间/虚拟墙。
- [x] **[强烈建议] 绘制对比轨迹 (Trajectory Contrast)**: 增加一条直接穿过聊天人群或盲区脚步声的**红色细虚线**（代表传统 AV Nav 的生硬行径并打上），与图中当前的**蓝色实线**（代表 SAVNav 绕过社交区的优雅路线）形成强烈对比，一图切中论文核心。
- [x] caption 要改，叫...framework不合适。

### 方法图

### 仿真展示图

## intro

- [x] contribution 2和3
- [x] method overview 要更新
- [x] 更新 contribution
- [x] NLOS不仅是dp，不要这么局限

## related work

-[x] 相关工作：社交导航、声音导航、主动听觉感知

## dataset

- [x] `doorbell`, `call`（呼唤robot过来，偏日常不是sos）, `music`, `running water`（流水声）
- [x] 仿真节
  - [x] 补充细节，场景用mp3d（选什么规模的场景），不跨层...（falcon有mp3d内容）
  - [x] 补充，episode规模，最大时间步等等尽可能考虑全面
  - [x] 任务成功具体定义：比如在max step内，选择stop方法，且机器人在距离声源 <= x m。
  - [x] 不要叫约束，换个说法
  - [x] 不用训练集，只挑选10个场景用于eval
- [x] 与其他任务对比，加home_emergency，表格跨栏
- [x] 删除cr指标
- [x] 修复表1的列命名歧义与表述不清问题
- [x] SIT和PSV合并成PSV，对移动和静止的人都生效
- [x] 缩写问题，不要沿用我的SC MF，重新设计，符合学术规范
- [x] table-1，改
<!-- - [ ] 与其他任务对比的表格，等related work部分写完后再做更新 -->
- [x] 声音的仿真，（soundspace）再详细说明
- [x] 人数补充说明
- [x] 再过一遍merics
- [x] 在哪提给定地图合适
- [x] The navigating agent is modeled after a Stretch 3 robot2, equipped with a forward-facing RGB-D camera and a 4-channel microphone array.
- [] §IV-A 开头两段（04-dataset.tex L4-L11）用散文体复述了 §III-A Problem Formulation 已形式化的任务定义（两类声音事件、无 GT 人类状态、须推断 NLOS），存在重复。已评估节序（method 前 dataset 后维持现状，理由：method 自包含、dataset 七成内容是评估基础设施、对齐 Falcon 结构），优化方向不是换序，而是把这两段压缩成一两句回指 §III-A 的过渡句，省出篇幅。8页压缩时已处理：删除了 §IV 开头独立引入段，原两段合并压缩成一段（现 04-dataset.tex L7），信息点保留但篇幅大幅缩短；未采用显式回指 §III-A 的过渡句，两节间的语义重复（散文版 vs 形式化版）仍在，只是篇幅问题已解决。

## method

- [x] problem formulation，术语符号定义表格
- [x] q 改为一个词，跟目标声音对齐，且在整节逻辑说清楚
- [x] 更多累计观测？
- [x] problem Formulation的objective太长了
- [x] clap embedding映射到标签，再到imagebind embedding没提；human的embedding是从mask对应图像区域提的；至此两个embedding才在同一空间可比较；虽然是细节，但是不提不行，简单一句话说清楚
- [x] NLOS risk
- [x] 给定的静态语义地图，解释清楚，都有什么（看实现文档，静态物体就漏了，而且没有房间连通性）
- [x] 看渲染后的图片，几乎所有公式都过长，且因为符号过多可读性差
- [x] 更新术语表
- [x] 打磨语言
- [x] 参数提不提
- [x] 检查参数是否有歧义
- [x] 过一遍公式
- [x] 更新符号表格

## experiment

- [x] 打磨语言
- [ ] 实验结果精炼语言

## conclusion

## 其他

- [x] 括号、斜体、粗体、冒号、分点列表等（包括但不限于）格式细节，要符合学术规范，且保持全篇一致（尤其是括号解释，全文太多了）
- [x] 不少学术术语（如“Hallucination”）质感不够或者太ai，要打磨；信息论主动搜索能不能包装成贝叶斯推理
- [x] 不确定性？
- [x] falcon贴墙
- [x] 改题目: Listen to Yield
- [x] 更新savnav_impl.md方法实现细节
- [x] 更新所有caption和表格标题
- [x] 这不仅涉及公式，同时解释不要硬翻中文，源头风险逼近速度假说矢量这种可以用论文英文原文
- [x] 更新实现文档
- [x] 统一robot、agent的称呼
- [x] 引言与方法仍有轻微“术语前置过重”
- [x] Method 仍偏“解释机制”，还没完全转成“服务 claim”
- [x] 根据method更新后文
- [x] 行间公式冒号规范
- [x] γ(∥c−pi∥)应该解释或给出具体公式，但不必像
- [x] FMM
- [x] 术语表/符号检查
- [x] 两张表合并
- [ ] 精炼语言

我的两大心病，实体名和机制名，我希望：
对于环境中实体，1. GT层面有human actor H 【已修复】
2. 感知层面，有human entity及其集合，声学实体 acoustic entity及其集合；【已修复】

对于机制名：target spatial belief map不够好（去掉spatial，或者更好的？），anchoring confidence，NLOS risk belief还可以。总之命名的第一原则是方便同行理解（还有符号），其次考虑相近概念的呼应（例如human entity和acoustic entity，本质还是方便理 解的）。【已修复】
