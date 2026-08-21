"""
Automated PyTest Suite for Procurement Analytics, Anomaly Detection, and ML Predictor.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_generator import generate_procurement_dataset
from src.procurement_analytics import ProcurementAnalyticsEngine
from src.anomaly_detector import ProcurementAnomalyDetector
from src.ml_delay_predictor import DelayRiskPredictor

@pytest.fixture(scope="module")
def sample_data():
    df_suppliers, df_parts, df_pos = generate_procurement_dataset(num_pos=500, seed=42)
    return df_suppliers, df_parts, df_pos

def test_duckdb_procurement_analytics(sample_data):
    df_suppliers, df_parts, df_pos = sample_data
    engine = ProcurementAnalyticsEngine(df_pos, df_suppliers)
    
    summary = engine.get_executive_summary()
    assert summary["total_pos"] == 500
    assert summary["total_spend_usd"] > 0
    assert 0 <= summary["otif_percentage"] <= 100
    
    scorecard = engine.get_supplier_scorecard()
    assert len(scorecard) == len(df_suppliers)
    assert "otif_rate_pct" in scorecard.columns

def test_hhi_concentration(sample_data):
    df_suppliers, df_parts, df_pos = sample_data
    engine = ProcurementAnalyticsEngine(df_pos, df_suppliers)
    hhi = engine.calculate_herfindahl_index()
    assert "hhi_index" in hhi
    assert hhi["hhi_index"] > 0

def test_anomaly_detector(sample_data):
    df_suppliers, df_parts, df_pos = sample_data
    detector = ProcurementAnomalyDetector(contamination=0.05)
    df_scored = detector.fit_detect(df_pos)
    assert "is_ml_anomaly" in df_scored.columns
    assert "anomaly_score" in df_scored.columns
    assert df_scored["is_ml_anomaly"].sum() > 0

def test_ml_delay_predictor(sample_data):
    df_suppliers, df_parts, df_pos = sample_data
    predictor = DelayRiskPredictor(random_state=42)
    metrics = predictor.train(df_pos)
    assert metrics["roc_auc"] > 0.60
    
    # Test single PO inference
    sample_po = df_pos.iloc[0:2]
    scored = predictor.predict_delay_risk(sample_po)
    assert "predicted_delay_probability" in scored.columns
    assert "risk_tier" in scored.columns
