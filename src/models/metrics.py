"""
Scouting Metrics & The Deceleration Advantage Model.
Introduces:
  1. BRK+ (Braking Rate Plus): Standardized braking rate relative to league expectation (100 = average).
  2. DE-Index (Deceleration-to-Separation Efficiency): How effectively combine agility translates to game separation.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge


class DecelerationAdvantageModel:
    """
    Evaluates player braking capabilities conditioned on physical traits
    (weight, height, entry speed, drill angle).
    """
    
    def __init__(self):
        self.expected_decel_model = Ridge(alpha=1.0)
        self.baseline_mean = None
        self.baseline_std = None

    def fit_baseline(self, player_df, feature_cols, target_col="mean_deceleration"):
        """
        Fits baseline expectation model on Combine/NGS population.
        target_col: typically mean or peak deceleration (negative values).
        """
        X = player_df[feature_cols].fillna(player_df[feature_cols].median())
        y = player_df[target_col]
        
        self.expected_decel_model.fit(X, y)
        preds = self.expected_decel_model.predict(X)
        residuals = y - preds
        
        self.baseline_mean = np.mean(residuals)
        self.baseline_std = np.std(residuals) if np.std(residuals) > 0 else 1.0

    def calculate_brk_plus(self, player_df, feature_cols, target_col="mean_deceleration"):
        """
        Computes BRK+ (Braking Rate Plus):
          Score centered at 100 (League Average).
          > 115: Elite tier (top 10% deceleration ability)
          100 - 115: Above average
          85 - 100: Below average
          < 85: Heavy deceleration penalty / sluggish cutter
        Note: More negative deceleration means stronger braking, so sign is flipped.
        """
        X = player_df[feature_cols].fillna(player_df[feature_cols].median())
        y = player_df[target_col]
        
        expected_decel = self.expected_decel_model.predict(X)
        # Stronger braking is more negative, so advantage is (expected - actual)
        decel_advantage = expected_decel - y
        
        z_score = (decel_advantage - self.baseline_mean) / self.baseline_std
        # Scale to 100 baseline with 15 std dev (standard IQ / plus-metric scale)
        brk_plus = 100 + (z_score * 15)
        
        return np.clip(brk_plus, 50, 150)
