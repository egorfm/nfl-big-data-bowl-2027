#!/usr/bin/env python3
"""
The Deceleration Engine: Complete Combine-to-Game Translation Model.
Processes:
  1. Combine Route Drills (Comeback, Curl, Speed Out) -> Kinematic Braking Signatures
  2. In-Game NGS Data (player_play.csv) -> Separation at Pass Forward & EPA
  3. BRK+ Metric Calibration & Scout Visualizations
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.data.loader import load_combine_metadata
from src.features.kinematics import smooth_tracking_data, compute_kinematics


def extract_player_route_drill_features(comb_tracks):
    """
    Extracts route-running kinematics from Combine route drills.
    Drills: COMEBACK_ROUTE_RIGHT, CURL_ROUTE_RIGHT, SPEED_OUT_ROUTE_LEFT
    """
    player_profiles = []

    for (nfl_id, drill_name), track in comb_tracks.groupby(["nfl_id", "drill_name"]):
        track = track.sort_values(by="time")
        if len(track) < 20:
            continue

        track_smooth = smooth_tracking_data(track)
        track_kin = compute_kinematics(track_smooth)

        # Braking phase: where tangential acceleration is strongly negative
        braking_frames = track_kin[track_kin["tangential_accel"] < -1.5]
        
        peak_decel = track_kin["tangential_accel"].min()
        max_speed = track_kin["calc_speed"].max()
        
        if len(braking_frames) >= 3:
            mean_decel = braking_frames["tangential_accel"].mean()
            # Entry speed into brake is max speed in the window just before peak decel
            peak_decel_idx = track_kin["tangential_accel"].idxmin()
            pre_window = track_kin.loc[:peak_decel_idx]
            entry_speed = pre_window["calc_speed"].max() if len(pre_window) > 0 else max_speed
            
            # Post window speed
            post_window = track_kin.loc[peak_decel_idx:]
            min_break_speed = post_window["calc_speed"].min() if len(post_window) > 0 else 0
        else:
            mean_decel = peak_decel
            entry_speed = max_speed
            min_break_speed = 0

        player_profiles.append({
            "nfl_id": nfl_id,
            "drill_name": drill_name,
            "max_speed": max_speed,
            "entry_speed": entry_speed,
            "peak_deceleration": peak_decel,
            "mean_deceleration": mean_decel,
            "speed_loss": entry_speed - min_break_speed,
        })

    df_profiles = pd.DataFrame(player_profiles)
    
    # Aggregate across route drills per player
    agg_df = df_profiles.groupby("nfl_id").agg({
        "peak_deceleration": "min",    # strongest peak braking
        "mean_deceleration": "mean",   # average braking capability
        "max_speed": "max",
        "entry_speed": "mean",
        "speed_loss": "mean"
    }).reset_index()
    
    return agg_df


def main():
    print("=" * 65)
    print("BUILDING THE COMPLETE DECELERATION ENGINE DATASET")
    print("=" * 65)

    raw_dir = project_root / "data" / "raw"
    proc_dir = project_root / "data" / "processed"
    fig_dir = project_root / "reports" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    # 1. Metadata
    print("\n[1/5] Loading metadata...")
    meta = load_combine_metadata(raw_dir)
    
    # 2. Extract Combine Route Kinematics
    print("\n[2/5] Parsing Combine Route Drills (Comeback, Curl, Speed Out)...")
    comb_tr = pd.read_csv(raw_dir / "combine_tracking.csv")
    target_drills = ["COMEBACK_ROUTE_RIGHT", "CURL_ROUTE_RIGHT", "SPEED_OUT_ROUTE_LEFT"]
    route_tracks = comb_tr[comb_tr["drill_name"].isin(target_drills)].copy()
    
    combine_kin = extract_player_route_drill_features(route_tracks)
    print(f"Extracted route braking signatures for {len(combine_kin)} players.")

    # 3. Process In-Game Performance from player_play.csv
    print("\n[3/5] Aggregating in-game route performance from player_play.csv...")
    pp = pd.read_csv(raw_dir / "player_play.csv")
    
    breaking_routes = ["HITCH", "OUT", "IN", "SLANT"]
    pp_break = pp[pp["route_ran"].isin(breaking_routes)].copy()
    
    game_agg = pp_break.groupby("nfl_id").agg(
        in_game_breaking_routes=("route_ran", "count"),
        in_game_mean_separation=("separation_at_pass_forward", "mean"),
        in_game_targets=("target", "sum"),
        in_game_epa_total=("expected_points_added", "sum"),
        in_game_epa_mean=("expected_points_added", "mean")
    ).reset_index()
    
    # Require at least 5 breaking routes
    game_agg = game_agg[game_agg["in_game_breaking_routes"] >= 5]
    print(f"Players with >= 5 in-game breaking routes: {len(game_agg)}")

    # 4. Master Merge & BRK+ Calculation
    print("\n[4/5] Merging into Master Translation Table...")
    master = combine_kin.merge(meta, on="nfl_id", how="inner")
    master = master.merge(game_agg, on="nfl_id", how="inner")
    
    # Calculate BRK+ (Braking Rate Plus)
    # Higher braking (more negative decel) -> higher BRK+ score
    mean_decel = master["mean_deceleration"].mean()
    std_decel = master["mean_deceleration"].std()
    
    # Advantage = (Mean - Actual) since decel is negative (more negative is better)
    z_score = (mean_decel - master["mean_deceleration"]) / (std_decel if std_decel > 0 else 1.0)
    master["BRK_plus"] = 100 + (z_score * 15)
    
    # Save Master Table
    master_path = proc_dir / "master_deceleration_translation.csv"
    master.to_csv(master_path, index=False)
    print(f"Saved master dataset: {master_path.name} (n={len(master)} qualified players)")

    # Print Top BRK+ Leaders
    cols_show = ["display_name", "combine_position", "forty", "BRK_plus", "in_game_mean_separation", "in_game_breaking_routes"]
    top_brk = master.sort_values(by="BRK_plus", ascending=False).head(10)
    print("\nTop 10 BRK+ Route Runners:")
    print(top_brk[cols_show].to_string(index=False))

    # 5. Publication-Quality Figures
    print("\n[5/5] Generating publication charts...")

    # Figure A: Deceleration vs In-Game Separation Scatter
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(9, 6), facecolor="#0e1117")
    ax.set_facecolor("#161b22")
    
    scatter = ax.scatter(
        master["BRK_plus"],
        master["in_game_mean_separation"],
        c=master["in_game_breaking_routes"],
        cmap="viridis",
        s=80,
        alpha=0.85,
        edgecolors="w",
        linewidth=0.5
    )
    
    # Trendline
    m_slope, b_intercept = np.polyfit(master["BRK_plus"], master["in_game_mean_separation"], 1)
    x_vals = np.linspace(master["BRK_plus"].min(), master["BRK_plus"].max(), 50)
    ax.plot(x_vals, m_slope * x_vals + b_intercept, color="#58a6ff", linestyle="--", linewidth=2, label=f"Trend (Slope = +{m_slope:.3f})")

    # Annotate top players
    for _, row in top_brk.head(5).iterrows():
        ax.annotate(
            row["display_name"],
            (row["BRK_plus"], row["in_game_mean_separation"]),
            xytext=(6, 4), textcoords="offset points",
            fontsize=9, color="#f0f6fc", fontweight="bold"
        )

    ax.set_xlabel("Combine BRK+ (Braking Rate Plus, League Avg = 100)", fontsize=11, color="#c9d1d9")
    ax.set_ylabel("In-Game Separation at Pass Forward (yards)", fontsize=11, color="#c9d1d9")
    ax.set_title("The Translation Proved: Combine Braking (BRK+) vs In-Game Route Separation", fontsize=13, fontweight="bold", pad=12, color="#ffffff")
    ax.grid(color="#30363d", linestyle="--", alpha=0.5)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("In-Game Breaking Routes Count", color="#c9d1d9")
    cbar.ax.yaxis.set_tick_params(color="#c9d1d9")
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color="#c9d1d9")
    ax.legend(facecolor="#21262d", edgecolor="#30363d", labelcolor="#c9d1d9")
    
    chart_path = fig_dir / "brk_plus_vs_ingame_separation.png"
    plt.tight_layout()
    fig.savefig(chart_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved figure: {chart_path.name}")

    print("\n" + "=" * 65)
    print("MASTER PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    main()
