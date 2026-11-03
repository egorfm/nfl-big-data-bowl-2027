"""
Data Loading & Processing Pipeline.
Loads NFL Big Data Bowl 2027 tracking and combine data.
Includes sample generation for instant zero-dependency testing.
"""

from pathlib import Path
import numpy as np
import pandas as pd


DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def generate_synthetic_route_play(route_type="comeback", duration_sec=4.0, fps=10):
    """
    Generates synthetic high-fidelity 10Hz tracking data of a WR route cut
    and a covering DB, simulating realistic kinematics.
    Ideal for testing pipelines and visualization without multi-gigabyte raw files.
    """
    n_frames = int(duration_sec * fps)
    t = np.linspace(0, duration_sec, n_frames)
    
    # WR starts at line of scrimmage (x=30, y=10)
    # Stem: runs vertically upfield along X for 2.0s
    # Break: hard stop and cut back towards QB (Comeback route)
    wr_x = np.zeros(n_frames)
    wr_y = np.zeros(n_frames)
    db_x = np.zeros(n_frames)
    db_y = np.zeros(n_frames)
    
    # WR Trajectory
    stem_frames = int(2.0 * fps)
    break_frames = int(0.6 * fps)
    
    # 1. Stem phase (acceleration up to 8 yd/s)
    stem_dist = np.linspace(0, 15, stem_frames)
    wr_x[:stem_frames] = 30 + stem_dist
    wr_y[:stem_frames] = 10 + 0.1 * np.sin(np.linspace(0, np.pi, stem_frames))
    
    # 2. Break phase (hard braking: drops speed from 8 to 1.5 yd/s)
    break_idx = stem_frames + break_frames
    wr_x[stem_frames:break_idx] = 45 - np.linspace(0, 1.5, break_frames)
    wr_y[stem_frames:break_idx] = 10 + np.linspace(0, 2.0, break_frames)
    
    # 3. Recovery / Comeback phase (re-accelerating back towards sideline/QB)
    rem_frames = n_frames - break_idx
    wr_x[break_idx:] = (45 - 1.5) - np.linspace(0, 4.0, rem_frames)
    wr_y[break_idx:] = 12.0 + np.linspace(0, 2.5, rem_frames)
    
    # DB Trajectory (Starts 4 yds off in off-man coverage, lags WR cut by 0.25s)
    lag_frames = int(0.25 * fps)
    db_x[:stem_frames + lag_frames] = 34 + np.linspace(0, 15, stem_frames + lag_frames)
    db_y[:stem_frames + lag_frames] = 10.5
    
    # DB overshoots because of inertia, then changes direction
    overshoot_frames = n_frames - (stem_frames + lag_frames)
    db_x[stem_frames + lag_frames:] = 49 + np.linspace(0, 1.2, overshoot_frames) - np.linspace(0, 2.0, overshoot_frames)**1.2
    db_y[stem_frames + lag_frames:] = 10.5 + np.linspace(0, 3.0, overshoot_frames)
    
    df_wr = pd.DataFrame({
        "gameId": 2024090800,
        "playId": 101,
        "nflId": 99001,
        "frameId": np.arange(1, n_frames + 1),
        "time_s": t,
        "displayName": "Target WR (Elite Decel)",
        "position": "WR",
        "x": wr_x,
        "y": wr_y,
    })
    
    df_db = pd.DataFrame({
        "gameId": 2024090800,
        "playId": 101,
        "nflId": 99002,
        "frameId": np.arange(1, n_frames + 1),
        "time_s": t,
        "displayName": "Cover DB",
        "position": "CB",
        "x": db_x,
        "y": db_y,
    })
    
    return df_wr, df_db
