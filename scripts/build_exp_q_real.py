#!/usr/bin/env python
"""Compose figures/exp-q-real.pdf : real-world qualitative results on the
physical Stretch 3 robot.

Layout (two accent boxes side by side, a uniform 2-row cell grid so the Ours
rows align horizontally with the ablation frames).  Styling is aligned with the
sim figure: each box shows the scene name top-left in the scene accent colour,
the method centred below it, and a per-episode "Target: ..." label above each
tile row; the box border/fill takes the scene accent (Mixed = purple, Hidden
Boundary = red), while the ablation identity is carried by the ochre method text.

  LEFT box  = Mixed Home Activity / SAVNav (Ours), purple
              two SUCCESS episodes, each a 3-frame left->right temporal row
                row 1 : mixed-door  (target: doorbell)
                row 2 : mixed-tv    (target: television)
  RIGHT box = Hidden Boundary / w/o Topology-Aware Acoustic Anticipation, red
              one COLLISION episode, a 2-frame top->down temporal column
              (target: doorbell).  The ablation is shown only in its informative
              NLOS scenario, matching Table~\\ref{tab:main_results}; cf.
              experiments L86: "removing NLOS audio cost causes a collision in
              every occluded encounter".

Each source frame is a dense portrait composite (aspect ~0.641):
  * egocentric FPV               (top-left)
  * two third-person room views  (right)
  * top-down occupancy map with trajectory / cost field / robot pose / goal
    (bottom half)
embedded at full resolution (lossless), never distorted (figure physical aspect
== u-space aspect).

Terminal keyframes carry an outcome tag in the filename (__success / __collision)
which drives the coloured outcome border; the two success/collision states are
the only outcomes in the real set, so the legend has two entries.

Faces in the FPV / third-person views are blurred; the per-keyframe step badge is
parsed from the "_step<NNN>" tag baked into each filename.  Both step badges and
outcome borders default ON (disable with --no-step-labels / --no-outcome-frames).
"""
import os
import re
import argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "figures", "qualitative_exp", "real")

# ---- optional features ------------------------------------------------------
_ap = argparse.ArgumentParser(description="Compose figures/exp-q-real.pdf")
_ap.add_argument("--no-step-labels", dest="step_labels", action="store_false",
                 help="disable the per-keyframe step badge")
_ap.add_argument("--no-outcome-frames", dest="outcome_frames", action="store_false",
                 help="disable the coloured outcome border on terminal keyframes")
_ap.set_defaults(step_labels=True, outcome_frames=True)
ARGS, _ = _ap.parse_known_args()
SHOW_STEP_LABELS = ARGS.step_labels
SHOW_OUTCOME_FRAMES = ARGS.outcome_frames

# ---- font: match the paper (Times) -----------------------------------------
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif"]
matplotlib.rcParams["pdf.fonttype"] = 42     # embed TrueType, text stays selectable

PDF_DPI = 700

# ---- source frames ----------------------------------------------------------
# Face-blurred ("-deface") frames; the robot-side step is baked into each
# filename as "_step<NNN>" and the terminal outcome as "__success"/"__collision".
F = {
    "door1": "mixed-door-ours-deface.mp4_000012.316_step012.png",
    "door2": "mixed-door-ours-deface.mp4_000045.899_step101.png",
    "door3": "mixed-door-ours-deface.mp4_000137.084_step317__success.png",
    "tv1":   "mixed-tv-ours-deface.mp4_000015.933_step007.png",
    "tv2":   "mixed-tv-ours-deface.mp4_000103.266_step138.png",
    "tv3":   "mixed-tv-ours-deface.mp4_000138.906_step288__success.png",
    "abl1":  "nlos-door-ours_no_audio_cost-deface.mp4_000023.999_step038.png",
    "abl2":  "nlos-door-ours_no_audio_cost-deface.mp4_000027.166_step050__collision.png",
}
IMG = {k: Image.open(os.path.join(SRC, v)) for k, v in F.items()}
def ar(k):  # aspect ratio w/h
    return IMG[k].size[0] / IMG[k].size[1]

