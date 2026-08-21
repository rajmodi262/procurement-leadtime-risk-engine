"""
High-Performance DuckDB SQL Procurement Analytics Engine.
Calculates OTIF, PPV, Lead-Time Variance, and Supplier Concentration metrics.
"""

import duckdb
import pandas as pd
from typing import Dict, Any

class ProcurementAnalyticsEngine:
    def __init__(self, df_pos: pd.DataFrame, df_suppliers: pd.DataFrame):
        self.con = duckdb.connect(database=":memory:")
        self.con.register("fact_po", df_pos)
        self.con.register("dim_supplier", df_suppliers)

    def get_executive_summary(self) -> Dict[str, Any]:
        """Calculates macro-level procurement KPIs across all purchase orders."""
        query = """
        SELECT 
            COUNT(*) AS total_pos,
            SUM(total_spend_usd) AS total_spend_usd,
            SUM(purchase_price_variance_usd) AS total_ppv_usd,
            AVG(CASE WHEN is_otif THEN 1.0 ELSE 0.0 END) * 100 AS otif_percentage,
            AVG(CASE WHEN is_on_time THEN 1.0 ELSE 0.0 END) * 100 AS on_time_percentage,
            AVG(CASE WHEN is_in_full THEN 1.0 ELSE 0.0 END) * 100 AS in_full_percentage,
            AVG(actual_lead_time_days - contracted_lead_time_days) AS avg_lead_time_slippage_days,
            AVG(port_congestion_index) AS avg_port_congestion
        FROM fact_po
        """
        res = self.con.execute(query).df().iloc[0]
        return {
            "total_pos": int(res["total_pos"]),
            "total_spend_usd": round(float(res["total_spend_usd"]), 2),
            "total_ppv_usd": round(float(res["total_ppv_usd"]), 2),
            "otif_percentage": round(float(res["otif_percentage"]), 2),
            "on_time_percentage": round(float(res["on_time_percentage"]), 2),
            "in_full_percentage": round(float(res["in_full_percentage"]), 2),
            "avg_lead_time_slippage_days": round(float(res["avg_lead_time_slippage_days"]), 2)
        }

    def get_supplier_scorecard(self) -> pd.DataFrame:
        """Generates comprehensive vendor performance scorecards."""
        query = """
        SELECT 
            s.supplier_id,
            s.supplier_name,
            s.commodity_category,
            s.tier_level,
            s.headquarters_country,
            s.is_single_source,
            COUNT(p.po_number) AS po_count,
            SUM(p.total_spend_usd) AS total_spend_usd,
            SUM(p.purchase_price_variance_usd) AS total_ppv_usd,
            AVG(CASE WHEN p.is_otif THEN 1.0 ELSE 0.0 END) * 100 AS otif_rate_pct,
            AVG(p.actual_lead_time_days) AS avg_actual_lead_time,
            STDDEV(p.actual_lead_time_days) AS lead_time_std_dev,
            AVG(p.days_delayed) AS avg_delay_when_late
        FROM fact_po p
        JOIN dim_supplier s ON p.supplier_id = s.supplier_id
        GROUP BY 
            s.supplier_id, s.supplier_name, s.commodity_category, 
            s.tier_level, s.headquarters_country, s.is_single_source
        ORDER BY total_spend_usd DESC
        """
        return self.con.execute(query).df()

    def get_commodity_spend_and_ppv(self) -> pd.DataFrame:
        """Calculates spend and PPV aggregated by raw material commodity category."""
        query = """
        SELECT 
            commodity_group,
            COUNT(po_number) AS po_count,
            SUM(total_spend_usd) AS total_spend_usd,
            SUM(purchase_price_variance_usd) AS total_ppv_usd,
            (SUM(purchase_price_variance_usd) / SUM(total_spend_usd)) * 100 AS ppv_percentage_of_spend,
            AVG(CASE WHEN is_otif THEN 1.0 ELSE 0.0 END) * 100 AS otif_rate_pct
        FROM fact_po
        GROUP BY commodity_group
        ORDER BY total_spend_usd DESC
        """
        return self.con.execute(query).df()

    def calculate_herfindahl_index(self) -> Dict[str, float]:
        """
        Calculates the Herfindahl-Hirschman Index (HHI) for procurement market concentration.
        HHI = Sum of squared market share percentages (Range: 0 to 10,000).
        HHI > 2500 indicates high supplier concentration / single-source vulnerability.
        """
        query = """
        WITH supplier_shares AS (
            SELECT 
                supplier_id,
                (SUM(total_spend_usd) / (SELECT SUM(total_spend_usd) FROM fact_po)) * 100 AS market_share_pct
            FROM fact_po
            GROUP BY supplier_id
        )
        SELECT SUM(POWER(market_share_pct, 2)) AS hhi_index FROM supplier_shares
        """
        hhi = float(self.con.execute(query).df().iloc[0]["hhi_index"])
        return {
            "hhi_index": round(hhi, 1),
            "concentration_tier": "Highly Concentrated (High Risk)" if hhi > 2500 else ("Moderate" if hhi > 1500 else "Diversified")
        }
