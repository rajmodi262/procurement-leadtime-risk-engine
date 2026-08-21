"""
Enterprise Power BI Template & Dataset Bundle Builder for Global Procurement Analytics & Risk Engine.
Generates:
1. Eaton_Procurement_Risk_Platform.pbit (Power BI Template Archive)
2. Eaton_Procurement_Project.pbip (Power BI Modern Project Format)
3. Eaton_Procurement_DataModel.xlsx (Pre-loaded Star Schema Excel Model with 25,000+ POs)
"""

import os
import sys
import json
import zipfile
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath("."))
try:
    from src.data_generator import generate_procurement_dataset
except ImportError:
    from data_generator import generate_procurement_dataset

def create_procurement_bundle():
    print("=== Generating Procurement Power BI Files ===")
    os.makedirs("powerbi", exist_ok=True)
    
    df_suppliers, df_parts, df_orders = generate_procurement_dataset(num_pos=25000, seed=42)
    
    # 1. Pre-Packaged Excel Star Schema Model
    excel_path = "powerbi/Eaton_Procurement_DataModel.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_orders.to_excel(writer, sheet_name="fact_purchase_orders", index=False)
        df_suppliers.to_excel(writer, sheet_name="dim_supplier", index=False)
        df_parts.to_excel(writer, sheet_name="dim_commodity_part", index=False)
    print(f"  [OK] Created Pre-loaded Procurement Excel Model: {excel_path}")

    # 2. Tabular Model Schema (BIM)
    data_model_schema = {
        "name": "Eaton_Procurement_DataModel",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "tables": [
                {
                    "name": "dim_supplier",
                    "columns": [{"name": col, "dataType": "string" if df_suppliers[col].dtype == 'object' else "double"} for col in df_suppliers.columns]
                },
                {
                    "name": "dim_commodity_part",
                    "columns": [{"name": col, "dataType": "string" if df_parts[col].dtype == 'object' else "double"} for col in df_parts.columns]
                },
                {
                    "name": "fact_purchase_orders",
                    "columns": [{"name": col, "dataType": "string" if df_orders[col].dtype == 'object' else "double"} for col in df_orders.columns],
                    "measures": [
                        {
                            "name": "Total Procurement Spend ($)",
                            "expression": "SUM(fact_purchase_orders[total_po_value_usd])",
                            "formatString": "\\$#,0"
                        },
                        {
                            "name": "Supplier OTIF %",
                            "expression": "DIVIDE(CALCULATE(COUNTROWS(fact_purchase_orders), fact_purchase_orders[is_otif] = TRUE), COUNTROWS(fact_purchase_orders), 0)",
                            "formatString": "0.0%"
                        },
                        {
                            "name": "Total Purchase Price Variance (PPV)",
                            "expression": "SUM(fact_purchase_orders[purchase_price_variance_usd])",
                            "formatString": "\\$#,0"
                        },
                        {
                            "name": "Delayed POs Count",
                            "expression": "CALCULATE(COUNTROWS(fact_purchase_orders), fact_purchase_orders[is_delayed] = TRUE)",
                            "formatString": "#,0"
                        }
                    ]
                }
            ],
            "relationships": [
                {"name": "rel_supplier", "fromTable": "fact_purchase_orders", "fromColumn": "supplier_id", "toTable": "dim_supplier", "toColumn": "supplier_id"},
                {"name": "rel_part", "fromTable": "fact_purchase_orders", "fromColumn": "part_number", "toTable": "dim_commodity_part", "toColumn": "part_number"}
            ]
        }
    }

    # 3. Power BI Layout JSON
    report_layout = {
        "id": 0,
        "resourcePackages": [],
        "sections": [
            {
                "id": 0,
                "name": "ReportSection_ProcurementCommand",
                "displayName": "Global Procurement Command Center",
                "filters": "[]",
                "ordinal": 0,
                "visualContainers": [
                    {
                        "x": 20, "y": 20, "z": 1000, "width": 300, "height": 140,
                        "config": json.dumps({"name": "Card_Spend", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "fact_purchase_orders.Total Procurement Spend ($)"}]}}})
                    },
                    {
                        "x": 340, "y": 20, "z": 1000, "width": 300, "height": 140,
                        "config": json.dumps({"name": "Card_OTIF", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "fact_purchase_orders.Supplier OTIF %"}]}}})
                    },
                    {
                        "x": 660, "y": 20, "z": 1000, "width": 300, "height": 140,
                        "config": json.dumps({"name": "Card_PPV", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "fact_purchase_orders.Total Purchase Price Variance (PPV)"}]}}})
                    },
                    {
                        "x": 980, "y": 20, "z": 1000, "width": 280, "height": 140,
                        "config": json.dumps({"name": "Card_Delayed", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "fact_purchase_orders.Delayed POs Count"}]}}})
                    }
                ]
            }
        ],
        "config": json.dumps({"version": "5.50", "themeCollection": {"baseTheme": {"name": "CY24SU08", "version": "5.50"}}})
    }

    # 4. Pack into .pbit
    pbit_path = "powerbi/Eaton_Procurement_Risk_Platform.pbit"
    content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="" />
  <Default Extension="xml" ContentType="application/xml" />
  <Override PartName="/DataModelSchema" ContentType="" />
  <Override PartName="/Report/Layout" ContentType="" />
  <Override PartName="/Settings" ContentType="" />
  <Override PartName="/Version" ContentType="" />
</Types>"""

    with zipfile.ZipFile(pbit_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("Version", "1.28".encode("utf-16-le"))
        zf.writestr("Settings", json.dumps({"version": "1.0"}))
        zf.writestr("DataModelSchema", json.dumps(data_model_schema, indent=2).encode("utf-16-le"))
        zf.writestr("Report/Layout", json.dumps(report_layout, indent=2).encode("utf-16-le"))

    print(f"  [OK] Assembled Power BI Template File (.pbit): {pbit_path}")

    # 5. Build .pbip Structure
    pbip_dir = "powerbi/Eaton_Procurement_Project.pbip"
    os.makedirs(f"{pbip_dir}/Eaton_Procurement.Report", exist_ok=True)
    os.makedirs(f"{pbip_dir}/Eaton_Procurement.Dataset", exist_ok=True)
    
    with open(f"{pbip_dir}/definition.pbip", "w") as f:
        json.dump({"version": "1.0", "artifacts": [{"report": {"path": "Eaton_Procurement.Report"}}]}, f, indent=2)
        
    with open(f"{pbip_dir}/Eaton_Procurement.Dataset/model.bim", "w") as f:
        json.dump(data_model_schema, f, indent=2)
        
    with open(f"{pbip_dir}/Eaton_Procurement.Report/report.json", "w") as f:
        json.dump(report_layout, f, indent=2)
        
    print(f"  [OK] Created Modern Power BI Project Format (.pbip): {pbip_dir}")
    print("=== Procurement Power BI Bundle Generation Complete! ===")

if __name__ == "__main__":
    create_procurement_bundle()
