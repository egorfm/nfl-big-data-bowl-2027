"""
NFL Field Visualization Module.
Renders an accurate, publication-quality NFL field using matplotlib.
Dimensions: 120 yards long (including 10-yard endzones), 53.3 yards wide.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def draw_nfl_field(
    figsize=(12, 6.33),
    field_color="#1a472a",
    line_color="#ffffff",
    endzone_color="#12351e",
    alpha=0.9,
    show_numbers=True,
    show_hashes=True,
    xlim=(0, 120),
    ylim=(0, 53.3),
):
    """
    Creates and returns a matplotlib figure and axis with an authentic NFL field.
    
    Standard NFL Coordinate System:
      - X axis: 0 to 120 (0-10: Endzone, 10-110: Field of play, 110-120: Endzone)
      - Y axis: 0 to 53.3 (Sideline to sideline)
    """
    fig, ax = plt.subplots(figsize=figsize, facecolor="#0e1117")
    ax.set_facecolor(field_color)

    # 1. Outer boundary
    field_rect = patches.Rectangle(
        (0, 0), 120, 53.3, linewidth=2, edgecolor=line_color, facecolor=field_color, alpha=alpha, zorder=0
    )
    ax.add_patch(field_rect)

    # 2. Endzones
    left_endzone = patches.Rectangle((0, 0), 10, 53.3, facecolor=endzone_color, alpha=0.9, zorder=1)
    right_endzone = patches.Rectangle((110, 0), 10, 53.3, facecolor=endzone_color, alpha=0.9, zorder=1)
    ax.add_patch(left_endzone)
    ax.add_patch(right_endzone)

    # 3. Yard lines every 5 yards
    for x in range(15, 110, 5):
        lw = 1.5 if x % 10 == 0 else 0.75
        ax.plot([x, x], [0, 53.3], color=line_color, linewidth=lw, alpha=0.7, zorder=2)

    # Goal lines (10 and 110)
    ax.plot([10, 10], [0, 53.3], color=line_color, linewidth=2.5, zorder=3)
    ax.plot([110, 110], [0, 53.3], color=line_color, linewidth=2.5, zorder=3)

    # 4. Hash marks
    if show_hashes:
        # NFL hashmarks: 70 ft 9 in (23.58 yd) from sidelines
        hash_bottom_y = 53.3 / 2 - 3.08  # ~23.57 yd
        hash_top_y = 53.3 / 2 + 3.08     # ~29.73 yd
        for x in range(11, 110):
            if x % 5 != 0:
                # Sideline hashes
                ax.plot([x, x], [0.4, 0.9], color=line_color, linewidth=0.6, alpha=0.6, zorder=2)
                ax.plot([x, x], [53.3 - 0.9, 53.3 - 0.4], color=line_color, linewidth=0.6, alpha=0.6, zorder=2)
                # Infield hashes
                ax.plot([x, x], [hash_bottom_y - 0.25, hash_bottom_y + 0.25], color=line_color, linewidth=0.6, alpha=0.6, zorder=2)
                ax.plot([x, x], [hash_top_y - 0.25, hash_top_y + 0.25], color=line_color, linewidth=0.6, alpha=0.6, zorder=2)

    # 5. Yard numbers
    if show_numbers:
        for x in range(20, 110, 10):
            num = x - 10 if x <= 60 else 110 - x
            # Bottom numbers
            ax.text(
                x, 12, str(num),
                color=line_color, fontsize=12, fontweight="bold",
                horizontalalignment="center", verticalalignment="center",
                alpha=0.65, zorder=3, rotation=0
            )
            # Top numbers
            ax.text(
                x, 53.3 - 12, str(num),
                color=line_color, fontsize=12, fontweight="bold",
                horizontalalignment="center", verticalalignment="center",
                alpha=0.65, zorder=3, rotation=180
            )

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()

    return fig, ax
