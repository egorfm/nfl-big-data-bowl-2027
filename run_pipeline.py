#!/usr/bin/env python3
"""
End-to-End Pipeline Execution: The Deceleration Engine.
Runs data extraction, kinematics calculation, WR-DB separation dynamics,
metric scoring (BRK+), and generates publication-grade visual artifacts.
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# Add src to python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.data.loader import generate_synthetic_route_play
from src.features.kinematics import smooth_tracking_data, compute_kinematics, extract_braking_signature
from src.features.separation import compute_wr_db_separation, quantify_break_separation_gain
from src.models.metrics import DecelerationAdvantageModel
from src.visualization.field import draw_nfl_field
from src.visualization.plots import plot_route_deceleration_overlay, plot_separation_breakdown


def main():
    print("=" * 65)
    print("NFL BIG DATA BOWL 2027: THE DECELERATION ENGINE PIPELINE")
    print("=" * 65)

    # 1. Load / Generate tracking data
    print("\n[1/5] Loading tracking data...")
    df_wr, df_db = generate_synthetic_route_play()
    print(f"Loaded WR frames: {len(df_wr)}, DB frames: {len(df_db)}")

    # 2. Kinematics & Braking Dynamics
    print("\n[2/5] Smoothing sensors & computing high-order kinematics...")
    df_wr_smooth = smooth_tracking_data(df_wr)
    df_wr_kin = compute_kinematics(df_wr_smooth)
    
    df_db_smooth = smooth_tracking_data(df_db)
    df_db_kin = compute_kinematics(df_db_smooth)
    
    braking_events = extract_braking_signature(df_wr_kin)
    print(f"Detected {len(braking_events)} significant route break / braking event(s):")
    for idx, ev in braking_events.iterrows():
        print(f"  - Break #{idx+1}: Peak Decel = {ev['peak_deceleration']:.2f} yd/s², "
              f"Entry Speed = {ev['entry_speed']:.2f} yd/s, Speed Drop = {ev['speed_drop']:.2f} yd/s")

    # 3. Dynamic WR-DB Separation Analysis
    print("\n[3/5] Quantifying WR vs DB separation & reaction lag...")
    merged_sep = compute_wr_db_separation(df_wr_kin, df_db_kin)
    break_impact = quantify_break_separation_gain(merged_sep, braking_events)
    
    if len(break_impact) > 0:
        row = break_impact.iloc[0]
        print(f"  - Entry Separation: {row['entry_separation']:.2f} yds")
        print(f"  - Exit Separation:  {row['exit_separation']:.2f} yds")
        print(f"  - Net Gained from Deceleration: +{row['net_separation_gained']:.2f} yds")

    # 4. Metric Formulation (BRK+ Score)
    print("\n[4/5] Evaluating Deceleration Advantage (BRK+)...")
    # Simulate a population sample for baseline calibration
    mock_population = pd.DataFrame({
        "weight_lbs": [190, 195, 205, 185, 210, 192],
        "height_in": [72, 73, 74, 71, 75, 72],
        "entry_speed": [7.8, 8.1, 7.5, 8.4, 7.2, 8.0],
        "mean_deceleration": [-3.1, -3.8, -2.6, -4.5, -2.4, -3.5]
    })
    
    feature_cols = ["weight_lbs", "height_in", "entry_speed"]
    model = DecelerationAdvantageModel()
    model.fit_baseline(mock_population, feature_cols)
    
    # Evaluate target player
    target_player = pd.DataFrame([{
        "weight_lbs": 192,
        "height_in": 72,
        "entry_speed": braking_events.iloc[0]["entry_speed"],
        "mean_deceleration": braking_events.iloc[0]["mean_deceleration"]
    }])
    brk_score = model.calculate_brk_plus(target_player, feature_cols)[0]
    print(f"  >>> Target WR BRK+ Index: {brk_score:.1f} (League Avg = 100)")

    # 5. Visualizations & Artifacts
    print("\n[5/5] Generating publication figures...")
    figures_dir = project_root / "reports" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    # Figure 1: Field Trajectory with Braking Overlay
    fig, ax = draw_nfl_field(xlim=(25, 55), ylim=(5, 25))
    plot_route_deceleration_overlay(
        ax, df_wr_kin["x_smooth"], df_wr_kin["y_smooth"],
        df_wr_kin["calc_speed"], df_wr_kin["tangential_accel"],
        label="WR Route"
    )
    ax.plot(df_db_kin["x_smooth"], df_db_kin["y_smooth"], "--", color="#ffcc00", linewidth=1.8, label="DB Shadow Track")
    ax.legend(loc="upper right", facecolor="#21262d", edgecolor="#30363d", labelcolor="#c9d1d9")
    field_fig_path = figures_dir / "field_route_break_overlay.png"
    fig.savefig(field_fig_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {field_fig_path.name}")

    # Figure 2: Separation Breakdown Curve
    fig2, _ = plot_separation_breakdown(
        merged_sep["time_s_wr"],
        merged_sep["tangential_accel_wr"],
        merged_sep["separation_distance"],
        title="WR Braking vs Created Separation Over Time"
    )
    sep_fig_path = figures_dir / "separation_dynamics_curve.png"
    fig2.savefig(sep_fig_path, dpi=200, bbox_inches="tight")
    plt.close(fig2)
    print(f"  Saved: {sep_fig_path.name}")

    print("\n" + "=" * 65)
    print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    main()
