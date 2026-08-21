"""
Commodity Index-Linked Contract Pricing & Hedging Engine.
Simulates LME (London Metal Exchange) raw material index-linked pricing vs Fixed Contract vs Spot Market dynamics.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

class CommodityContractIndexer:
    def __init__(self, base_copper_lme_usd_per_kg: float = 9.20):
        self.base_copper_lme = base_copper_lme_usd_per_kg

    def calculate_index_linked_price(self, lme_market_price_kg: float, 
                                     supplier_conversion_fee_kg: float = 1.25,
                                     hedged_ratio: float = 0.60,
                                     contracted_fixed_price_kg: float = 9.50) -> Dict[str, Any]:
        """
        Calculates blended contract pricing under financial commodity hedging.
        Formula: Price = Hedged_Ratio * Contracted_Fixed + (1 - Hedged_Ratio) * (LME_Market + Conversion_Fee)
        """
        unhedged_market_price = lme_market_price_kg + supplier_conversion_fee_kg
        blended_unit_cost = (hedged_ratio * contracted_fixed_price_kg) + ((1.0 - hedged_ratio) * unhedged_market_price)
        
        price_variance_vs_budget = blended_unit_cost - contracted_fixed_price_kg
        hedging_savings_usd_per_kg = unhedged_market_price - blended_unit_cost
        
        return {
            "lme_market_price_usd_kg": round(lme_market_price_kg, 2),
            "unhedged_spot_price_usd_kg": round(unhedged_market_price, 2),
            "blended_contract_cost_usd_kg": round(blended_unit_cost, 2),
            "effective_hedging_ratio_pct": round(hedged_ratio * 100, 1),
            "unit_price_variance_vs_budget": round(price_variance_vs_budget, 2),
            "cost_avoidance_savings_per_kg": round(hedging_savings_usd_per_kg, 2),
            "contract_strategy": "Hedged Protection Active" if hedging_savings_usd_per_kg > 0 else "Spot Price Favorable"
        }
