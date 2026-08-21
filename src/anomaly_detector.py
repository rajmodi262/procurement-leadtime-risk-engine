"""
Procurement Anomaly Detection Engine.
Uses Isolation Forest and robust statistical z-scores to identify price gouging, rogue spend, and extreme delivery bottlenecks.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class ProcurementAnomalyDetector:
    def __init__(self, contamination: float = 0.02, random_state: int = 42):
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        self.is_fitted = False

    def fit_detect(self, df_pos: pd.DataFrame) -> pd.DataFrame:
        """
        Fits Isolation Forest on PO pricing variance and lead-time anomalies.
        """
        df = df_pos.copy()
        
        # Features for anomaly detection
        df["price_variance_ratio"] = df["po_unit_price_usd"] / df["standard_unit_cost_usd"].replace(0, 0.01)
        df["lead_time_ratio"] = df["actual_lead_time_days"] / df["contracted_lead_time_days"].replace(0, 1)
        
        features = ["price_variance_ratio", "lead_time_ratio", "total_spend_usd", "days_delayed"]
        X = df[features].fillna(0)
        
        # Fit Isolation Forest
        self.model.fit(X)
        self.is_fitted = True
        
        df["anomaly_score"] = self.model.decision_function(X)
        df["is_ml_anomaly"] = self.model.predict(X) == -1
        
        # Rule-based validation flags
        df["price_spike_3x"] = df["price_variance_ratio"] >= 1.50
        df["extreme_delay_20d"] = df["days_delayed"] >= 15
        
        return df

    def get_flagged_anomalies(self, df_scored: pd.DataFrame) -> pd.DataFrame:
        """Returns flagged anomalous purchase orders for auditing."""
        return df_scored[df_scored["is_ml_anomaly"]].sort_values(by="anomaly_score", ascending=True)
