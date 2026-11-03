"""
Kinematics & Biomechanical Feature Engineering Module.
Extracts continuous velocity, acceleration, braking, jerk, and curvature
from Combine drills and in-game Next Gen Stats (NGS) tracking data.
"""

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter


def smooth_tracking_data(df, coord_cols=("x", "y"), window_length=9, polyorder=2):
    """
    Applies Savitzky-Golay filter to smooth sensor coordinates and reduce sensor noise.
    Assumes standard 10Hz sampling (0.1s step).
    """
    df_smoothed = df.copy()
    if len(df_smoothed) >= window_length:
        for col in coord_cols:
            df_smoothed[f"{col}_smooth"] = savgol_filter(df_smoothed[col], window_length, polyorder)
    else:
        for col in coord_cols:
            df_smoothed[f"{col}_smooth"] = df_smoothed[col]
    return df_smoothed


def compute_kinematics(df, dt=0.1, x_col="x_smooth", y_col="y_smooth"):
    """
    Computes comprehensive 2D kinematics:
      - vx, vy, speed
      - ax, ay, total acceleration
      - tangential acceleration (a_t: positive = acceleration, negative = deceleration/braking)
      - normal / centripetal acceleration (a_n: turning force)
      - curvature (kappa)
      - jerk (da/dt)
    """
    df_k = df.copy()
    
    # Coordinates to numpy
    x = df_k[x_col].values if x_col in df_k.columns else df_k["x"].values
    y = df_k[y_col].values if y_col in df_k.columns else df_k["y"].values
    
    # 1. Velocities (1st derivative)
    vx = np.gradient(x, dt)
    vy = np.gradient(y, dt)
    speed = np.sqrt(vx**2 + vy**2)
    
    # 2. Accelerations (2nd derivative)
    ax = np.gradient(vx, dt)
    ay = np.gradient(vy, dt)
    total_accel = np.sqrt(ax**2 + ay**2)
    
    # 3. Tangential acceleration (along velocity vector)
    # a_t = (vx*ax + vy*ay) / speed
    with np.errstate(divide="ignore", invalid="ignore"):
        speed_safe = np.where(speed < 1e-4, 1e-4, speed)
        a_t = (vx * ax + vy * ay) / speed_safe
        
        # 4. Normal / Centripetal acceleration (perpendicular to velocity)
        # a_n = |vx*ay - vy*ax| / speed
        a_n = np.abs(vx * ay - vy * ax) / speed_safe
        
        # 5. Path Curvature: kappa = |vx*ay - vy*ax| / speed^3
        curvature = np.abs(vx * ay - vy * ax) / (speed_safe**3)
    
    # 6. Jerk (3rd derivative of position, derivative of acceleration)
    jerk = np.gradient(total_accel, dt)
    
    df_k["calc_vx"] = vx
    df_k["calc_vy"] = vy
    df_k["calc_speed"] = speed
    df_k["calc_ax"] = ax
    df_k["calc_ay"] = ay
    df_k["total_accel"] = total_accel
    df_k["tangential_accel"] = a_t
    df_k["normal_accel"] = a_n
    df_k["curvature"] = curvature
    df_k["jerk"] = jerk
    
    # Deceleration flag (braking phase)
    df_k["is_braking"] = a_t < -1.5  # decelerating at > 1.5 yd/s^2 (~1.37 m/s^2)
    
    return df_k


def extract_braking_signature(df, min_speed_entry=3.0):
    """
    Identifies significant braking events (cuts, stops, route breaks)
    and extracts key kinematic signatures:
      - Peak Deceleration (yd/s^2)
      - Entry Speed into Break (yd/s)
      - Exit Speed out of Break (yd/s)
      - Deceleration Duration (s)
      - Kinetic Energy Dissipation Efficiency (J/kg or yd^2/s^2)
    """
    if "tangential_accel" not in df.columns:
        df = compute_kinematics(df)
        
    braking_events = []
    in_event = False
    event_frames = []
    
    for idx, row in df.iterrows():
        if row["is_braking"] and row["calc_speed"] > 1.0:
            in_event = True
            event_frames.append(row)
        else:
            if in_event:
                if len(event_frames) >= 3:  # At least 300ms of braking
                    event_df = pd.DataFrame(event_frames)
                    entry_spd = event_df.iloc[0]["calc_speed"]
                    exit_spd = event_df.iloc[-1]["calc_speed"]
                    
                    if entry_spd >= min_speed_entry:
                        peak_decel = event_df["tangential_accel"].min()
                        mean_decel = event_df["tangential_accel"].mean()
                        duration = len(event_df) * 0.1
                        
                        braking_events.append({
                            "peak_deceleration": peak_decel,
                            "mean_deceleration": mean_decel,
                            "entry_speed": entry_spd,
                            "exit_speed": exit_spd,
                            "speed_drop": entry_spd - exit_spd,
                            "duration_seconds": duration,
                            "braking_rate": (entry_spd - exit_spd) / duration if duration > 0 else 0,
                            "peak_jerk": event_df["jerk"].abs().max(),
                            "start_frame": event_df.index[0],
                            "end_frame": event_df.index[-1]
                        })
                in_event = False
                event_frames = []
                
    return pd.DataFrame(braking_events)
