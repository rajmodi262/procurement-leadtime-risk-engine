"""
Global Freight Logistics & Scope-3 Carbon Footprint Network Optimizer.
Optimizes multi-modal transit corridors (Ocean vs Air vs Road vs Rail) balancing transit time, freight cost, and CO2 emissions.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any

class LogisticsNetworkOptimizer:
    def __init__(self):
        # Emission factors: kg CO2 per ton-km (GLEC Framework standard)
        self.emission_factors = {
            "Air Express": 0.602,     # High speed, high carbon
            "Road Freight": 0.082,    # Regional trucking
            "Rail": 0.028,            # Inter-modal rail
            "Ocean": 0.016            # Slow transit, lowest carbon footprint
        }
        
        # Base transit costs per ton-km ($)
        self.cost_per_ton_km = {
            "Air Express": 1.45,
            "Road Freight": 0.18,
            "Rail": 0.06,
            "Ocean": 0.02
        }

    def evaluate_transit_corridors(self, origin_country: str, destination_plant: str,
                                   weight_tons: float, distance_km: float) -> pd.DataFrame:
        """
        Evaluates multi-modal freight routes across Cost, Lead Time, and Carbon Footprint (Scope 3).
        """
        results: List[Dict[str, Any]] = []
        
        for mode, ef in self.emission_factors.items():
            base_cost = self.cost_per_ton_km[mode] * weight_tons * distance_km
            co2_emissions_kg = ef * weight_tons * distance_km
            
            # Transit speed approximation (km/day)
            speed_km_per_day = 8000 if mode == "Air Express" else (750 if mode == "Road Freight" else (500 if mode == "Rail" else 350))
            transit_days = max(1, int(distance_km / speed_km_per_day))
            
            # Environmental ESG Score (0 to 100)
            esg_score = max(0.0, min(100.0, 100.0 - (co2_emissions_kg / (weight_tons * 100.0))))
            
            results.append({
                "freight_mode": mode,
                "distance_km": distance_km,
                "cargo_weight_tons": weight_tons,
                "estimated_freight_cost_usd": round(base_cost, 2),
                "estimated_transit_days": transit_days,
                "scope_3_co2_kg": round(co2_emissions_kg, 2),
                "esg_sustainability_score": round(esg_score, 1)
            })
            
        df_res = pd.DataFrame(results)
        return df_res.sort_values(by="estimated_freight_cost_usd")