# ---- step number per keyframe --------------------------------------------
# The robot-side step is baked into each filename as "_step<NNN>" (ROS logical
# time is non-linear, so a filename timestamp * fps would be wrong); parse it
# directly so the badge always matches the frame.
def step_for(k):
    m = re.search(r"_step(\d+)", F[k])
    return int(m.group(1)) if m else None

# ---- outcome per keyframe (parsed from the filename tag) --------------------
OUTCOME_C = {"success": "#1a9850", "collision": "#d62728"}
OUTCOME_LABEL = {"success": "Success", "collision": "Collision"}
def outcome_for(k):
    m = re.search(r"__(success|collision)\.png$", F[k])
    return m.group(1) if m else None

# ---- palette (shared with the sim figure) ----------------------------------
OURS_C   = "#0b6b3a"   # green  -> our-method label
ABL_C    = "#b5651d"   # ochre  -> ablation-method label (matches sim ablations)
TITLE_C  = "#111417"
TARGET_C = "#3f454c"   # slate-grey -> per-episode "Target: ..." label
ARROW_C  = "#464b52"   # slate  -> temporal-sequence arrow
ACC = {"mixed": "#6d4c9f", "nlos": "#c0392b"}   # scene accents (box + scene title)

# ---- layout parameters (u-space, top-down: y grows downward) ----------------
H_TALL   = 1000.0                 # tile height
COL_W    = H_TALL * ar("door1")   # tile width (all frames share the aspect)
SEQ_GAP  = 92.0                   # horizontal gap inside an Ours row (hosts arrow)
ROW_GAP  = 88.0                   # vertical gap between the two cell rows (tightened)
TITLE_H  = 210.0                  # band above a box: scene title + method label
                                  # (roomier so the narrow NLOS header -- scene
                                  # title over a two-line method -- is not cramped)
SCENE_H  = 52.0                   # band above a row for its "Target: ..." label
GAP_BOX  = 104.0                  # gap between the Mixed and NLOS boxes; kept
                                  # tight -- the outcome legend stacks its swatch
                                  # over a rotated label, so the channel is slim
BOX_PAD  = 34.0                   # inner padding of an accent box
MARGIN   = 78.0                   # outer margin

panels = []   # (key, x, ytop, w, h)
texts  = []   # dict
boxes  = []   # dict(x,ytop,w,h,accent)
harrows = []  # (x_mid, y_center)   rightward
varrows = []  # (x_center, y_mid)   downward

def add_img(key, x, ytop):
    panels.append((key, x, ytop, COL_W, H_TALL))

def add_text(s, x, y, fs, color=TITLE_C, weight="normal", ha="center",
             va="center", style="normal"):
    texts.append(dict(s=s, x=x, y=y, fs=fs, color=color, weight=weight,
                      ha=ha, va=va, style=style))

# ---------------------------------------------------------------------------
# vertical rhythm of a box interior (shared by both boxes so rows align)
#   TITLE_H | SCENE_H | H_TALL | ROW_GAP | SCENE_H | H_TALL
BOX_INNER_H = TITLE_H + 2 * (SCENE_H + H_TALL) + ROW_GAP

def row_y(iy, box_top):
    """top-y of the tiles in cell-row iy (0 or 1) of a box whose interior top
    is box_top."""
    base = box_top + TITLE_H + SCENE_H
    return base + iy * (H_TALL + ROW_GAP + SCENE_H)

def scene_label_y(iy, box_top):
    return row_y(iy, box_top) - SCENE_H * 0.42

# ===========================================================================
# LEFT box : SAVNav (Ours), Mixed Home Activity  (3 x 2 tiles)
# ===========================================================================
lx = MARGIN + BOX_PAD
ly = MARGIN

OURS_ROWS = [
    (["door1", "door2", "door3"], "Target: doorbell"),
    (["tv1", "tv2", "tv3"],       "Target: television"),
]
for iy, (keys, tgt) in enumerate(OURS_ROWS):
    yt = row_y(iy, ly)
    for j, k in enumerate(keys):
        x = lx + j * (COL_W + SEQ_GAP)
        add_img(k, x, yt)
        if j > 0:
            harrows.append((x - SEQ_GAP / 2, yt + H_TALL * 0.5))
    row_w = 3 * COL_W + 2 * SEQ_GAP
    add_text(tgt, lx + row_w / 2, scene_label_y(iy, ly), fs=13,
             color=TARGET_C, weight="bold")

