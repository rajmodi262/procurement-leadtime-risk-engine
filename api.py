"""
Enterprise FastAPI REST Service for Procurement Analytics & Delay Risk Scoring.
Enables real-time ERP integration to score purchase orders and fetch executive KPIs.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
from typing import Dict, Any, List

from src.data_generator import generate_procurement_dataset
from src.procurement_analytics import ProcurementAnalyticsEngine
from src.ml_delay_predictor import DelayRiskPredictor
from src.shap_explainer import SCMShapExplainer
from src.dual_sourcing_optimizer import DualSourcingOptimizer

app = FastAPI(
    title="Global Procurement & Delay Risk API",
    description="Enterprise REST API for Supplier Performance, OTIF/PPV KPIs, and Inbound Delay Forecasting.",
    version="1.2.0"
)

# Initialize data & model state
df_suppliers, df_parts, df_pos = generate_procurement_dataset(num_pos=5000, seed=42)
analytics = ProcurementAnalyticsEngine(df_pos, df_suppliers)
predictor = DelayRiskPredictor(random_state=42)
predictor.train(df_pos)
explainer = SCMShapExplainer(predictor)
dual_optimizer = DualSourcingOptimizer()

class PurchaseOrderPayload(BaseModel):
    supplier_id: str = Field(..., example="SUP-GLO-02")
    commodity_group: str = Field(..., example="Semiconductors")
    freight_mode: str = Field("Ocean", example="Ocean")
    origin_country: str = Field("Taiwan", example="Taiwan")
    destination_plant_id: str = Field("PL-PUN", example="PL-PUN")
    contracted_lead_time_days: int = Field(45, ge=1, le=180)
    ordered_quantity: float = Field(2500.0, gt=0)
    po_unit_price_usd: float = Field(42.50, gt=0)
    port_congestion_index: float = Field(1.5, ge=1.0, le=3.0)

class DualSourcingRequest(BaseModel):
    primary_cost: float = Field(..., example=42.5)
    primary_otif: float = Field(..., example=82.0)
    secondary_cost: float = Field(..., example=46.0)
    secondary_otif: float = Field(..., example=96.0)
    total_order_qty: float = Field(..., example=10000.0)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ONLINE", "service": "SCM Procurement Analytics Engine", "version": "1.2.0"}

@app.get("/api/v1/kpis/executive-summary", tags=["Analytics"])
def get_executive_kpis():
    summary = analytics.get_executive_summary()
    hhi = analytics.calculate_herfindahl_index()
    return {"executive_summary": summary, "market_concentration_hhi": hhi}

@app.get("/api/v1/suppliers/scorecard", tags=["Analytics"])
def get_supplier_scorecards():
    scorecard_df = analytics.get_supplier_scorecard()
    return {"count": len(scorecard_df), "scorecards": scorecard_df.to_dict(orient="records")}

@app.post("/api/v1/predict/delay-risk", tags=["Predictive AI"])
def predict_po_delay_risk(payload: PurchaseOrderPayload):
    po_dict = payload.dict()
    df_single = pd.DataFrame([po_dict])
    
    scored_df = predictor.predict_delay_risk(df_single)
    prob = float(scored_df["predicted_delay_probability"].values[0])
    
    # Generate SHAP root-cause diagnostic
    explanation = explainer.generate_narrative_explanation(pd.Series(po_dict), prob)
    
    return {
        "po_input": po_dict,
        "prediction": explanation
    }

@app.post("/api/v1/optimize/dual-sourcing", tags=["Optimization"])
def optimize_dual_sourcing_split(req: DualSourcingRequest):
    result = dual_optimizer.optimize_allocation(
        primary_cost=req.primary_cost,
        primary_otif=req.primary_otif,
        secondary_cost=req.secondary_cost,
        secondary_otif=req.secondary_otif,
        total_order_qty=req.total_order_qty
    )
    return result
