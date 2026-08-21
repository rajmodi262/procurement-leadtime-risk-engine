"""
Enterprise Synthetic Procurement & Purchase Order Data Generator.
Generates realistic multi-tier global supply chain procurement records with price variances and delivery dynamics.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_procurement_dataset(num_pos=25000, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    # 1. Suppliers
    suppliers = [
        {"supplier_id": "SUP-GLO-01", "supplier_name": "Codelco Chilean Copper Corp", "tier_level": "Strategic", "commodity_category": "Raw Copper", "headquarters_country": "Chile", "contract_incoterms": "FOB", "payment_terms_days": 60, "credit_rating": "AA", "is_single_source": False, "base_otif": 0.91, "base_lead_time": 30},
        {"supplier_id": "SUP-GLO-02", "supplier_name": "TSMC Automotive Microelectronics", "tier_level": "Strategic", "commodity_category": "Semiconductors", "headquarters_country": "Taiwan", "contract_incoterms": "FOB", "payment_terms_days": 45, "credit_rating": "AAA", "is_single_source": True, "base_otif": 0.83, "base_lead_time": 55},
        {"supplier_id": "SUP-GLO-03", "supplier_name": "Nippon Grain-Oriented Steel Works", "tier_level": "Tier 1", "commodity_category": "Electrical Steel", "headquarters_country": "Japan", "contract_incoterms": "CIF", "payment_terms_days": 60, "credit_rating": "AA", "is_single_source": False, "base_otif": 0.94, "base_lead_time": 25},
        {"supplier_id": "SUP-GLO-04", "supplier_name": "Infineon Power Modules GmbH", "tier_level": "Tier 1", "commodity_category": "IGBT Modules", "headquarters_country": "Germany", "contract_incoterms": "DDP", "payment_terms_days": 30, "credit_rating": "AA", "is_single_source": False, "base_otif": 0.89, "base_lead_time": 35},
        {"supplier_id": "SUP-GLO-05", "supplier_name": "Bharat Precision Fasteners & Busbars", "tier_level": "Tier 2", "commodity_category": "Fasteners & Copper Busbars", "headquarters_country": "India", "contract_incoterms": "EXW", "payment_terms_days": 45, "credit_rating": "A", "is_single_source": False, "base_otif": 0.95, "base_lead_time": 14},
        {"supplier_id": "SUP-GLO-06", "supplier_name": "SABIC High-Dielectric Polymers", "tier_level": "Tier 1", "commodity_category": "Polymers", "headquarters_country": "Saudi Arabia", "contract_incoterms": "CIF", "payment_terms_days": 60, "credit_rating": "AA", "is_single_source": False, "base_otif": 0.92, "base_lead_time": 28},
        {"supplier_id": "SUP-GLO-07", "supplier_name": "Shenzhen Precision Connectors Ltd", "tier_level": "Approved", "commodity_category": "Connectors & Terminals", "headquarters_country": "China", "contract_incoterms": "FOB", "payment_terms_days": 30, "credit_rating": "BBB", "is_single_source": True, "base_otif": 0.78, "base_lead_time": 42}
    ]
    df_suppliers = pd.DataFrame(suppliers)
    
    # 2. Commodities / Parts
    parts = [
        {"part_number": "PRT-CU-101", "part_description": "Oxygen-Free Continuous Cast Copper Rod 8mm", "commodity_group": "Raw Copper", "standard_cost_usd": 9.20, "unit_of_measure": "KG", "criticality_tier": "Class 1"},
        {"part_number": "PRT-ST-204", "part_description": "M4 Grade High-Permeability Silicon Steel Sheet", "commodity_group": "Electrical Steel", "standard_cost_usd": 4.80, "unit_of_measure": "KG", "criticality_tier": "Class 1"},
        {"part_number": "PRT-SC-301", "part_description": "32-Bit ARM Cortex M4 Inverter Controller MCU", "commodity_group": "Semiconductors", "standard_cost_usd": 42.50, "unit_of_measure": "Units", "criticality_tier": "Class 1"},
        {"part_number": "PRT-IG-402", "part_description": "1200V 600A Dual IGBT Half-Bridge Power Module", "commodity_group": "IGBT Modules", "standard_cost_usd": 285.00, "unit_of_measure": "Units", "criticality_tier": "Class 1"},
        {"part_number": "PRT-PL-505", "part_description": "Glass-Filled PBT Flame-Retardant Polymer Resin", "commodity_group": "Polymers", "standard_cost_usd": 6.40, "unit_of_measure": "KG", "criticality_tier": "Class 2"},
        {"part_number": "PRT-BB-601", "part_description": "Electrolytic Tin-Plated Copper Busbar 50x5mm", "commodity_group": "Fasteners & Copper Busbars", "standard_cost_usd": 18.50, "unit_of_measure": "Meters", "criticality_tier": "Class 2"},
        {"part_number": "PRT-CN-702", "part_description": "High-Voltage Sealed Terminal Connector Assembly", "commodity_group": "Connectors & Terminals", "standard_cost_usd": 12.80, "unit_of_measure": "Units", "criticality_tier": "Class 3"}
    ]
    df_parts = pd.DataFrame(parts)
    
    # Destination Plants
    plants = ["PL-PUN", "PL-TEX", "PL-SHA", "PL-STU", "PL-JUA"]
    freight_modes = [("Ocean", 0.60), ("Road Freight", 0.25), ("Air Express", 0.15)]
    
    # 3. Generate PO Transactions
    start_date = datetime(2025, 1, 1)
    pos_data = []
    
    for i in range(1, num_pos + 1):
        po_num = f"PO-2026-{100000 + i}"
        sup = random.choice(suppliers)
        
        # Match part by commodity group if possible
        matched_parts = [p for p in parts if p["commodity_group"] == sup["commodity_category"]]
        part = matched_parts[0] if matched_parts else random.choice(parts)
        
        plant_id = random.choice(plants)
        f_mode = random.choices([fm[0] for fm in freight_modes], weights=[fm[1] for fm in freight_modes])[0]
        
        po_date = start_date + timedelta(days=random.randint(0, 420))
        contracted_lt = sup["base_lead_time"] + random.randint(-3, 5)
        if f_mode == "Air Express":
            contracted_lt = max(5, int(contracted_lt * 0.4))
        elif f_mode == "Road Freight" and sup["headquarters_country"] in ["India", "Germany", "Japan"]:
            contracted_lt = max(7, int(contracted_lt * 0.6))
            
        promised_date = po_date + timedelta(days=contracted_lt)
        
        # Ordered Quantity
        qty_scale = 500 if part["unit_of_measure"] == "KG" else 50
        ordered_qty = round(float(random.randint(1, 40) * qty_scale), 2)
        
        # Purchase Price Variance (Inflation / Spot Market Dynamics)
        std_cost = part["standard_cost_usd"]
        # Commodity price volatility factor
        volatility = np.random.normal(0.02, 0.08) # 2% mean inflation, 8% std dev
        
        # 2% chance of extreme anomaly (e.g. 2x price surge or data entry error)
        is_anomaly = random.random() < 0.02
        if is_anomaly:
            volatility = random.uniform(0.60, 2.20)
            
        po_unit_price = round(max(0.1, std_cost * (1.0 + volatility)), 2)
        
        # Delivery Performance
        port_congestion = round(random.uniform(1.0, 1.8 if sup["headquarters_country"] in ["Taiwan", "China"] else 1.2), 2)
        
        # Probability of delay driven by: supplier base OTIF, freight mode, congestion, and single source
        delay_prob = (1.0 - sup["base_otif"]) * (1.2 if sup["is_single_source"] else 1.0) * (port_congestion / 1.2)
        if f_mode == "Ocean":
            delay_prob *= 1.3
        elif f_mode == "Air Express":
            delay_prob *= 0.4
        delay_prob = min(0.95, max(0.02, delay_prob))
        
        is_delayed = random.random() < delay_prob
        days_delayed = 0
        if is_delayed:
            days_delayed = int(np.random.exponential(scale=8.0)) + 1
            
        actual_lt = contracted_lt + days_delayed
        actual_receipt = po_date + timedelta(days=actual_lt)
        
        # Full receipt or partial shipment
        is_partial = is_delayed and random.random() < 0.20
        received_qty = round(ordered_qty * random.uniform(0.70, 0.95), 2) if is_partial else ordered_qty
        
        is_on_time = not is_delayed
        is_in_full = received_qty >= ordered_qty
        is_otif = is_on_time and is_in_full
        
        total_spend = round(received_qty * po_unit_price, 2)
        ppv = round((po_unit_price - std_cost) * received_qty, 2)
        
        pos_data.append({
            "po_number": po_num,
            "po_line_item": 1,
            "supplier_id": sup["supplier_id"],
            "supplier_name": sup["supplier_name"],
            "tier_level": sup["tier_level"],
            "is_single_source": sup["is_single_source"],
            "part_number": part["part_number"],
            "part_description": part["part_description"],
            "commodity_group": part["commodity_group"],
            "destination_plant_id": plant_id,
            "po_creation_date": po_date.strftime("%Y-%m-%d"),
            "promised_delivery_date": promised_date.strftime("%Y-%m-%d"),
            "actual_receipt_date": actual_receipt.strftime("%Y-%m-%d"),
            "contracted_lead_time_days": contracted_lt,
            "actual_lead_time_days": actual_lt,
            "ordered_quantity": ordered_qty,
            "received_quantity": received_qty,
            "po_unit_price_usd": po_unit_price,
            "standard_unit_cost_usd": std_cost,
            "total_spend_usd": total_spend,
            "purchase_price_variance_usd": ppv,
            "freight_mode": f_mode,
            "origin_country": sup["headquarters_country"],
            "transit_lane": f"{sup['headquarters_country']} -> {plant_id}",
            "port_congestion_index": port_congestion,
            "is_on_time": is_on_time,
            "is_in_full": is_in_full,
            "is_otif": is_otif,
            "is_delayed": is_delayed,
            "days_delayed": days_delayed,
            "anomaly_flag": is_anomaly
        })
        
    df_pos = pd.DataFrame(pos_data)
    
    os.makedirs("data", exist_ok=True)
    df_suppliers.to_csv("data/dim_supplier_procurement.csv", index=False)
    df_parts.to_csv("data/dim_commodity_part.csv", index=False)
    df_pos.to_csv("data/fact_purchase_orders.csv", index=False)
    
    print(f"[OK] Generated {len(df_pos)} Purchase Orders across {len(df_suppliers)} global suppliers.")
    return df_suppliers, df_parts, df_pos

if __name__ == "__main__":
    generate_procurement_dataset(num_pos=15000)
