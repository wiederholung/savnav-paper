# Unified 面板图注（PRECISION_NAV）— 移植参考

给**实机实验仓库**参考用：把 SAVNav unified 面板右上角那块图注单独抽出来，只依赖
`matplotlib` + `numpy`，不依赖 habitat / savnav 任何东西。整份代码可直接拷进新仓库。

对应本仓实现：`src/savnav/savnav/utils/visualization.py`（`_legend_topright`、
`_HandlerGradientBar`）与 `src/savnav/savnav/utils/map_panel.py`（`LEGEND_ORDER`）。

---

## 1. PRECISION_NAV 下会出现哪些条目

图注是**按帧实测**的：谁被画到图上、谁才进图注（`ax.get_legend_handles_labels()` 去重）。
精确导航状态下 unified 面板最多 8 条：

| 条目 | 图标 | 出现条件 |
|---|---|---|
| `Social Cost` | 橙色渐变色条 | 恒有（社交代价场一直画） |
| `Anchored Audio` | 深品红空心圈 | 有已锚定的声源实体时 |
| `NLOS-associated node` | 深墨色空心圈 | 有未锚定声源且关联到拓扑节点时 |
| `Target` | 红色五角星 | 恒有（PRECISION_NAV 的终点标记） |
| `Planned Path` | 绿色粗线 | 规划路径长度 > 1 时 |
| `Robot Trajectory` | 棕色粗线 | 历史轨迹长度 ≥ 2 时 |
| `Human` | 绿色实心圆 | 视野内有被跟踪的人时 |
| `Robot` | 青色三角 | 恒有 |

**不会出现**（都是 ACTIVE_SEARCH 专属）：`Target Belief`、`Belief Centroid`、
`Candidate Viewpoints`、`Best Viewpoint`。`Topology Nodes` 只在 SAVMap 面板出现，
unified 刻意不画（几十上百个叉号是背景噪声，且与听觉锥体抢色）。

---

## 2. 配色（RGB，值域 [0,1]）

```python
ANCHORED_RING_COLOR = (0.62, 0.02, 0.38)   # 深品红：听觉证据"已锚定到实体"
NLOS_NODE_COLOR     = (0.15, 0.16, 0.22)   # 深墨色：听觉证据落到拓扑节点
GOAL_MARKER_COLOR   = (0.84, 0.15, 0.16)   # 红：Target 五角星
PATH_COLOR          = (0.17, 0.63, 0.17)   # 绿：规划路径
TRAJECTORY_COLOR    = (0.50, 0.32, 0.13)   # 暖棕：历史轨迹
HUMAN_COLOR         = (0.17, 0.63, 0.17)   # 绿：人（与 path 同绿，靠形状区分）
ROBOT_COLOR         = (0.00, 0.60, 0.60)   # 青：机器人
SOCIAL_COST_CMAP    = "Oranges"            # 社交代价场色带
```

两处选色理由（换配色前先读，否则很容易踩回去）：

- **锚定圈与 NLOS 圈用固定色，不跟声源类别色走。** 状态和身份是正交的两个维度——身份由
  锥体/标签的类别色表达，状态由这两个固定色表达。曾让它们取所属声源锥体的深色描边变体
  （"同一实体配色同源"），结果在 unified 上圈和锥糊成一体：锥体是大面积高饱和多边形，
  同色细环压在它边上根本读不出来。
- **NLOS 取墨色而非品红族。** 两个圈都是空心圆，同为品红时在图注小图标上只剩明度差，
  实测就是两个一模一样的环。可换的色相其实只剩黄/金和黑/中性（品红被拓扑节点+doorbell
  占、绿被 person/path 占、蓝被 belief/候选点占、青被 robot/water_tap 占、紫被
  human_call/television 占、橙棕被代价场/轨迹占、红被星标占）；金色会死在 Oranges 代价场
  上，而 NLOS 圈恰恰常落在代价场里，所以取墨色——灰 floor / 橙代价场 / 蓝 belief 三种底色
  上都是最高对比。

---

## 3. 两个非显然的实现点

**① 地图上是 Patch 的元素，图注里必须换 `Line2D` 代理。**
matplotlib 的 `HandlerPatch` 无视 patch 的实际形状，一律照原属性造一个 `Rectangle`——
所以直接把地图上的 `Circle`（human、锚定环）和 `Polygon`（机器人三角）丢进图注，出来
全是方块。必须显式给 `Line2D(marker=...)` 代理。

**② 连续场（代价场）要用整条渐变色条，不能用离散色块。**
它是连续量，三个色块会读成"三个类别"。matplotlib 没有现成的渐变 handler，用 N 个首尾
相接的窄矩形拼（`_HandlerGradientBar`）比自定义 renderer 可靠，也不依赖 legend 内部管线。