LEFT_W = 3 * COL_W + 2 * SEQ_GAP
boxes.append(dict(x=lx, y=ly, w=LEFT_W, h=BOX_INNER_H, accent=ACC["mixed"]))

# left box header: scene name (top-left) then method (centered) -- sim style
add_text("Mixed Home Activity", lx, ly + TITLE_H * 0.20, fs=16,
         color=ACC["mixed"], weight="bold", ha="left")
add_text("SAVNav (Ours)", lx + LEFT_W / 2, ly + TITLE_H * 0.58, fs=15,
         color=OURS_C, weight="bold")

# ===========================================================================
# RIGHT box : w/o Topology-Aware Acoustic Anticipation, Hidden Boundary (1x2)
# ===========================================================================
rx = lx + LEFT_W + BOX_PAD + GAP_BOX + BOX_PAD
ry = ly

ABL_COL = ["abl1", "abl2"]
for iy, k in enumerate(ABL_COL):
    yt = row_y(iy, ry)
    add_img(k, rx, yt)
# downward temporal arrow between abl1 and abl2 (centered in the inter-row gap)
y_top_bottom = row_y(0, ry) + H_TALL
y_bot_top    = row_y(1, ry)
varrows.append((rx + COL_W / 2, (y_top_bottom + y_bot_top) / 2))

RIGHT_W = COL_W
boxes.append(dict(x=rx, y=ry, w=RIGHT_W, h=BOX_INNER_H, accent=ACC["nlos"]))

# right box header: scene name (centered above a narrow column) then method.
# The NLOS box is a single tile wide, so both lines are centred and the method
# is set a touch smaller to keep the longer name off the box walls.
add_text("Hidden Boundary", rx + RIGHT_W / 2, ry + TITLE_H * 0.20, fs=16,
         color=ACC["nlos"], weight="bold")
add_text("w/o Topology-Aware\nAcoustic Anticipation", rx + RIGHT_W / 2,
         ry + TITLE_H * 0.60, fs=11, color=ABL_C, weight="bold")
# per-episode target label above the ablation column
add_text("Target: doorbell", rx + RIGHT_W / 2, scene_label_y(0, ry), fs=13,
         color=TARGET_C, weight="bold")

# ===========================================================================
# Canvas
# ===========================================================================
Ltot = rx + RIGHT_W + BOX_PAD + MARGIN
Htot = ly + BOX_INNER_H + MARGIN
U_PER_IN = 380.0     # match the sim figure so fonts/tiles share the same scale
fig = plt.figure(figsize=(Ltot / U_PER_IN, Htot / U_PER_IN))

def to_frac(x, ytop, w, h):
    return [x / Ltot, (Htot - ytop - h) / Htot, w / Ltot, h / Htot]
def uy(ytop):
    return Htot - ytop
def tint(hexc, t=0.07):
    r, g, b = matplotlib.colors.to_rgb(hexc)
    return (r + (1 - r) * (1 - t), g + (1 - g) * (1 - t), b + (1 - b) * (1 - t))

# background: accent boxes ----------------------------------------------------
bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, Ltot); bg.set_ylim(0, Htot)
bg.axis("off"); bg.set_zorder(0); bg.patch.set_alpha(0)
for b in boxes:
    x, ytop, w, h = b["x"], b["y"], b["w"], b["h"]
    pad = BOX_PAD
    bg.add_patch(FancyBboxPatch(
        (x - pad, uy(ytop + h) - pad), w + 2 * pad, h + 2 * pad,
        boxstyle="round,pad=0,rounding_size=36",
        linewidth=1.6, edgecolor=b["accent"], facecolor=tint(b["accent"])))

