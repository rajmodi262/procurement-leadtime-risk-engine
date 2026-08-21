"""
Automated PyTest Suite for Procurement Analytics, Anomaly Detection, ML Predictor, Dual-Sourcing & API.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_generator import generate_procurement_dataset
from src.procurement_analytics import ProcurementAnalyticsEngine
from src.anomaly_detector import ProcurementAnomalyDetector
from src.ml_delay_predictor import DelayRiskPredictor
from src.dual_sourcing_optimizer import DualSourcingOptimizer
from src.shap_explainer import SCMShapExplainer

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
    
    sample_po = df_pos.iloc[0:2]
    scored = predictor.predict_delay_risk(sample_po)
    assert "predicted_delay_probability" in scored.columns
    assert "risk_tier" in scored.columns

def test_dual_sourcing_optimizer():
    optimizer = DualSourcingOptimizer()
    res = optimizer.optimize_allocation(
        primary_cost=40.0, primary_otif=80.0,
        secondary_cost=45.0, secondary_otif=95.0,
        total_order_qty=10000.0
    )
    assert "primary_allocation_pct" in res
    assert "secondary_allocation_pct" in res
    assert res["primary_allocation_pct"] + res["secondary_allocation_pct"] == 100.0

def test_shap_explainer(sample_data):
    df_suppliers, df_parts, df_pos = sample_data
    predictor = DelayRiskPredictor(random_state=42)
    predictor.train(df_pos)
    explainer = SCMShapExplainer(predictor)
    
    sample_row = df_pos.iloc[0]
    narrative = explainer.generate_narrative_explanation(sample_row, predicted_prob=0.75)
    assert narrative["risk_tier"] == "HIGH RISK"
    assert len(narrative["top_root_cause_drivers"]) > 0
    assert len(narrative["recommended_actions"]) > 0
