#!/usr/bin/env python3
"""
Real NFL Scouting Combine Analysis:
1. Audits Combine 40-yd Dash, 3-Cone, and Shuttle against Career Success.
2. Extracts high-resolution kinematics (Braking Rate, Jerk, Curvature)
   from actual 10Hz combine tracking drills (THREE_CONE_DRILL & SKILL_DRILLS_WR).
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.data.loader import load_combine_metadata, load_combine_drill_tracks
from src.features.kinematics import smooth_tracking_data, compute_kinematics


def main():
    print("=" * 65)
    print("ANALYZING REAL NFL SCOUTING COMBINE DATASET")
    print("=" * 65)

    # 1. Load and merge metadata
    print("\n[1/4] Loading player metadata & career success...")
    meta = load_combine_metadata()
    print(f"Total merged players in dataset: {len(meta)}")
    
    # Filter WRs and DBs
    wrs_dbs = meta[meta["combine_position"].isin(["WR", "CB", "FS", "SS", "DB"])].copy()
    print(f"WRs & DBs in cohort: {len(wrs_dbs)}")

    # 2. Traditional metrics correlation audit
    print("\n[2/4] Traditional Combine vs Career Success Correlation Audit:")
    corr_cols = ["forty", "ten_yd_split", "three_cone", "short_shuttle", "vertical"]
    target_metric = "career_games_started"
    
    for col in corr_cols:
        if col in wrs_dbs.columns:
            valid = wrs_dbs.dropna(subset=[col, target_metric])
            if len(valid) > 20:
                corr = valid[col].corr(valid[target_metric])
                print(f"  - {col:<15} vs {target_metric}: r = {corr:+.3f} (n={len(valid)})")

    # 3. Load tracking for 3-Cone Drill
    print("\n[3/4] Processing real 10Hz Combine Tracking (THREE_CONE_DRILL)...")
    tracks_3cone = load_combine_drill_tracks(drill_types=["THREE_CONE_DRILL"])
    print(f"Loaded {len(tracks_3cone)} frames across {tracks_3cone['nfl_id'].nunique()} unique players.")

    # 4. Extract kinematic braking for each player in 3-Cone
    print("\n[4/4] Computing player kinematic signatures in 3-Cone Drill...")
    player_stats = []
    
    for nfl_id, p_track in tracks_3cone.groupby("nfl_id"):
        # Sort by event_id and time
        p_track = p_track.sort_values(by="time")
        if len(p_track) < 30:
            continue
            
        p_smooth = smooth_tracking_data(p_track)
        p_kin = compute_kinematics(p_smooth)
        
        peak_decel = p_kin["tangential_accel"].min()
        mean_braking = p_kin[p_kin["tangential_accel"] < -1.5]["tangential_accel"].mean()
        max_jerk = p_kin["jerk"].abs().max()
        max_speed = p_kin["calc_speed"].max()
        
        player_stats.append({
            "nfl_id": nfl_id,
            "max_speed": max_speed,
            "peak_deceleration": peak_decel,
            "mean_braking": mean_braking if not np.isnan(mean_braking) else 0,
            "max_jerk": max_jerk,
        })
        
    df_kin = pd.DataFrame(player_stats)
    df_merged = df_kin.merge(meta[["nfl_id", "display_name", "combine_position", "combine_weight", "forty", "three_cone", "career_games_started"]], on="nfl_id", how="left")
    
    # Sort by strongest braking capability (most negative peak deceleration)
    top_brakers = df_merged.sort_values(by="peak_deceleration").head(10)
    print("\nTop 10 Deceleration Specialists (3-Cone Drill):")
    cols_show = ["display_name", "combine_position", "forty", "three_cone", "peak_deceleration", "max_speed"]
    print(top_brakers[cols_show].to_string(index=False))

    # Save processed kin table
    out_path = project_root / "data" / "processed" / "combine_3cone_kinematics.csv"
    df_merged.to_csv(out_path, index=False)
    print(f"\nSaved processed kinematics table to: {out_path.name}")
    print("=" * 65)


if __name__ == "__main__":
    main()
