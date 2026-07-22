#!/usr/bin/env python
"""Shared bottom legend band for build_exp_q_sim.py / build_exp_q_real.py.

Single source of truth for the unified-panel legend entries (palette + icon
proxies, ported from scripts/unified_panel_legend_reference.md; must match what
the renderer baked into the frames) and for the outcome key.  Outcome entries
are hollow square frames echoing the coloured outcome border of terminal
keyframes -- the real figure's icon style (a Patch handle would stretch to the
full handlebox and read as a bar, not a frame).

Each figure passes the subset of map-element keys present in its maps plus its
outcome list; the band is a frameless matplotlib legend centred in an invisible
axes at the very bottom of the canvas, auto-shrinking its font until the row
layout fits the band width.
"""
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# ---- unified-panel palette (RGB in [0,1]) -----------------------------------
# Fixed status colours; class colours are self-labelled inside each map so they
# need no legend entry here.
ANCHORED_RING_C = (0.62, 0.02, 0.38)   # deep magenta: anchored acoustic evidence
NLOS_NODE_C     = (0.15, 0.16, 0.22)   # ink: unanchored evidence on a topo node
GOAL_C          = (0.84, 0.15, 0.16)   # red target star
PATH_C          = (0.17, 0.63, 0.17)   # green planned path
TRAJ_C          = (0.50, 0.32, 0.13)   # warm brown robot trajectory
HUMAN_C         = (0.17, 0.63, 0.17)   # green human dot (shape disambiguates)
ROBOT_C         = (0.00, 0.60, 0.60)   # cyan robot triangle
COST_CMAP       = "Oranges"            # social cost field
BELIEF_CMAP     = "Blues"              # target belief map (active search state)

# ---- outcome key ------------------------------------------------------------
OUTCOME_C = {"success": "#1a9850", "collision": "#d62728", "unreached": "#f0a020"}
OUTCOME_LABEL = {"success": "Success", "collision": "Collision",
                 "unreached": "Not reached"}


class HandlerGradientBar:
    """Render a legend entry as one continuous gradient bar.

    Built from N abutting narrow rectangles: matplotlib has no stock gradient
    handler, and this stays independent of the legend's internal draw pipeline.
    (Ported from scripts/unified_panel_legend_reference.md.)
    """

    def __init__(self, cmap_name, n_slices=48, low=0.12):
        self.cmap_name, self.n_slices, self.low = cmap_name, n_slices, low

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        cmap = plt.get_cmap(self.cmap_name)
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        w, h = handlebox.width, handlebox.height
        bar_h = h * 0.72
        bar_y = -y0 + (h - bar_h) / 2.0
        sw = w / self.n_slices
        for i in range(self.n_slices):
            frac = self.low + (1.0 - self.low) * (i / max(1, self.n_slices - 1))
            handlebox.add_artist(mpatches.Rectangle(
                (-x0 + i * sw, bar_y), sw * 1.06, bar_h,   # 1.06: hide AA seams
                facecolor=cmap(frac), edgecolor="none"))
        border = mpatches.Rectangle((-x0, bar_y), w, bar_h,
                                    facecolor="none", edgecolor="0.45",
                                    linewidth=0.7)
        handlebox.add_artist(border)
        return border


def _ring(c):
    return Line2D([], [], marker="o", linestyle="none", markersize=8.5,
                  markerfacecolor="none", markeredgecolor=c, markeredgewidth=1.8)


def _star():
    return Line2D([], [], marker="*", linestyle="none", markersize=13.5,
                  markerfacecolor=GOAL_C, markeredgecolor="white",
                  markeredgewidth=0.8)


def _frame(c):
    # hollow square marker: the real figure's outcome icon, adopted for both
    return Line2D([], [], marker="s", linestyle="none", markersize=9.5,
                  markerfacecolor="none", markeredgecolor=c,
                  markeredgewidth=2.2)


# Map elements are Patches on the source frames; the legend needs Line2D proxies
# (HandlerPatch would render Circle/Polygon as plain rectangles).  Labels follow
# the paper's sentence-case convention for internal terms.
def _entry(key):
    """key -> (label, handle, gradient cmap or None)."""
    if key == "cost":
        return ("Social cost field", Patch(facecolor="none", edgecolor="none"),
                COST_CMAP)
    if key == "belief":
        # continuous field like the cost, hence a second gradient bar
        return ("Target belief", Patch(facecolor="none", edgecolor="none"),
                BELIEF_CMAP)
    if key == "anchored":
        return "Anchored audio", _ring(ANCHORED_RING_C), None
    if key == "nlos_node":
        return "NLOS-associated node", _ring(NLOS_NODE_C), None
    if key == "target":
        return "Target", _star(), None
    if key == "target_bv":
        # the sim maps reuse the red star for the best viewpoint during active
        # sensory exploration, so the entry names both roles
        return "Target/Best viewpoint", _star(), None
    if key == "path":
        return "Planned path", Line2D([], [], color=PATH_C, linewidth=4.2), None
    if key == "traj":
        return ("Robot trajectory", Line2D([], [], color=TRAJ_C, linewidth=3.8),
                None)
    if key == "human":
        return ("Human", Line2D([], [], marker="o", linestyle="none",
                                markersize=8.5, markerfacecolor=HUMAN_C,
                                markeredgecolor="black", markeredgewidth=0.8),
                None)
    if key == "robot":
        # the map draws the robot as a yaw-oriented triangle; the legend keeps
        # the shape identity with an upright '^' without implying a heading
        return ("Robot", Line2D([], [], marker="^", linestyle="none",
                                markersize=9, markerfacecolor=ROBOT_C,
                                markeredgecolor="black", markeredgewidth=0.8),
                None)
    raise KeyError(key)


def draw_band(fig, rect, map_keys, outcomes, ncol, fontsize=11.5,
              min_fontsize=8.0):
    """Draw the shared legend band in an invisible axes at rect (fig fractions).

    matplotlib fills a multi-column legend column-major, so with N/ncol == 2 the
    key lists pair up vertically: order map_keys so related entries share a
    column.  The font auto-shrinks in 0.25 pt steps until the legend fits the
    rect width (Legend.get_window_extent triggers only the legend's own box
    layout; no canvas draw needed).  Returns (legend, fontsize_used).
    """
    handles, labels, handler_map = [], [], {}
    for k in map_keys:
        lbl, h, cmap = _entry(k)
        if cmap is not None:
            handler_map[h] = HandlerGradientBar(cmap)
        handles.append(h)
        labels.append(lbl)
    for o in outcomes:
        handles.append(_frame(OUTCOME_C[o]))
        labels.append(OUTCOME_LABEL[o])

    lax = fig.add_axes(rect)
    lax.axis("off")
    avail = rect[2] * fig.bbox.width
    fs = fontsize
    while True:
        leg = lax.legend(handles, labels, ncol=ncol, loc="center",
                         frameon=False, fontsize=fs,
                         handlelength=1.5, handleheight=1.05,
                         borderpad=0.15, columnspacing=1.1,
                         handletextpad=0.45, labelspacing=0.35,
                         handler_map=handler_map)
        if fs <= min_fontsize:
            break
        if leg.get_window_extent(fig.canvas.get_renderer()).width <= avail:
            break
        leg.remove()
        fs -= 0.25
    return leg, fs
