"""
Predictive Machine Learning Pipeline for Component Transit Delay Risk.
Trains an XGBoost Classifier with SHAP explainability to predict shipment delay probabilities at PO creation time.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report, f1_score
import xgboost as xgb
import shap

class DelayRiskPredictor:
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.model = None
        self.explainer = None
        self.feature_names = []
        self.categorical_cols = ["supplier_id", "commodity_group", "freight_mode", "origin_country", "destination_plant_id"]
        self.numeric_cols = ["contracted_lead_time_days", "ordered_quantity", "po_unit_price_usd", "port_congestion_index"]

    def prepare_features(self, df_pos: pd.DataFrame, is_train: bool = True):
        df = df_pos.copy()
        
        # One-hot encode categoricals
        df_encoded = pd.get_dummies(df[self.categorical_cols], drop_first=True)
        
        if is_train:
            self.encoded_columns = df_encoded.columns.tolist()
        else:
            # Align columns with training set
            for col in self.encoded_columns:
                if col not in df_encoded.columns:
                    df_encoded[col] = 0
            df_encoded = df_encoded[self.encoded_columns]
            
        X = pd.concat([df[self.numeric_cols].reset_index(drop=True), df_encoded.reset_index(drop=True)], axis=1)
        self.feature_names = X.columns.tolist()
        return X

    def train(self, df_pos: pd.DataFrame):
        X = self.prepare_features(df_pos, is_train=True)
        y = df_pos["is_delayed"].astype(int).values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=self.random_state, stratify=y
        )
        
        self.model = xgb.XGBClassifier(
            n_estimators=120,
            max_depth=5,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            eval_metric="logloss",
            random_state=self.random_state
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluation
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        y_pred = self.model.predict(X_test)
        
        auc = roc_auc_score(y_test, y_pred_proba)
        f1 = f1_score(y_test, y_pred)
        
        # Initialize SHAP TreeExplainer
        self.explainer = shap.TreeExplainer(self.model)
        
        metrics = {
            "roc_auc": round(float(auc), 4),
            "f1_score": round(float(f1), 4),
            "classification_report": classification_report(y_test, y_pred, output_dict=True)
        }
        print(f"[ML Pipeline] Model Trained Successfully. ROC-AUC: {auc:.4f} | F1: {f1:.4f}")
        return metrics

    def predict_delay_risk(self, df_new: pd.DataFrame) -> pd.DataFrame:
        if self.model is None:
            raise ValueError("Model must be trained before predicting.")
            
        X = self.prepare_features(df_new, is_train=False)
        probabilities = self.model.predict_proba(X)[:, 1]
        
        df_result = df_new.copy()
        df_result["predicted_delay_probability"] = np.round(probabilities, 4)
        df_result["risk_tier"] = df_result["predicted_delay_probability"].apply(
            lambda p: "HIGH RISK (>70%)" if p >= 0.70 else ("MEDIUM (40-70%)" if p >= 0.40 else "LOW (<40%)")
        )
        return df_result

    def get_shap_feature_importance(self, df_sample: pd.DataFrame):
        X = self.prepare_features(df_sample, is_train=False)
        shap_values = self.explainer.shap_values(X)
        mean_shap = np.abs(shap_values).mean(axis=0)
        df_importance = pd.DataFrame({
            "feature": self.feature_names,
            "mean_abs_shap": mean_shap
        }).sort_values(by="mean_abs_shap", ascending=False)
        return df_importance