---

## 4. 可直接拷贝的完整实现

```python
"""Unified 面板右上角图注（PRECISION_NAV）。仅依赖 matplotlib + numpy。"""
import math
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerTuple
from matplotlib.lines import Line2D

ANCHORED_RING_COLOR = (0.62, 0.02, 0.38)
NLOS_NODE_COLOR     = (0.15, 0.16, 0.22)
GOAL_MARKER_COLOR   = (0.84, 0.15, 0.16)
PATH_COLOR          = (0.17, 0.63, 0.17)
TRAJECTORY_COLOR    = (0.50, 0.32, 0.13)
HUMAN_COLOR         = (0.17, 0.63, 0.17)
ROBOT_COLOR         = (0.00, 0.60, 0.60)

# 图注条目的固定顺序（从左到右、从上到下）。未出现的条目自动跳过，所以同一张表可以
# 直接用在不同状态/不同面板上，各自得到正确的子序列——分开维护多份只会漂移。
LEGEND_ORDER = (
    "Social Cost",            # 连续场
    "Anchored Audio",         # 听觉/拓扑证据
    "NLOS-associated node",
    "Target",                 # 规划意图
    "Planned Path",
    "Robot Trajectory",
    "Human",                  # 主体
    "Robot",
)
FIELD_CMAPS = {"Social Cost": "Oranges"}   # 走渐变色条的条目


class HandlerGradientBar:
    """把图注条目画成一条连续渐变色条。

    用 N 个首尾相接的窄矩形拼出色条：matplotlib 没有现成的渐变 handler，这样比自定义
    renderer 可靠，且不依赖 legend 内部的绘图管线。
    """

    def __init__(self, cmap_name, n_slices=48, low=0.12):
        self.cmap_name, self.n_slices, self.low = cmap_name, n_slices, low

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        cmap = plt.get_cmap(self.cmap_name)
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        w, h = handlebox.width, handlebox.height
        bar_h = h * 0.72                      # 略矮于整格并垂直居中，免得顶到上下行文字
        bar_y = -y0 + (h - bar_h) / 2.0
        sw = w / self.n_slices
        for i in range(self.n_slices):
            frac = self.low + (1.0 - self.low) * (i / max(1, self.n_slices - 1))
            handlebox.add_artist(mpatches.Rectangle(
                (-x0 + i * sw, bar_y), sw * 1.06, bar_h,   # 宽 1.06 消除反锯齿缝隙
                facecolor=cmap(frac), edgecolor="none"))
        border = mpatches.Rectangle((-x0, bar_y), w, bar_h,
                                    facecolor="none", edgecolor="0.45", linewidth=0.7)
        handlebox.add_artist(border)
        return border


def _ring(c):
    return Line2D([], [], marker="o", linestyle="none", markersize=12,
                  markerfacecolor="none", markeredgecolor=c, markeredgewidth=2.2)


def legend_proxies():
    """label -> 图注图标。地图上是 Patch 的元素必须在这里换成 Line2D 代理，
    否则 HandlerPatch 会把 Circle / Polygon 一律渲染成方块。"""
    return {
        "Anchored Audio":       _ring(ANCHORED_RING_COLOR),
        "NLOS-associated node": _ring(NLOS_NODE_COLOR),
        "Target": Line2D([], [], marker="*", linestyle="none", markersize=16,
                         markerfacecolor=GOAL_MARKER_COLOR,
                         markeredgecolor="white", markeredgewidth=0.8),
        "Planned Path":     Line2D([], [], color=PATH_COLOR, linewidth=6.0),
        "Robot Trajectory": Line2D([], [], color=TRAJECTORY_COLOR, linewidth=5.5),
        "Human": Line2D([], [], marker="o", linestyle="none", markersize=12,
                        markerfacecolor=HUMAN_COLOR, markeredgecolor="black",
                        markeredgewidth=1.0),
        # 地图上机器人是朝向 yaw 的三角形；图注用正立 '^' 保持形状身份，不表达朝向
        "Robot": Line2D([], [], marker="^", linestyle="none", markersize=13,
                        markerfacecolor=ROBOT_COLOR, markeredgecolor="black",
                        markeredgewidth=1.0),
    }


def register_field_legend(ax, label):
    """给连续场（imshow 热力图）注册图注条目。

    imshow 产出的 AxesImage 不进 get_legend_handles_labels()，所以整片渐变没法直接进
    图注。加一个零数据点的占位 Line2D：只贡献 label，不画任何像素。
    """
    ax.plot([], [], linestyle="none", marker="none", label=label)


def draw_legend(ax, rows=2, fontsize=16):
    """在 ax 右上角画去重图注。返回 Legend 对象（无条目时 None）。

    只收集**当前已画到 ax 上**且带 label 的 artist，所以图注自动跟随本帧内容；
    同 label 只保留第一个 handle，图注不会随实体数量膨胀。
    """
    handles, labels = ax.get_legend_handles_labels()
    seen = {}
    for h, l in zip(handles, labels):
        seen.setdefault(l, h)
    if not seen:
        return None

    ordered = {k: seen[k] for k in LEGEND_ORDER if k in seen}
    ordered.update({k: v for k, v in seen.items() if k not in ordered})

    proxies = legend_proxies()
    for lbl, proxy in proxies.items():
        if lbl in ordered:
            ordered[lbl] = proxy

    handler_map = {}
    for lbl, cmap_name in FIELD_CMAPS.items():
        if lbl in ordered:
            handler_map[ordered[lbl]] = HandlerGradientBar(cmap_name)

    ncol = max(1, math.ceil(len(ordered) / max(1, rows)))
    leg = ax.legend(
        list(ordered.values()), list(ordered.keys()),
        loc="upper right", fontsize=fontsize, framealpha=0.92, edgecolor="0.4",
        ncol=ncol, handler_map=handler_map or None,
        # 收紧内外边距：默认值会在框内外各留出近一行字高，论文版面吃不消
        borderaxespad=0.15, borderpad=0.35, labelspacing=0.35,
        columnspacing=1.2, handletextpad=0.5,
    )
    leg.set_zorder(300)          # 压过所有地图元素
    leg.get_frame().set_linewidth(2.0)
    return leg
```

