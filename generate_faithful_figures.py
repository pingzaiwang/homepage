#!/usr/bin/env python3
"""
Generate 100% faithful, empirical publication-grade figures for the SPReAD project.
EVERY number plotted is exact and traceable to source_data.txt and HANDOFF.md:

- Fig 1: Training-Free Premise Test (Coupling probe AAC/PAC & Dispersion probe per-band vs scalar)
- Fig 3: Single-Variable Geometry Decomposition (LOSO balanced accuracy on BNCI n=9 and Sleep n=12)

Compliant with Nature / ICLR graphic standards:
- Exact data points plotted with jitter
- Exact means and standard deviations
- Colorblind-safe Wong palette
- 300+ DPI PNG and vector PDF output
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

# Global matplotlib settings
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "axes.unicode_minus": False,
    "mathtext.fontset": "cm",
    "font.size": 9.0,
    "axes.labelsize": 9.5,
    "axes.titlesize": 10.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8.5,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

OUT_DIR = "/Users/antonw/Code/AI4S/spread_homepage/assets"
os.makedirs(OUT_DIR, exist_ok=True)

# Colorblind-safe Wong Palette
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
VERMILLION = "#D55E00"
GREY = "#64748B"
DARK_NAVY = "#0F172A"
LIGHT_BG = "#F8FAFC"
BORDER_COLOR = "#E2E8F0"

rng = np.random.default_rng(42)

def jitter(n, w=0.08):
    return (rng.random(n) - 0.5) * 2 * w

# ==============================================================================
# EXACT REAL DATA (Source: source_data.txt / HANDOFF.md Section 6 / paper/main.tex)
# ==============================================================================

# Premise Probe 1: Coupling probe (AAC/PAC) - within-subject 5-fold CV balanced acc (%)
coup_data = {
    "Power A": {"BNCI": 57.3, "Sleep": 82.1},
    "AAC":      {"BNCI": 28.5, "Sleep": 65.5},
    "PAC":      {"BNCI": 25.9, "Sleep": 53.9},
}

# Premise Probe 2: Dispersion probe (per-band tube vs pooled scalar) - balanced acc (%)
disp_data = {
    "Power A":              {"BNCI": 52.3, "Sleep": 82.5},
    "Per-band (Tube)":      {"BNCI": 26.2, "Sleep": 75.1},
    "Pooled (Scalar)":      {"BNCI": 26.2, "Sleep": 56.5},
}

# Geometry Results: LOSO balanced accuracy (%) per domain / subject
geo_data = {
    "BNCI2014_001 Motor Imagery (n=9 folds)": {
        "chance": 25.0,
        "Product (EEG-MoCE)":   [66.7, 70.5, 46.9, 47.6, 73.3, 75.3, 55.2, 48.6, 42.0],
        "+ Coupling L":         [71.5, 72.2, 39.9, 39.9, 76.7, 73.6, 48.3, 51.0, 39.9],
        "+ Tube Dispersion":    [69.4, 66.7, 46.2, 38.2, 73.6, 65.6, 53.1, 53.8, 40.3],
    },
    "Sleep-EDF Staging (n=12 subjects)": {
        "chance": 20.0,
        "Product (EEG-MoCE)":   [45.9, 40.0, 50.6, 48.1, 42.7, 42.7, 38.7, 42.0, 72.7, 78.5, 40.6, 32.9],
        "+ Coupling L":         [78.3, 37.0, 79.7, 36.4, 76.9, 41.6, 85.4, 37.8, 36.5, 28.4, 40.0, 69.8],
        "+ Tube Dispersion":    [76.0, 80.8, 80.5, 82.9, 77.3, 82.7, 84.7, 82.3, 81.0, 72.7, 73.0, 64.9],
    }
}


# ==============================================================================
# FIGURE 1: TRAINING-FREE PREMISE TEST PROBES (COUPING & DISPERSION)
# ==============================================================================
def generate_figure1():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2), constrained_layout=True)
    fig.patch.set_facecolor("white")

    # --- Panel A: Coupling Probe ---
    keys1 = list(coup_data.keys())
    x1 = np.arange(len(keys1))
    w = 0.35

    ax1.set_facecolor("white")
    ax1.grid(axis="y", linestyle="--", alpha=0.4, color=BORDER_COLOR, zorder=0)

    # BNCI Bars
    b1_bnci = ax1.bar(x1 - w/2, [coup_data[k]["BNCI"] for k in keys1], width=w,
                      color=GREY, alpha=0.85, edgecolor=DARK_NAVY, linewidth=0.8,
                      label="BNCI-2a Motor Imagery", zorder=2)
    # Sleep Bars
    b1_sleep = ax1.bar(x1 + w/2, [coup_data[k]["Sleep"] for k in keys1], width=w,
                       color=BLUE, alpha=0.85, edgecolor=DARK_NAVY, linewidth=0.8,
                       label="Sleep-EDF Staging", zorder=2)

    # Chance levels
    ax1.axhline(25, ls="--", lw=1.0, color=GREY, alpha=0.8, zorder=1)
    ax1.text(2.35, 26, "Chance (BNCI: 25%)", fontsize=7.5, color=GREY, ha="right")
    ax1.axhline(20, ls=":", lw=1.0, color=BLUE, alpha=0.8, zorder=1)
    ax1.text(2.35, 15, "Chance (Sleep: 20%)", fontsize=7.5, color=BLUE, ha="right")

    ax1.set_xticks(x1)
    ax1.set_xticklabels(keys1, fontweight="bold")
    ax1.set_ylabel("Within-Subject CV Balanced Acc. (%)", fontweight="bold")
    ax1.set_ylim(0, 100)
    ax1.set_title("(a) Coupling Probe: Amplitude-Phase Coupling", fontweight="bold", pad=12)
    ax1.legend(frameon=True, facecolor="white", edgecolor=BORDER_COLOR, loc="upper right")

    # Callout: Coupling is near chance on BNCI but discriminative on Sleep
    ax1.text(1.5, 42, "Coupling at Chance\non Motor Imagery", ha="center", fontsize=7.8,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF2F2", edgecolor="#FECACA", lw=0.8))

    # --- Panel B: Dispersion Probe ---
    keys2 = ["Power A", "Per-band (Tube)", "Pooled (Scalar)"]
    x2 = np.arange(len(keys2))

    ax2.set_facecolor("white")
    ax2.grid(axis="y", linestyle="--", alpha=0.4, color=BORDER_COLOR, zorder=0)

    # BNCI Bars
    b2_bnci = ax2.bar(x2 - w/2, [disp_data[k]["BNCI"] for k in keys2], width=w,
                      color=GREY, alpha=0.85, edgecolor=DARK_NAVY, linewidth=0.8,
                      label="BNCI-2a Motor Imagery", zorder=2)
    # Sleep Bars
    b2_sleep = ax2.bar(x2 + w/2, [disp_data[k]["Sleep"] for k in keys2], width=w,
                       color=BLUE, alpha=0.85, edgecolor=DARK_NAVY, linewidth=0.8,
                       label="Sleep-EDF Staging", zorder=2)

    # Chance levels
    ax2.axhline(25, ls="--", lw=1.0, color=GREY, alpha=0.8, zorder=1)
    ax2.axhline(20, ls=":", lw=1.0, color=BLUE, alpha=0.8, zorder=1)

    # Annotate the exact +18.6 pp gain
    ax2.annotate("", xy=(1 + w/2, 75.1), xytext=(2 + w/2, 56.5),
                 arrowprops=dict(arrowstyle="<-", lw=1.4, color=BLUE))
    ax2.text(1.5 + w/2, 68, "+18.6 pp\n(p < 0.01)", fontsize=8.0, fontweight="bold",
             ha="center", color=BLUE, bbox=dict(boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#93C5FD", lw=0.6))

    # Annotate BNCI 0.0 pp
    ax2.text(1.5 - w/2, 30, "Delta = +0.0 pp\n(Null)", fontsize=7.5, ha="center", color=GREY)

    ax2.set_xticks(x2)
    ax2.set_xticklabels(keys2, fontweight="bold")
    ax2.set_ylabel("Within-Subject CV Balanced Acc. (%)", fontweight="bold")
    ax2.set_ylim(0, 100)
    ax2.set_title("(b) Dispersion Probe: Tube vs. Scalar Dispersion", fontweight="bold", pad=12)
    ax2.legend(frameon=True, facecolor="white", edgecolor=BORDER_COLOR, loc="upper right")

    # Save outputs
    png_path = os.path.join(OUT_DIR, "fig1_structural_gap.png")
    pdf_path = os.path.join(OUT_DIR, "fig1_structural_gap.pdf")
    fig.savefig(png_path, bbox_inches="tight", dpi=300)
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Fig 1 generated from REAL numbers: {png_path}")


# ==============================================================================
# FIGURE 3: SINGLE-VARIABLE GEOMETRY & MECHANISM DECOMPOSITION (REAL LOSO DATA)
# ==============================================================================
def generate_figure3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.4), constrained_layout=True)
    fig.patch.set_facecolor("white")

    arms = ["Product\n(EEG-MoCE)", "+ Coupling L\n(Scalar Disp.)", "+ Tube Disp.\n(Tubal Lorentz)"]
    arm_colors = [GREY, ORANGE, BLUE]

    # --- Panel A: BNCI Motor Imagery (n=9 folds) ---
    d_bnci = geo_data["BNCI2014_001 Motor Imagery (n=9 folds)"]
    ax1.set_facecolor("white")
    ax1.grid(axis="y", linestyle="--", alpha=0.4, color=BORDER_COLOR, zorder=0)

    for i, a_key in enumerate(["Product (EEG-MoCE)", "+ Coupling L", "+ Tube Dispersion"]):
        vals = np.array(d_bnci[a_key])
        m, sd = vals.mean(), vals.std()

        # Bar
        ax1.bar(i, m, width=0.55, color=arm_colors[i], alpha=0.35,
                edgecolor=arm_colors[i], linewidth=1.2, zorder=1)
        # Error bar
        ax1.errorbar(i, m, yerr=sd, fmt="none", ecolor=DARK_NAVY, elinewidth=1.2, capsize=3.5, zorder=2)
        # Scatter individual points
        ax1.scatter(i + jitter(len(vals)), vals, s=28, color=arm_colors[i],
                    edgecolors=DARK_NAVY, linewidths=0.6, zorder=3, alpha=0.9)
        # Print mean text
        ax1.text(i, m + sd + 2.5, f"{m:.1f}%", ha="center", fontsize=8.2, fontweight="bold", color=arm_colors[i])

    ax1.axhline(d_bnci["chance"], ls="--", lw=1.0, color="black", zorder=1)
    ax1.text(2.35, d_bnci["chance"] + 1.2, "Chance (25%)", fontsize=7.5, color="black", ha="right")

    ax1.set_xticks(range(3))
    ax1.set_xticklabels(arms, fontweight="bold")
    ax1.set_ylim(20, 95)
    ax1.set_ylabel("LOSO Balanced Accuracy (%)", fontweight="bold")
    ax1.set_title("(a) BNCI2014_001 Motor Imagery (n=9 folds)\nHonest Null Result (All p > 0.65 n.s.)", fontweight="bold", pad=12)

    # --- Panel B: Sleep-EDF Staging (n=12 subjects) ---
    d_sleep = geo_data["Sleep-EDF Staging (n=12 subjects)"]
    ax2.set_facecolor("white")
    ax2.grid(axis="y", linestyle="--", alpha=0.4, color=BORDER_COLOR, zorder=0)

    for i, a_key in enumerate(["Product (EEG-MoCE)", "+ Coupling L", "+ Tube Dispersion"]):
        vals = np.array(d_sleep[a_key])
        m, sd = vals.mean(), vals.std()

        ax2.bar(i, m, width=0.55, color=arm_colors[i], alpha=0.35,
                edgecolor=arm_colors[i], linewidth=1.2, zorder=1)
        ax2.errorbar(i, m, yerr=sd, fmt="none", ecolor=DARK_NAVY, elinewidth=1.2, capsize=3.5, zorder=2)
        ax2.scatter(i + jitter(len(vals)), vals, s=28, color=arm_colors[i],
                    edgecolors=DARK_NAVY, linewidths=0.6, zorder=3, alpha=0.9)
        ax2.text(i, m + sd + 2.5, f"{m:.1f}%", ha="center", fontsize=8.2, fontweight="bold", color=arm_colors[i])

    ax2.axhline(d_sleep["chance"], ls="--", lw=1.0, color="black", zorder=1)
    ax2.text(2.35, d_sleep["chance"] + 1.2, "Chance (20%)", fontsize=7.5, color="black", ha="right")

    # Annotate the mechanism breakdown
    # 1. Total Gain
    ax2.annotate("", xy=(2, 88.5), xytext=(0, 88.5),
                 arrowprops=dict(arrowstyle="->", lw=1.4, color=BLUE))
    ax2.text(1.0, 90.5, "Total Win: +30.3 pp (p = 0.001)", ha="center", fontsize=8.0, fontweight="bold", color=BLUE)

    # 2. Coupling alone
    ax2.text(0.5, 66.0, "Coupling alone:\n+6.0 pp (p=0.49 n.s.)", ha="center", fontsize=7.5, color=ORANGE,
             bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFBEB", edgecolor="#FDE68A", lw=0.6))

    # 3. Tube dispersion alone
    ax2.annotate("", xy=(2, 83.5), xytext=(1, 83.5),
                 arrowprops=dict(arrowstyle="->", lw=1.2, color=BLUE))
    ax2.text(1.5, 78.5, "Tube Disp. alone:\n+24.3 pp (p=0.013*)", ha="center", fontsize=7.5, fontweight="bold", color=BLUE,
             bbox=dict(boxstyle="round,pad=0.2", facecolor="#EFF6FF", edgecolor="#93C5FD", lw=0.6))

    ax2.set_xticks(range(3))
    ax2.set_xticklabels(arms, fontweight="bold")
    ax2.set_ylim(20, 98)
    ax2.set_ylabel("LOSO Balanced Accuracy (%)", fontweight="bold")
    ax2.set_title("(b) Sleep-EDF Staging (n=12 subjects)\nMechanism: Driven by Tube Dispersion (+30.3 pp)", fontweight="bold", pad=12)

    # Save outputs
    png_path = os.path.join(OUT_DIR, "fig3_preliminary_evidence.png")
    pdf_path = os.path.join(OUT_DIR, "fig3_preliminary_evidence.pdf")
    fig.savefig(png_path, bbox_inches="tight", dpi=300)
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)
    print(f"✓ Fig 3 generated from REAL numbers: {png_path}")


if __name__ == "__main__":
    generate_figure1()
    generate_figure3()
