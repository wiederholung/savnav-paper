#!/usr/bin/env python
"""Compose figures/exp-q-sim.pdf : qualitative comparison across the three
SAVNav scenarios (Crowded Social / Hidden Boundary / Mixed Home Activity).

Layout (matches the user's sketch):
  Top-left  = LOS  region : Ours x2 (tall)  over  Falcon x1 + ENMuS3 x1 (wide)
  Top-right = NLOS region : Ours x3 (tall)  over  Falcon x2 + ENMuS3 x1 (wide)
  Bottom    = Mixed region: Ours x3 | w/o Active Sensory Exploration x1 |
                            w/o Topology-Aware Anticipation x1   (all tall)

Alignment guarantees:
  * the two top regions are rendered at EQUAL height (wide row bottom-aligned);
  * the Mixed region spans EXACTLY the combined width of the two top regions
    (its groups are justified edge-to-edge).

Multi-frame temporal sequences (Ours x2/x3, Falcon x2) get a small arrow between
consecutive keyframes to indicate time order.

Source frames are embedded at full resolution (no downsampling); flate (lossless)
stream compression only.  All geometry is in abstract "u" units, top-down
(y grows downward), converted to matplotlib bottom-up fractions at render time so
image aspect ratios are never distorted (figure physical aspect == u-space aspect).
"""
import os
import re
import argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Patch
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "figures", "qualitative_exp", "sim")

# ---- optional features (both default ON) -----------------------------------
_ap = argparse.ArgumentParser(description="Compose figures/exp-q-sim.pdf")
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

# resolution at which the raster panels are embedded into the PDF.  The figure is
# ~9.8 in wide and is placed at ~7.16 in (\linewidth) in the paper, so on-page dpi
# = PDF_DPI * 9.8/7.16.  700 -> panels embedded near their source pixel size, crisp
# enough to zoom into the internal legends/maps on screen.
PDF_DPI = 700

# ---- source frames ----------------------------------------------------------
# Terminal keyframes carry an outcome tag in the filename (__success / __collision
# / __unreached); non-terminal frames do not.  This is the single source of truth
# for the outcome border going forward.
F = {
    "los_ours1":  "los-ep0-ours.mp4_000006.720.png",
    "los_ours2":  "los-ep0-ours.mp4_000010.176__success.png",
    "los_falcon": "los-ep0-falcon.mp4_000024.021__unreached.png",
    "los_enmus":  "los-ep0-enmus.mp4_000024.021__unreached.png",
    "nlos_ours1": "nlos-ep785-ours.mp4_000007.247.png",
    "nlos_ours2": "nlos-ep785-ours.mp4_000008.804.png",
    "nlos_ours3": "nlos-ep785-ours.mp4_000014.357__success.png",
    "nlos_falcon1": "nlos-ep785-falocn.mp4_000021.218.png",
    "nlos_falcon2": "nlos-ep785-falocn.mp4_000022.005__collision.png",
    "nlos_enmus": "nlos-ep1-enmus.mp4_000009.045__collision.png",
    "mix_ours1":  "mixed-ep3-ours.mp4_000004.865.png",
    "mix_ours2":  "mixed-ep3-ours.mp4_000008.687.png",
    "mix_ours3":  "mixed-ep3-ours.mp4_000012.673__success.png",
    "mix_nosearch": "mixed-ep3-ours_no_search.mp4_000019.058__unreached.png",
    "mix_noaudio":  "mixed-ep3-ours_no_audio_cost.mp4_20260714_004116.962__collision.png",
}
IMG = {k: Image.open(os.path.join(SRC, v)) for k, v in F.items()}
def ar(k):  # aspect ratio w/h
    return IMG[k].size[0] / IMG[k].size[1]

