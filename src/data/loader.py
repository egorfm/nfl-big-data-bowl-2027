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


def load_combine_metadata(raw_dir=RAW_DIR):
    """Loads players, combine results, and career success tables."""
    raw_dir = Path(raw_dir)
    players = pd.read_csv(raw_dir / "players.csv")
    combine_results = pd.read_csv(raw_dir / "combine_results.csv")
    career = pd.read_csv(raw_dir / "player_career_successes.csv")
    
    # Merge on nfl_id
    meta = players.merge(combine_results, on="nfl_id", how="left", suffixes=("", "_results"))
    meta = meta.merge(career, on="nfl_id", how="left")
    return meta


def load_combine_drill_tracks(drill_types=None, drill_names=None, raw_dir=RAW_DIR):
    """
    Loads combine tracking filtered by specific drill types or drill names.
    e.g. drill_types=['THREE_CONE_DRILL', 'SHORT_SHUTTLE', 'SKILL_DRILLS_WR']
    """
    raw_dir = Path(raw_dir)
    file_path = raw_dir / "combine_tracking.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Missing {file_path}")
        
    df = pd.read_csv(file_path)
    if drill_types is not None:
        df = df[df["drill_type"].isin(drill_types)]
    if drill_names is not None:
        df = df[df["drill_name"].isin(drill_names)]
    return df


def load_game_tracking(year=2023, sample_plays=None, raw_dir=RAW_DIR):
    """Loads in-game NGS tracking data for a specific season."""
    raw_dir = Path(raw_dir)
    file_path = raw_dir / f"game_tracking_{year}.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Missing {file_path}")
        
    if sample_plays is not None:
        # Stream read only requested plays for fast memory-efficient loading
        chunks = []
        for chunk in pd.read_csv(file_path, chunksize=100000):
            matched = chunk[chunk["play_id"].isin(sample_plays)]
            if len(matched) > 0:
                chunks.append(matched)
        return pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()
    
    return pd.read_csv(file_path)


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
        "game_id": 2024090800,
        "play_id": 101,
        "nfl_id": 99001,
        "frame_id": np.arange(1, n_frames + 1),
        "time_s": t,
        "display_name": "Target WR (Elite Decel)",
        "position": "WR",
        "x": wr_x,
        "y": wr_y,
    })
    
    df_db = pd.DataFrame({
        "game_id": 2024090800,
        "play_id": 101,
        "nfl_id": 99002,
        "frame_id": np.arange(1, n_frames + 1),
        "time_s": t,
        "display_name": "Cover DB",
        "position": "CB",
        "x": db_x,
        "y": db_y,
    })
    
    return df_wr, df_db

