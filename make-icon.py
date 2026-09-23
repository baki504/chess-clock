#!/usr/bin/env python3
"""Render the Chess Clock app icons (no external assets)."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

BG   = "#0d1420"
BODY = "#2c3847"
EDGE = "#3d4b5e"
IDLE = "#eef2f7"
ACT  = "#22c55e"
DARK = "#111a26"


def hand(ax, cx, cy, angle_deg, length, width, color):
    a = math.radians(90 - angle_deg)
    ax.plot([cx, cx + length * math.cos(a)],
            [cy, cy + length * math.sin(a)],
            color=color, lw=width, solid_capstyle="round", zorder=6)


def render(px, path):
    fig = plt.figure(figsize=(px / 100, px / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=BG, zorder=0))

    s = px / 512.0  # line widths scale with size

    # plungers on top
    for x in (0.235, 0.645):
        ax.add_patch(FancyBboxPatch((x, 0.735), 0.12, 0.055,
                                    boxstyle="round,pad=0,rounding_size=0.025",
                                    facecolor=EDGE, edgecolor="none", zorder=2))
    # body
    ax.add_patch(FancyBboxPatch((0.075, 0.215), 0.85, 0.525,
                                boxstyle="round,pad=0,rounding_size=0.09",
                                facecolor=BODY, edgecolor="none", zorder=3))
    # dials
    for cx, face, h_m, h_h in ((0.295, IDLE, 20, 140), (0.705, ACT, -15, 110)):
        ax.add_patch(Circle((cx, 0.478), 0.155, facecolor=face,
                            edgecolor=DARK, lw=3 * s, zorder=5))
        hand(ax, cx, 0.478, h_h, 0.075, 9 * s, DARK)   # hour
        hand(ax, cx, 0.478, h_m, 0.115, 6 * s, DARK)   # minute
        ax.add_patch(Circle((cx, 0.478), 0.016, facecolor=DARK,
                            edgecolor="none", zorder=7))

    fig.savefig(path, dpi=100, facecolor=BG)
    plt.close(fig)
    print("wrote", path, px)


render(512, "icon-512.png")
render(180, "icon-180.png")