# ---- step number per keyframe ----------------------------------------------
# The sim logical frame rate (1/update_dt) is ~20.83 Hz (drafts/savnav_impl.md),
# so a frame's step is derivable from the "<t>" in "*.mp4_<t>.png" as round(t*FPS).
# The sim's effective fps jitters by a frame or two, so we pin the EXACT step read
# from each frame's baked "Step" overlay; filename derivation is the fallback for
# any new/un-pinned frame (and the only option for frames lacking a video timestamp).
FPS_SIM = 20.83
STEP_EXACT = {
    "los_ours1": 141, "los_ours2": 213, "los_falcon": 498, "los_enmus": 498,
    "nlos_ours1": 152, "nlos_ours2": 185, "nlos_ours3": 299,
    "nlos_falcon1": 443, "nlos_falcon2": 456, "nlos_enmus": 186,
    "mix_ours1": 103, "mix_ours2": 182, "mix_ours3": 265,
    "mix_nosearch": 398, "mix_noaudio": 182,
}
def step_for(k):
    if k in STEP_EXACT:
        return STEP_EXACT[k]
    m = re.search(r"\.mp4_(\d+\.\d+)(?:__|\.png)", F[k])
    return round(float(m.group(1)) * FPS_SIM) if m else None

# ---- outcome per keyframe (parsed from the filename tag) --------------------
OUTCOME_C = {"success": "#1a9850", "collision": "#d62728", "unreached": "#f0a020"}
OUTCOME_LABEL = {"success": "Success", "collision": "Collision",
                 "unreached": "Not reached"}
def outcome_for(k):
    m = re.search(r"__(success|collision|unreached)\.png$", F[k])
    return m.group(1) if m else None

# ---- palette ----------------------------------------------------------------
OURS_C  = "#0b6b3a"   # green  -> our method
BASE_C  = "#2f3437"   # dark   -> baselines
ABL_C   = "#b5651d"   # ochre  -> ablations
TITLE_C = "#111417"
ARROW_C = "#464b52"   # slate  -> temporal-sequence arrow
ACC = {"los": "#2f6db5", "nlos": "#c0392b", "mixed": "#6d4c9f"}

# ---- layout parameters (u-space) -------------------------------------------
H_TALL     = 1000.0    # height of a tall (portrait) panel
SEQ_GAP    = 96.0      # gap between consecutive frames (hosts the sequence arrow)
GAP_REGION = 150.0     # gap between LOS and NLOS
GAP_V      = 172.0     # gap between top block and Mixed block (holds outcome legend)
TITLE_H    = 86.0      # band reserved above a region for its title
METHOD_H   = 58.0      # band reserved above a sub-row for method labels
ROW_GAP    = 34.0      # min gap between the tall sub-row and the wide sub-row
MARGIN     = 74.0      # outer margin

panels = []   # (key, x, ytop, w, h)
texts  = []   # dict
boxes  = []   # dict(x,ytop,w,h,accent,title)
arrows = []   # (x_mid, y_center)  top-down u

def add_img(key, x, ytop, w, h):
    panels.append((key, x, ytop, w, h))

def add_text(s, x, ytop, fs, color=TITLE_C, weight="normal", ha="center",
             va="center"):
    texts.append(dict(s=s, x=x, y=ytop, fs=fs, color=color, weight=weight,
                      ha=ha, va=va))

def add_arrow(x_mid, y_center):
    arrows.append((x_mid, y_center))

# ---------------------------------------------------------------------------
def top_region_dims(tall_keys, wide_groups):
    """natural (width, height) of a top region."""
    N = len(tall_keys)
    col_w = H_TALL * ar(tall_keys[0])
    region_w = N * col_w + (N - 1) * SEQ_GAP
    all_wide = [k for keys, _, _ in wide_groups for k in keys]
    wide_h = col_w / max(ar(k) for k in all_wide)
    region_h = TITLE_H + METHOD_H + H_TALL + ROW_GAP + METHOD_H + wide_h
    return region_w, region_h, col_w, wide_h

