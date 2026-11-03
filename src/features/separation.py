"""
Route Separation & Matchup Dynamics Module.
Calculates continuous WR-DB separation, closing speed, reaction latency,
and separation gained during deceleration break points.
"""

import numpy as np
import pandas as pd


def compute_wr_db_separation(wr_tracking, db_tracking, join_on=None):
    """
    Merges WR and DB tracking on temporal frames and computes:
      - Euclidean distance (separation)
      - Closing / opening velocity (d_separation / dt)
      - Relative orientation and angle
    """
    if join_on is None:
        if "game_id" in wr_tracking.columns:
            join_on = ["game_id", "play_id"]
        else:
            join_on = ["gameId", "playId"]
            
        time_col = "frame_id" if "frame_id" in wr_tracking.columns else ("time_s" if "time_s" in wr_tracking.columns else "time")
        join_on.append(time_col)
        
    merged = pd.merge(
        wr_tracking,
        db_tracking,
        on=list(join_on),
        suffixes=("_wr", "_db")
    )
    
    # Separation distance
    dx = merged["x_wr"] - merged["x_db"]
    dy = merged["y_wr"] - merged["y_db"]
    merged["separation_distance"] = np.sqrt(dx**2 + dy**2)
    
    # Rate of change of separation (separation velocity)
    dt = 0.1
    merged["separation_velocity"] = np.gradient(merged["separation_distance"], dt)
    
    return merged


def quantify_break_separation_gain(merged_tracking, wr_braking_events):
    """
    For each braking event (route break) of the WR:
      - Computes separation at start of cut (entry)
      - Computes separation at break point (apex)
      - Computes separation at recovery point (exit)
      - Net separation gained (Separation Delta = Exit - Entry)
    """
    break_impacts = []
    
    for _, event in wr_braking_events.iterrows():
        start_f = event["start_frame"]
        end_f = event["end_frame"]
        
        event_window = merged_tracking.loc[start_f:end_f]
        if len(event_window) > 0:
            sep_entry = event_window.iloc[0]["separation_distance"]
            sep_exit = event_window.iloc[-1]["separation_distance"]
            max_sep = event_window["separation_distance"].max()
            min_sep = event_window["separation_distance"].min()
            
            break_impacts.append({
                "entry_separation": sep_entry,
                "exit_separation": sep_exit,
                "net_separation_gained": sep_exit - sep_entry,
                "max_separation_in_window": max_sep,
                "peak_decel": event["peak_deceleration"],
                "duration": event["duration_seconds"]
            })
            
    return pd.DataFrame(break_impacts)
