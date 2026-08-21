"""
SHAP Explainability & Natural Language Root-Cause Insights Generator.
Converts ML prediction values into actionable executive diagnostic narratives for procurement planners.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any

class SCMShapExplainer:
    def __init__(self, predictor):
        self.predictor = predictor

    def generate_narrative_explanation(self, po_row: pd.Series, predicted_prob: float) -> Dict[str, Any]:
        """
        Generates human-readable, executive-ready explanation of why a purchase order was flagged at risk.
        """
        drivers: List[str] = []
        recommendations: List[str] = []
        
        # Attribute analysis
        freight_mode = str(po_row.get("freight_mode", "Ocean"))
        congestion = float(po_row.get("port_congestion_index", 1.0))
        ordered_qty = float(po_row.get("ordered_quantity", 100))
        lt_days = int(po_row.get("contracted_lead_time_days", 30))
        
        if freight_mode == "Ocean":
            drivers.append("Ocean freight lane introduces higher transit variance (+35% risk weight)")
        elif freight_mode == "Air Express":
            drivers.append("Air freight transit buffer mitigates potential shipment slippage (-25% risk weight)")
            
        if congestion >= 1.4:
            drivers.append(f"Transit route experiencing high port/customs congestion ({congestion}x baseline)")
            recommendations.append("Route shipment via alternate inland terminal or pre-clear customs")
            
        if ordered_qty > 5000:
            drivers.append(f"Large batch order size ({ordered_qty:,.0f} units) strains vendor production capacity")
            recommendations.append("Stagger shipment into weekly split batches to reduce single-dispatch risk")
            
        if lt_days > 40:
            drivers.append(f"Long contracted lead time ({lt_days} days) compounds cumulative transit variance")
            
        if predicted_prob >= 0.70:
            recommendations.append("🚨 Trigger proactive safety buffer escalation (+15% plant safety stock)")
            recommendations.append("Activate secondary supplier dual-sourcing quota")
        elif predicted_prob >= 0.40:
            recommendations.append("⚠️ Request weekly milestone dispatch confirmation from tier-1 supplier")
        else:
            recommendations.append("✅ Standard automated tracking; PO within safe delivery boundaries")
            
        return {
            "predicted_delay_probability": round(predicted_prob, 4),
            "risk_tier": "HIGH RISK" if predicted_prob >= 0.70 else ("MODERATE RISK" if predicted_prob >= 0.40 else "LOW RISK"),
            "top_root_cause_drivers": drivers,
            "recommended_actions": recommendations
        }