# A top region (LOS / NLOS): N tall panels over N wide panels, rendered to a
# fixed region_h with the wide row bottom-aligned so LOS and NLOS match height.
def build_top_region(rx, ry, region_h, tall_keys, tall_label, wide_groups):
    N = len(tall_keys)
    _, _, col_w, wide_h = top_region_dims(tall_keys, wide_groups)
    region_w = N * col_w + (N - 1) * SEQ_GAP

    # tall row (top)
    y_tall = ry + TITLE_H + METHOD_H
    for i, k in enumerate(tall_keys):
        x = rx + i * (col_w + SEQ_GAP)
        add_img(k, x, y_tall, col_w, H_TALL)
        if i > 0:                                   # sequence arrow (Ours x N)
            add_arrow(x - SEQ_GAP / 2, y_tall + H_TALL * 0.5)
    add_text(tall_label, rx + region_w / 2, y_tall - METHOD_H * 0.52,
             fs=15, color=OURS_C, weight="bold")

    # wide row (bottom-aligned to region bottom)
    y_wide = ry + region_h - wide_h
    y_wlab = y_wide - METHOD_H
    cx = rx
    for keys, label, color in wide_groups:
        gw = len(keys) * col_w + (len(keys) - 1) * SEQ_GAP
        add_text(label, cx + gw / 2, y_wlab + METHOD_H * 0.42,
                 fs=13, color=color, weight="bold")
        for j, k in enumerate(keys):
            w = wide_h * ar(k)
            add_img(k, cx + (col_w - w) / 2, y_wide, w, wide_h)
            if j > 0:                               # sequence arrow (Falcon x2)
                add_arrow(cx - SEQ_GAP / 2, y_wide + wide_h * 0.5)
            cx += col_w + SEQ_GAP
    return region_w

# The Mixed region: horizontal groups of tall panels justified to total_w.
#   groups : list of (keys, label, color, fontsize)
def build_mixed_region(rx, ry, total_w, groups):
    col_w = {g[0][0]: H_TALL * ar(g[0][0]) for g in groups}
    group_w = [len(keys) * col_w[keys[0]] + (len(keys) - 1) * SEQ_GAP
               for keys, *_ in groups]
    gap = (total_w - sum(group_w)) / (len(groups) - 1)   # justify edge-to-edge
    y_tall = ry + TITLE_H + METHOD_H
    x = rx
    for gi, (keys, label, color, fs) in enumerate(groups):
        cw = col_w[keys[0]]
        gw = group_w[gi]
        add_text(label, x + gw / 2, y_tall - 16,
                 fs=fs, color=color, weight="bold", va="bottom")
        for j, k in enumerate(keys):
            add_img(k, x, y_tall, cw, H_TALL)
            if j > 0:                               # sequence arrow (Ours x3)
                add_arrow(x - SEQ_GAP / 2, y_tall + H_TALL * 0.5)
            x += cw + SEQ_GAP
        x = x - SEQ_GAP + gap
    return (y_tall + H_TALL) - ry

# ===========================================================================
# Place the three regions
# ===========================================================================
x0, y0 = MARGIN, MARGIN

LOS_TALL = ["los_ours1", "los_ours2"]
LOS_WIDE = [(["los_falcon"], "Falcon+Goal Oracle", BASE_C),
            (["los_enmus"],  "ENMuS³", BASE_C)]
NLOS_TALL = ["nlos_ours1", "nlos_ours2", "nlos_ours3"]
NLOS_WIDE = [(["nlos_falcon1", "nlos_falcon2"], "Falcon+Goal Oracle", BASE_C),
             (["nlos_enmus"], "ENMuS³", BASE_C)]

los_w,  los_h_nat,  _, _ = top_region_dims(LOS_TALL, LOS_WIDE)
nlos_w, nlos_h_nat, _, _ = top_region_dims(NLOS_TALL, NLOS_WIDE)
TOP_H = max(los_h_nat, nlos_h_nat)               # equal height for both regions

build_top_region(x0, y0, TOP_H, LOS_TALL, "SAVNav (Ours)", LOS_WIDE)
nlos_x = x0 + los_w + GAP_REGION
build_top_region(nlos_x, y0, TOP_H, NLOS_TALL, "SAVNav (Ours)", NLOS_WIDE)

boxes.append(dict(x=x0, y=y0, w=los_w, h=TOP_H, accent=ACC["los"],
                  title="Crowded Social"))
boxes.append(dict(x=nlos_x, y=y0, w=nlos_w, h=TOP_H, accent=ACC["nlos"],
                  title="Hidden Boundary"))

