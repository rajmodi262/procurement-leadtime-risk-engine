"""
Dual-Sourcing Risk-Adjusted Allocation Optimizer.
Calculates optimal order quantity splits between primary (cost-effective) and secondary (high-reliability) suppliers
to minimize expected total landed cost while hedging against line stoppage risk.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

class DualSourcingOptimizer:
    def __init__(self, risk_aversion_factor: float = 1.5):
        self.risk_aversion = risk_aversion_factor

    def optimize_allocation(self, primary_cost: float, primary_otif: float,
                            secondary_cost: float, secondary_otif: float,
                            total_order_qty: float,
                            stockout_cost_per_unit: float = 150.0) -> Dict[str, Any]:
        """
        Calculates optimal split ratio:
        Primary Supplier: Lower cost, but lower OTIF (higher delay risk)
        Secondary Supplier: Higher cost, but higher OTIF (backup hedge)
        """
        best_primary_ratio = 1.0
        min_expected_cost = float("inf")
        
        # Grid search over split ratios from 0.50 to 1.00 (with step 0.05)
        for ratio in np.linspace(0.40, 1.0, 13):
            primary_qty = total_order_qty * ratio
            secondary_qty = total_order_qty * (1.0 - ratio)
            
            # Expected Direct Purchase Cost
            direct_cost = (primary_qty * primary_cost) + (secondary_qty * secondary_cost)
            
            # Expected Delay / Line-Stoppage Risk Penalty
            primary_risk_qty = primary_qty * (1.0 - (primary_otif / 100.0 if primary_otif > 1 else primary_otif))
            secondary_risk_qty = secondary_qty * (1.0 - (secondary_otif / 100.0 if secondary_otif > 1 else secondary_otif))
            expected_risk_cost = (primary_risk_qty + secondary_risk_qty) * stockout_cost_per_unit * self.risk_aversion
            
            total_cost = direct_cost + expected_risk_cost
            if total_cost < min_expected_cost:
                min_expected_cost = total_cost
                best_primary_ratio = ratio
                
        opt_primary_qty = round(total_order_qty * best_primary_ratio, 1)
        opt_secondary_qty = round(total_order_qty * (1.0 - best_primary_ratio), 1)
        
        return {
            "primary_allocation_pct": round(best_primary_ratio * 100, 1),
            "secondary_allocation_pct": round((1.0 - best_primary_ratio) * 100, 1),
            "primary_order_units": opt_primary_qty,
            "secondary_order_units": opt_secondary_qty,
            "total_expected_landed_cost_usd": round(min_expected_cost, 2),
            "risk_mitigation_strategy": "Dual-Sourcing Active" if best_primary_ratio < 0.95 else "Single-Sourcing Sufficient"
        }
