#!/usr/bin/env python3
"""Render the Chess Clock app icons — digital LCD face, no external assets."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyBboxPatch

# --- seven-segment geometry (same numbers as index.html) ---
DW, DH, T, PAD, GAP = 60, 104, 13, 3, 2.2
ADV = DW + 6
yT, yM, yB = PAD + T / 2, DH / 2, DH - PAD - T / 2
xL, xR = PAD + T / 2, DW - PAD - T / 2


def hs(y, x1, x2):
    t = T / 2; x1 += GAP; x2 -= GAP
    return [(x1, y), (x1 + t, y - t), (x2 - t, y - t), (x2, y), (x2 - t, y + t), (x1 + t, y + t)]


def vs(x, y1, y2):
    t = T / 2; y1 += GAP; y2 -= GAP
    return [(x, y1), (x + t, y1 + t), (x + t, y2 - t), (x, y2), (x - t, y2 - t), (x - t, y1 + t)]


PTS = {"a": hs(yT, xL, xR), "g": hs(yM, xL, xR), "d": hs(yB, xL, xR),
       "f": vs(xL, yT, yM), "b": vs(xR, yT, yM), "e": vs(xL, yM, yB), "c": vs(xR, yM, yB)}
SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fbgc",
       "5": "afgcd", "6": "afgecd", "7": "abc", "8": "abcdefg", "9": "abfgcd", " ": ""}

BG   = "#000000"   # case — black frame
LCD  = "#a6b497"   # display glass — liquid crystal green-grey
LIT  = "#151f0e"   # lit segment
OFF  = 0.10        # ghost opacity


def digits(ax, s, ox, oy, sc):
    x = 0
    for ch in s:
        if ch == ":":
            for cy in (DH * 0.33, DH * 0.70):
                ax.add_patch(Circle((ox + (x + 11) * sc, oy + cy * sc), 6.5 * sc, color=LIT, zorder=5))
            x += 23
        else:
            on = SEG.get(ch, "")
            for k in "abcdefg":
                ax.add_patch(Polygon([(ox + (px + x) * sc, oy + py * sc) for px, py in PTS[k]],
                                     color=LIT, alpha=1.0 if k in on else OFF, zorder=5))
            x += ADV
    return max(0, x - 6) * sc


def render(px, path):
    fig = plt.figure(figsize=(px / 100, px / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 512); ax.set_ylim(512, 0); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 512, 512, color=BG, zorder=0))

    # display glass
    X0, X1, Y0, GH = 44, 468, 156, 200
    ax.add_patch(FancyBboxPatch((X0, Y0), X1 - X0, GH,
                                boxstyle="round,pad=0,rounding_size=26",
                                facecolor=LCD, edgecolor="#20281c", lw=3, zorder=1))

    # two two-digit groups with a centre gap for the arrow — positions derived,
    # so the digits can never collide with each other or with the arrow
    MARGIN, CGAP = 34, 62
    group = ((X1 - X0) - 2 * MARGIN - CGAP) / 2
    sc = group / (2 * ADV - 6)
    top = Y0 + (GH - DH * sc) / 2
    digits(ax, "30", X0 + MARGIN, top, sc)
    digits(ax, "30", X1 - MARGIN - group, top, sc)

    # turn arrow, centred in the gap
    aw, ah = 28, 34
    cx, cy = (X0 + X1) / 2, Y0 + GH / 2
    ax.add_patch(Polygon([(cx + aw / 2, cy - ah / 2), (cx + aw / 2, cy + ah / 2),
                          (cx - aw / 2, cy)], color=LIT, zorder=5))

    fig.savefig(path, dpi=100, facecolor=BG)
    plt.close(fig)
    print("wrote", path, px)


render(512, "icon-512.png")
render(180, "icon-180.png")