# --- bottom : Mixed spans the full combined width of the two top regions -----
TOP_W = los_w + GAP_REGION + nlos_w
mix_y = y0 + TOP_H + GAP_V
mix_h = build_mixed_region(
    x0, mix_y, TOP_W,
    [(["mix_ours1", "mix_ours2", "mix_ours3"], "SAVNav (Ours)", OURS_C, 15),
     (["mix_nosearch"], "w/o Active Sensory\nExploration", ABL_C, 12),
     (["mix_noaudio"],  "w/o Topology-Aware\nAnticipation", ABL_C, 12)],
)
boxes.append(dict(x=x0, y=mix_y, w=TOP_W, h=mix_h, accent=ACC["mixed"],
                  title="Mixed Home Activity"))

# ===========================================================================
# Canvas
# ===========================================================================
Ltot = x0 + TOP_W + MARGIN
Htot = mix_y + mix_h + MARGIN
U_PER_IN = 380.0
fig = plt.figure(figsize=(Ltot / U_PER_IN, Htot / U_PER_IN))

def to_frac(x, ytop, w, h):
    return [x / Ltot, (Htot - ytop - h) / Htot, w / Ltot, h / Htot]
def uy(ytop):
    return Htot - ytop
def tint(hexc, t=0.07):
    r, g, b = matplotlib.colors.to_rgb(hexc)
    return (r + (1 - r) * (1 - t), g + (1 - g) * (1 - t), b + (1 - b) * (1 - t))

# background: region boxes ----------------------------------------------------
bg = fig.add_axes([0, 0, 1, 1]); bg.set_xlim(0, Ltot); bg.set_ylim(0, Htot)
bg.axis("off"); bg.set_zorder(0); bg.patch.set_alpha(0)
for b in boxes:
    x, ytop, w, h = b["x"], b["y"], b["w"], b["h"]
    pad = 30
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
    # outcome border: coloured + thick on terminal frames, subtle grey otherwise
    oc = outcome_for(key)
    if SHOW_OUTCOME_FRAMES and oc:
        ecol, elw = OUTCOME_C[oc], 3.6
    else:
        ecol, elw = "#c3c7cc", 0.7
    for s in ax.spines.values():
        s.set_visible(True); s.set_edgecolor(ecol); s.set_linewidth(elw)
        s.set_zorder(8)
    # step badge, top-left of the panel
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
for b in boxes:
    fg.text(b["x"] + 4, uy(b["y"] + TITLE_H * 0.46), b["title"], fontsize=17,
            color=b["accent"], weight="bold", ha="left", va="center")
for t in texts:
    if not t["s"]:
        continue
    fg.text(t["x"], uy(t["y"]), t["s"], fontsize=t["fs"], color=t["color"],
            weight=t["weight"], ha=t["ha"], va=t["va"], linespacing=0.95)
for xm, yc in arrows:
    Y = uy(yc)
    half = SEQ_GAP * 0.34
    fg.annotate("", xy=(xm + half, Y), xytext=(xm - half, Y),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_C, lw=2.2,
                                mutation_scale=16, shrinkA=0, shrinkB=0))

# outcome legend, centered in the band between the top regions and Mixed -------
if SHOW_OUTCOME_FRAMES:
    lax = fig.add_axes(to_frac(x0, y0 + TOP_H, TOP_W, GAP_V))
    lax.axis("off")
    handles = [Patch(facecolor=OUTCOME_C[o], edgecolor="none",
                     label=OUTCOME_LABEL[o])
               for o in ("success", "collision", "unreached")]
    lax.legend(handles=handles, ncol=3, loc="center", frameon=False,
               fontsize=12.5, handlelength=1.15, handleheight=1.15,
               columnspacing=1.9)

out_pdf = os.path.join(ROOT, "figures", "exp-q-sim.pdf")
out_png = os.path.join(ROOT, "figures", "exp-q-sim.png")
fig.savefig(out_pdf, dpi=PDF_DPI)
fig.savefig(out_png, dpi=150)
print("wrote", out_pdf, "and", out_png)
print("canvas u:", round(Ltot), "x", round(Htot), " aspect", round(Ltot / Htot, 3))
print("figsize in:", round(Ltot / U_PER_IN, 2), "x", round(Htot / U_PER_IN, 2))
print("TOP_W:", round(TOP_W), " mixed_w:", round(TOP_W),
      " los_h==nlos_h:", round(TOP_H))
