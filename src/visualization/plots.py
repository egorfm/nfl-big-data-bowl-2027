"""
Analytical Visualizations & Plotting Tools for Big Data Bowl.
Generates:
  - Route cuts with deceleration color heatmaps
  - Separation dynamics curves over time
  - Scout player profile radar charts
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_route_deceleration_overlay(ax, x, y, speed, tangential_accel, label="Player Track"):
    """
    Plots a player route trajectory on field axis with deceleration heatmap.
    Deceleration (braking) is highlighted in vivid crimson/orange, cruise in cyan.
    """
    # Scatter points with color mapping to tangential acceleration
    norm = plt.Normalize(-6.0, 4.0)
    cmap = plt.cm.coolwarm  # Blue/Cyan = acceleration, Red/Orange = heavy deceleration
    
    sc = ax.scatter(
        x, y,
        c=tangential_accel,
        cmap=cmap,
        norm=norm,
        s=35,
        alpha=0.85,
        edgecolor="none",
        zorder=5,
        label=label
    )
    
    # Draw trajectory line
    ax.plot(x, y, color="#ffffff", alpha=0.3, linewidth=1.5, zorder=4)
    return sc


def plot_separation_breakdown(time_series, wr_decel, db_distance, title="Separation vs Braking"):
    """
    Two-panel plot:
      Top: WR deceleration profile during route stem and break
      Bottom: Resulting separation distance to nearest defensive back
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, facecolor="#0e1117")
    
    for ax in [ax1, ax2]:
        ax.set_facecolor("#161b22")
        ax.grid(color="#30363d", linestyle="--", alpha=0.5)
        ax.tick_params(colors="#c9d1d9")
        for spine in ax.spines.values():
            spine.set_color("#30363d")

    # Panel 1: Deceleration
    ax1.plot(time_series, wr_decel, color="#f85149", linewidth=2.2, label="WR Tangential Accel (yd/s²)")
    ax1.axhline(0, color="#8b949e", linestyle=":", alpha=0.7)
    ax1.axhline(-2.0, color="#d29922", linestyle="--", alpha=0.8, label="Braking Threshold (-2.0 yd/s²)")
    ax1.set_ylabel("Accel / Decel (yd/s²)", color="#c9d1d9", fontsize=11)
    ax1.legend(loc="lower left", facecolor="#21262d", edgecolor="#30363d", labelcolor="#c9d1d9")
    ax1.set_title(title, color="#ffffff", fontsize=13, fontweight="bold", pad=10)

    # Panel 2: Separation
    ax2.plot(time_series, db_distance, color="#58a6ff", linewidth=2.5, label="Separation Distance (yards)")
    ax2.axhline(2.0, color="#3fb950", linestyle="--", alpha=0.8, label="Open Window (>= 2.0 yds)")
    ax2.set_xlabel("Time from Snap (s)", color="#c9d1d9", fontsize=11)
    ax2.set_ylabel("Separation (yards)", color="#c9d1d9", fontsize=11)
    ax2.legend(loc="upper left", facecolor="#21262d", edgecolor="#30363d", labelcolor="#c9d1d9")

    plt.tight_layout()
    return fig, (ax1, ax2)
