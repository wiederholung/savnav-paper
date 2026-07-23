#!/usr/bin/env python
"""Compose figures/scene.pdf : representative episodes of the three SAVNav
scenarios (Crowded Social / Hidden Boundary / Mixed Home Activity), one panel
per scenario.

Each panel stacks three third-person views (robot / human actors / target)
over the episode's ground-truth top-down map, and annotates the map with
numbered human badges, class callouts (LOS-NLOS x SCG-DP) and a pink acoustic
target label.  A shared legend band spans the canvas bottom.

Source frames live in figures/demo_dataset/ and are video grabs named
"<scenario>_<camera>.mp4_<t>.png".  A third-person human camera with filename
id k follows the human drawn as circle k+1 on that scenario's GT map.

The GT-map renderer bakes the badge digits rotated by 180 deg and colours each
badge rim by human identity; both are repaired here by covering every baked
badge (and the maroon target square) with an upright vector redraw, so the
composited maps carry crisp selectable-quality marks.  Badge positions below
are measured in source-map pixels (see MAPS).

All geometry is in abstract "u" units, top-down (y grows downward), converted
to matplotlib bottom-up fractions at render time (figure physical aspect ==
u-space aspect; fonts are in points, so U_PER_IN fixes the printed text scale,
matching build_exp_q_sim.py).  Frames embed at full resolution.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from matplotlib.textpath import TextPath
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "figures", "demo_dataset")

# ---- font: match the paper (Times) -----------------------------------------
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif"]
matplotlib.rcParams["pdf.fonttype"] = 42     # embed TrueType, text stays selectable

PDF_DPI = 1400   # views are ~540 px over ~1 in, maps ~1600 px over ~3 in

# ---- palette ----------------------------------------------------------------
# Scenario accent colours shared with build_exp_q_sim.py; chip fills sampled
# from the previous scene figure so the legend keeps its established identity.
ACC = {"los": "#2f6db5", "nlos": "#c0392b", "mixed": "#6d4c9f"}
CHIP = {"LOS":  (191/255, 210/255, 230/255),
        "NLOS": (199/255, 198/255, 198/255),
        "SCG":  (183/255, 218/255, 170/255),
        "DP":   (251/255, 181/255, 123/255),
        "TGT":  (240/255, 209/255, 228/255)}
TEXT_C   = "#1e2022"
EDGE_C   = "#3a3f45"        # badge rims, callout borders, leader lines
TARGET_SQ_C = (0.50, 0.08, 0.05)   # vector redraw of the maroon goal square

FP_SERIF = FontProperties(family="serif")
FP_BOLD  = FontProperties(family="serif", weight="bold")


def ink_w(s, fs, fp=FP_SERIF):
    """ink width of s at fs pt, in u."""
    return TextPath((0, 0), s, size=fs, prop=fp).get_extents().width * U_PER_IN / 72.0


# ---- layout parameters (u-space) -------------------------------------------
S_VIEW   = 300.0    # side of one square third-person view
VIEW_GAP = 14.0     # gap between the three views
V2M_GAP  = 18.0     # views row -> map area
MAP_H    = 560.0    # map area height (all panels equal; each map fits inside)
MAP_PADX = 5.0      # min horizontal clearance map <-> panel edge
TITLE_H  = 70.0     # band above the views for the panel title
PANEL_GAP = 90.0    # gap between panels
MARGIN   = 56.0     # outer margin
LEG_GAP  = 34.0     # panel bottom -> legend band
LEG_H    = 96.0     # legend band height
U_PER_IN = 300.0

PANEL_W = 3 * S_VIEW + 2 * VIEW_GAP
PANEL_H = TITLE_H + S_VIEW + V2M_GAP + MAP_H + 20.0

BADGE_R  = 26.5     # numbered badge radius (uniform across views and maps);
                    # must exceed the largest baked-badge cover need, 25.0 u
                    # on the los map ((27.5 px white + rim/AA) * 918/1230)
BADGE_FS = 11.0     # sizes chosen for the ~0.70 print scale (10.25 in canvas
CHIP_FS  = 9.0      # -> \linewidth): chips stay >= 6 pt on paper
CHIP_H   = 26.0
CHIP_PADX = 7.0
CALL_FS  = 11.0     # callout number
TGT_FS   = 11.5     # pink target label text

# ===========================================================================
# Per-scenario data.  Pixel coordinates refer to the source images.
#   views: (filename, [badges], [target tags]) with badge = (number, x, y) px;
#          each target tag is pink-chip text anchored bottom-left in the view.
#   map:   filename, badges = (number, x, y) px (covering the baked badge),
#          target = (x, y, cover_px) or None (mixed: the target is human 1),
#          callouts = (number|None, chips, box_x, box_y, anchor) with box
#          centre in map px (may extend past the map into panel whitespace)
#          and anchor the map-px point the leader points at.
# ===========================================================================
SCENES = [
    dict(
        key="los", title="Crowded Social",
        views=[
            ("los_third_robot.mp4_000000.000.png",
             [(1, 110, 54), (2, 204, 50)], ["television"]),
            ("los_third_human_1.mp4_000000.425.png",
             [(2, 235, 345), (1, 423, 287)], []),
            ("los_third_human_2.mp4_000000.188.png",
             [(3, 243, 310), (1, 212, 72), (2, 292, 68)], []),
        ],
        map="los_gt_map.mp4_000000.000.png",
        badges=[(1, 809, 460), (2, 763, 487), (3, 910, 40)],
        target=(769, 275, 48),
        callouts=[
            (1, ["LOS", "SCG"], 980, 415, (809, 460)),
            (2, ["LOS", "SCG"], 640, 640, (763, 487)),
            (3, ["LOS", "DP"], 1080, 95, (910, 40)),
            (None, ["television"], 985, 205, (769, 275)),
        ],
    ),
    dict(
        key="nlos", title="Hidden Boundary",
        views=[
            ("nlos_door.mp4_000000.000.png", [], ["doorbell"]),
            ("nlos_third_human_0.mp4_000000.954.png", [(1, 208, 308)], []),
            ("nlos_third_robot.mp4_000000.000.png", [], []),
        ],
        map="nlos_gt_map.mp4_000000.000.png",
        badges=[(1, 340, 211)],
        target=(158, 45, 40),
        callouts=[
            (1, ["NLOS", "DP"], 640, 120, (340, 211)),
            (None, ["doorbell"], 150, 355, (158, 45)),
        ],
    ),
    dict(
        key="mixed", title="Mixed Home Activity",
        views=[
            ("mixed_third_robot.mp4_000000.528.png",
             [(3, 48, 62), (4, 152, 55)], []),
            ("mixed_third_human_0.mp4_000000.202.png",
             [(1, 235, 338)], ["human call"]),
            ("mixed_third_human_1.mp4_000000.290.png",
             [(2, 233, 338)], []),
        ],
        map="mixed_gt_map.mp4_000000.000.png",
        badges=[(1, 1442, 105), (2, 1402, 471), (3, 995, 781), (4, 1060, 887)],
        target=None,
        callouts=[
            (None, ["human call"], 1060, 75, (1442, 105)),
            (2, ["NLOS", "DP"], 1480, 680, (1402, 471)),
            (3, ["LOS", "SCG"], 640, 620, (995, 781)),
            (4, ["LOS", "SCG"], 640, 760, (1060, 887)),
        ],
    ),
]

# ===========================================================================
# Canvas
# ===========================================================================
Ltot = 2 * MARGIN + 3 * PANEL_W + 2 * PANEL_GAP
Htot = MARGIN + PANEL_H + LEG_GAP + LEG_H + 24.0
fig = plt.figure(figsize=(Ltot / U_PER_IN, Htot / U_PER_IN))


def to_frac(x, ytop, w, h):
    return [x / Ltot, (Htot - ytop - h) / Htot, w / Ltot, h / Htot]


def uy(ytop):
    return Htot - ytop


def tint(hexc, t=0.07):
    r, g, b = matplotlib.colors.to_rgb(hexc)
    return (r + (1 - r) * (1 - t), g + (1 - g) * (1 - t), b + (1 - b) * (1 - t))


# background: accent panel boxes ---------------------------------------------
bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, Ltot); bg.set_ylim(0, Htot)
bg.axis("off"); bg.set_zorder(0); bg.patch.set_alpha(0)

# foreground overlay: badges, callouts, leaders, legend ----------------------
fg = fig.add_axes([0, 0, 1, 1]); fg.set_xlim(0, Ltot); fg.set_ylim(0, Htot)
fg.axis("off"); fg.set_zorder(20); fg.patch.set_alpha(0)


def draw_badge(x, y, n, r=BADGE_R):
    """numbered badge (white disc, dark rim) at u-space centre (x, y-down)."""
    fg.add_patch(Circle((x, uy(y)), r, facecolor="white", edgecolor=EDGE_C,
                        linewidth=1.3, zorder=26))
    fg.text(x, uy(y), str(n), fontsize=BADGE_FS, color="black",
            ha="center", va="center_baseline", zorder=27)


def draw_chip(cx, cy, text, fill, fs=CHIP_FS, h=CHIP_H, z=26, edge=None):
    """rounded chip centred at (cx, cy-down); returns its width."""
    w = ink_w(text, fs) + 2 * CHIP_PADX
    fg.add_patch(FancyBboxPatch((cx - w / 2, uy(cy) - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=6",
                                facecolor=fill,
                                edgecolor=edge or "none",
                                linewidth=0.9 if edge else 0, zorder=z))
    fg.text(cx, uy(cy), text, fontsize=fs, color=TEXT_C,
            ha="center", va="center_baseline", zorder=z + 1)
    return w


def draw_callout(bx, by, number, chips, anchor):
    """white rounded callout at u-centre (bx, by-down) + leader to anchor (u).

    chips: class acronyms, or a single target name -> pink label instead.
    """
    is_target = chips and chips[0] not in CHIP
    # leader first (under everything)
    fg.add_line(Line2D([bx, anchor[0]], [uy(by), uy(anchor[1])],
                       color=EDGE_C, linewidth=1.1, zorder=23,
                       solid_capstyle="round"))
    if is_target:
        label = chips[0]
        w = ink_w(label, TGT_FS) + 24.0
        h = 34.0
        fg.add_patch(FancyBboxPatch((bx - w / 2, uy(by) - h / 2), w, h,
                                    boxstyle="round,pad=0,rounding_size=8",
                                    facecolor=CHIP["TGT"], edgecolor=EDGE_C,
                                    linewidth=1.0, zorder=25))
        fg.text(bx, uy(by), label, fontsize=TGT_FS, color=TEXT_C,
                ha="center", va="center_baseline", zorder=26)
        return
    # number + class chips in a white box
    gap = 8.0
    num_w = ink_w(str(number), CALL_FS)
    chip_ws = [ink_w(c, CHIP_FS) + 2 * CHIP_PADX for c in chips]
    inner = num_w + sum(chip_ws) + gap * len(chips)
    pad = 10.0
    w, h = inner + 2 * pad, 36.0
    fg.add_patch(FancyBboxPatch((bx - w / 2, uy(by) - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=8",
                                facecolor="white", edgecolor=EDGE_C,
                                linewidth=1.0, zorder=25))
    x = bx - inner / 2
    fg.text(x + num_w / 2, uy(by), str(number), fontsize=CALL_FS,
            color="black", ha="center", va="center_baseline", zorder=26)
    x += num_w + gap
    for c, cw in zip(chips, chip_ws):
        draw_chip(x + cw / 2, by, c, CHIP[c])
        x += cw + gap


# ===========================================================================
# Panels
# ===========================================================================
y0 = MARGIN
for i, sc in enumerate(SCENES):
    px0 = MARGIN + i * (PANEL_W + PANEL_GAP)
    acc = ACC[sc["key"]]
    pad = 26
    bg.add_patch(FancyBboxPatch(
        (px0 - pad, uy(y0 + PANEL_H) - pad), PANEL_W + 2 * pad,
        PANEL_H + 2 * pad, boxstyle="round,pad=0,rounding_size=30",
        linewidth=1.6, edgecolor=acc, facecolor=tint(acc)))
    fg.text(px0 + 4, uy(y0 + TITLE_H * 0.42), sc["title"], fontsize=17,
            color=acc, weight="bold", ha="left", va="center")

    # --- three third-person views -------------------------------------------
    vy = y0 + TITLE_H
    for j, (fname, badges, chips) in enumerate(sc["views"]):
        vx = px0 + j * (S_VIEW + VIEW_GAP)
        img = Image.open(os.path.join(SRC, fname))
        ax = fig.add_axes(to_frac(vx, vy, S_VIEW, S_VIEW))
        ax.imshow(img, interpolation="none")
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zorder(5)
        for s in ax.spines.values():
            s.set_edgecolor("#c3c7cc"); s.set_linewidth(0.7); s.set_zorder(8)
        k = S_VIEW / img.size[0]          # view px -> u
        for n, x, y in badges:
            draw_badge(vx + x * k, vy + y * k, n)
        # pink acoustic-target tag, anchored to the view's bottom-left corner
        for text in chips:
            w = ink_w(text, 9.0) + 2 * CHIP_PADX
            draw_chip(vx + 12 + w / 2, vy + S_VIEW - 26, text, CHIP["TGT"],
                      fs=9.0, h=28.0, edge=EDGE_C)

    # --- GT map --------------------------------------------------------------
    # uniform white card behind every map: all three panels share the same
    # PANEL_W x MAP_H map area even though the map aspect ratios differ
    my = y0 + TITLE_H + S_VIEW + V2M_GAP
    bg.add_patch(Rectangle((px0, uy(my + MAP_H)), PANEL_W, MAP_H,
                           facecolor="white", edgecolor="none", zorder=1))
    img = Image.open(os.path.join(SRC, sc["map"]))
    iw, ih = img.size
    sc_k = min((PANEL_W - 2 * MAP_PADX) / iw, MAP_H / ih)   # map px -> u
    mw, mh = iw * sc_k, ih * sc_k
    mx = px0 + (PANEL_W - mw) / 2
    my_c = my + (MAP_H - mh) / 2
    ax = fig.add_axes(to_frac(mx, my_c, mw, mh))
    ax.imshow(img, interpolation="none")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zorder(5)
    for s in ax.spines.values():
        s.set_visible(False)

    def m2u(x, y, mx=mx, my_c=my_c, sc_k=sc_k):
        return mx + x * sc_k, my_c + y * sc_k

    # vector target square (covers the baked two-tone marker)
    if sc["target"]:
        tx, ty, cover = sc["target"]
        s_u = cover * sc_k
        ux, uyy = m2u(tx, ty)
        fg.add_patch(Rectangle((ux - s_u / 2, uy(uyy) - s_u / 2), s_u, s_u,
                               facecolor=TARGET_SQ_C, edgecolor="white",
                               linewidth=0.8, zorder=24))
    # numbered badges covering the baked (rotated) ones
    for n, x, y in sc["badges"]:
        ux, uyy = m2u(x, y)
        draw_badge(ux, uyy, n)
    # callouts
    for number, chips, bx, by, anchor in sc["callouts"]:
        draw_callout(*m2u(bx, by), number, chips, m2u(*anchor))

# ===========================================================================
# Legend band
# ===========================================================================
LEG = [("NLOS", "non-line-of-sight"), ("LOS", "line-of-sight"),
       ("SCG", "stationary conversational group"),
       ("DP", "dynamic pedestrian"), ("TGT", "acoustic target")]
LEG_FS = 13.0        # explanation text
LEG_CHIP_FS = 11.0   # acronym inside the chip
LEG_CHIP_H = 34.0
LEG_CHIP_PADX = 11.0
ly = MARGIN + PANEL_H + LEG_GAP + LEG_H / 2
group_gap, chip_text_gap = 60.0, 14.0
widths = []
for k, label in LEG:
    cw = (ink_w("NLOS", LEG_CHIP_FS) + 2 * LEG_CHIP_PADX if k == "TGT"
          else ink_w(k, LEG_CHIP_FS) + 2 * LEG_CHIP_PADX)
    widths.append(cw + chip_text_gap + ink_w(label, LEG_FS))
x = (Ltot - (sum(widths) + group_gap * (len(LEG) - 1))) / 2
for (k, label), wgrp in zip(LEG, widths):
    text = "" if k == "TGT" else k
    cw = ink_w("NLOS" if k == "TGT" else k, LEG_CHIP_FS) + 2 * LEG_CHIP_PADX
    fg.add_patch(FancyBboxPatch((x, uy(ly) - LEG_CHIP_H / 2), cw, LEG_CHIP_H,
                                boxstyle="round,pad=0,rounding_size=7",
                                facecolor=CHIP[k], edgecolor="none", zorder=26))
    if text:
        fg.text(x + cw / 2, uy(ly), text, fontsize=LEG_CHIP_FS, color=TEXT_C,
                ha="center", va="center_baseline", zorder=27)
    fg.text(x + cw + chip_text_gap, uy(ly), label, fontsize=LEG_FS,
            color=TEXT_C, ha="left", va="center_baseline", zorder=27)
    x += wgrp + group_gap

# ===========================================================================
out_pdf = os.path.join(ROOT, "figures", "scene.pdf")
out_png = os.path.join(ROOT, "figures", "scene.png")
fig.savefig(out_pdf, dpi=PDF_DPI)
fig.savefig(out_png, dpi=150)
if os.environ.get("SCENE_AUDIT"):          # high-res raster for visual audit
    fig.savefig(os.path.join(os.environ["SCENE_AUDIT"], "scene_audit.png"),
                dpi=420)
print("wrote", out_pdf, "and", out_png)
print("canvas u:", round(Ltot), "x", round(Htot), " aspect", round(Ltot / Htot, 3))
print("figsize in:", round(Ltot / U_PER_IN, 2), "x", round(Htot / U_PER_IN, 2))