绘制侧只要给 artist 挂上表里的 label 就会自动进图注，例如：

```python
ax.add_patch(mpatches.Circle(pos, 0.20, facecolor=HUMAN_COLOR, edgecolor="black",
                             linewidth=1.2, zorder=60, label="Human"))
ax.add_patch(mpatches.Circle(pos, 0.31, facecolor="none",
                             edgecolor=ANCHORED_RING_COLOR, linewidth=3.0,
                             zorder=65, label="Anchored Audio"))
ax.plot(xs, zs, color=PATH_COLOR, linewidth=6.0, zorder=35, label="Planned Path")
ax.scatter(gx, gz, marker="*", s=850, c=[GOAL_MARKER_COLOR], edgecolors="white",
           linewidths=3.0, zorder=90, label="Target")
register_field_legend(ax, "Social Cost")   # 代价场是 imshow，需单独注册
draw_legend(ax, rows=2)
```

---

## 5. 摆位与行数（想复刻整块顶部区域时才需要）

本仓 unified 面板把**状态框固定左上、图注固定右上**，两者都不让位；宽度不够时**加宽画布**
而不是把某一个挪到别的角（对角布局会让视线在两角之间来回跳，多面板并排时角标位置还不一致）。

行数不写死。行数与画布加宽量是一对权衡：行多则图注窄（少加宽）但高（顶部空白多），行少则
反之。留白率有闭式解——画布高 `H` 固定、地图数据宽高比 `A`、顶部空白占比 `f`、加宽倍数 `w`：

> 地图面积 `[H(1-f)]²·A`，画布面积 `H²(1-f)·A·w` ⟹ **留白率 = 1 − (1-f)/w**

所以扫一遍行数取 `(1-f)/w` 最大者即可。实测最优行数随面板胖瘦分岔：宽幅面板选 2 行 × 4 栏
（加宽几乎免费，该压低顶部空白），近正方形面板选 4 行 × 2 栏（加宽很贵，该把图注收窄）。

两个工程要点，移植时容易漏：

- **求解不必重绘地图。** `Legend.get_window_extent(renderer)` 只触发图注自身的盒式排版，
  不需要 `canvas.draw()`（实测与重绘后量得的数值一致）。整轮求解几十毫秒；若每个候选都
  重画整张面板，一次求解要多花掉六帧的渲染时间。
- **排版要单调增长。** 图注条目随实体出现/消失反复增删，若每帧都退回"刚好够用"的尺寸，
  画布宽度与顶部空白就逐帧变化——视频里是整张图在抖。只在当前排版**装不下**时才重解，
  且顶部空白与加宽倍数只增不减。

完整实现见本仓 `src/savnav/savnav/utils/callback.py` 的 `_solve_panel_layout`；
若实机侧只需要静态出图、不出视频，直接固定 `rows=2` 即可，可跳过整套求解。