# images ----------------------------------------------------------------------
for key, x, ytop, w, h in panels:
    ax = fig.add_axes(to_frac(x, ytop, w, h))
    ax.imshow(IMG[key], interpolation="none")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_zorder(5)
    oc = outcome_for(key)
    if SHOW_OUTCOME_FRAMES and oc:
        ecol, elw = OUTCOME_C[oc], 3.6
    else:
        ecol, elw = "#c3c7cc", 0.7
    for s in ax.spines.values():
        s.set_visible(True); s.set_edgecolor(ecol); s.set_linewidth(elw)
        s.set_zorder(8)
    if SHOW_STEP_LABELS:
        st = step_for(key)
        if st is not None:
            ax.text(0.970, 0.030, f"Step {st}", transform=ax.transAxes,
                    ha="right", va="bottom", fontsize=9, color="white",
                    weight="bold", zorder=12,
                    bbox=dict(boxstyle="round,pad=0.30",
                              facecolor=(0.10, 0.11, 0.12, 0.85),
                              edgecolor=(1, 1, 1, 0.55), linewidth=0.6))

# foreground: titles, labels, arrows -----------------------------------------
fg = fig.add_axes([0, 0, 1, 1]); fg.set_xlim(0, Ltot); fg.set_ylim(0, Htot)
fg.axis("off"); fg.set_zorder(20); fg.patch.set_alpha(0)
for t in texts:
    if not t["s"]:
        continue
    fg.text(t["x"], uy(t["y"]), t["s"], fontsize=t["fs"], color=t["color"],
            weight=t["weight"], ha=t["ha"], va=t["va"], style=t["style"],
            linespacing=0.98)
for xm, yc in harrows:
    Y = uy(yc); half = SEQ_GAP * 0.34
    fg.annotate("", xy=(xm + half, Y), xytext=(xm - half, Y),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_C, lw=2.2,
                                mutation_scale=16, shrinkA=0, shrinkB=0))
for xc, ym in varrows:
    X = xc; half = (ROW_GAP + SCENE_H) * 0.33   # match the row arrows' gap-fill
    fg.annotate("", xy=(X, uy(ym) - half), xytext=(X, uy(ym) + half),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_C, lw=2.2,
                                mutation_scale=16, shrinkA=0, shrinkB=0))

# outcome legend, drawn by hand in the slim channel between the two boxes: each
# entry is a rotated label (reading bottom->top) sitting directly *above* its
# colour swatch, the two entries (Collision over Success) stacked and roughly
# centred so the channel stays narrow.
if SHOW_OUTCOME_FRAMES:
    cx = lx + LEFT_W + BOX_PAD + GAP_BOX / 2   # channel centre x (u)
    cy = ly + BOX_INNER_H / 2                  # channel mid-height (u, top-down)
    sw = 42.0                                  # swatch side (u)
    tgap = 22.0                                # label-bottom -> swatch-top gap (u)
    y0 = cy - 43.0                             # top edge of the first swatch (u)
    pitch = 340.0                              # swatch-top -> swatch-top (u)
    for i, o in enumerate(("collision", "success")):
        y_sw = y0 + i * pitch
        fg.add_patch(Rectangle((cx - sw / 2, uy(y_sw + sw)), sw, sw,
                               facecolor=OUTCOME_C[o], edgecolor="none",
                               zorder=22))
        # rotation=90 with ha="center"/va="bottom" centres the rotated label on the
        # swatch's vertical axis (cx) and rests its bottom edge tgap above the swatch
        # top, so the label reads bottom->top directly *above* its colour block (in
        # the figure's own up-direction, not offset to one side).
        fg.text(cx, uy(y_sw - tgap), OUTCOME_LABEL[o], rotation=90,
                ha="center", va="bottom", fontsize=12, color=TITLE_C, zorder=22)

out_pdf = os.path.join(ROOT, "figures", "exp-q-real.pdf")
out_png = os.path.join(ROOT, "figures", "exp-q-real.png")
fig.savefig(out_pdf, dpi=PDF_DPI)
fig.savefig(out_png, dpi=150)
print("wrote", out_pdf, "and", out_png)
print("canvas u:", round(Ltot), "x", round(Htot), " aspect", round(Ltot / Htot, 3))
print("figsize in:", round(Ltot / U_PER_IN, 2), "x", round(Htot / U_PER_IN, 2))
