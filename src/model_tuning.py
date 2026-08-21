"""
Machine Learning Model Benchmark & 5-Fold Stratified Cross-Validation Module.
Benchmarks XGBoost against Random Forest and Logistic Regression baselines across ROC-AUC, Precision, Recall, and F1.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from typing import Dict, Any

class SCMModelBenchmark:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state

    def benchmark_models(self, df_pos: pd.DataFrame) -> pd.DataFrame:
        from src.ml_delay_predictor import DelayRiskPredictor
        
        predictor = DelayRiskPredictor(random_state=self.random_state)
        X = predictor.prepare_features(df_pos, is_train=True)
        y = df_pos["is_delayed"].astype(int).values
        
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
        scoring = ["roc_auc", "precision", "recall", "f1"]
        
        models = {
            "XGBoost (Optimized)": xgb.XGBClassifier(
                n_estimators=100, max_depth=5, learning_rate=0.08, eval_metric="logloss", random_state=self.random_state
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=100, max_depth=8, random_state=self.random_state
            ),
            "Logistic Regression (Baseline)": LogisticRegression(
                max_iter=1000, random_state=self.random_state
            )
        }
        
        results = []
        for name, clf in models.items():
            scores = cross_validate(clf, X, y, cv=cv, scoring=scoring, n_jobs=-1)
            results.append({
                "model_architecture": name,
                "mean_roc_auc": round(float(np.mean(scores["test_roc_auc"])), 4),
                "std_roc_auc": round(float(np.std(scores["test_roc_auc"])), 4),
                "mean_f1_score": round(float(np.mean(scores["test_f1"])), 4),
                "mean_precision": round(float(np.mean(scores["test_precision"])), 4),
                "mean_recall": round(float(np.mean(scores["test_recall"])), 4)
            })
            
        df_bench = pd.DataFrame(results).sort_values(by="mean_roc_auc", ascending=False)
        return df_bench
