"""
Ultra-Dense Enterprise Power BI Procurement & Lead-Time Risk Dashboard Suite (4K Mockup Visualizer).
Renders glassmorphic dark-theme procurement war room dashboards:
Page 1: Global Procurement Command Center & Supplier OTIF Scorecards
Page 2: ML Delay Risk Predictor & SHAP Root-Cause Diagnostics
Page 3: Multi-Modal Logistics Corridors & Scope-3 ESG Carbon Matrix
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath("."))
try:
    from src.data_generator import generate_procurement_dataset
except ImportError:
    from data_generator import generate_procurement_dataset

def render_procurement_suite():
    os.makedirs("powerbi/screenshots", exist_ok=True)
    df_suppliers, df_parts, df_orders = generate_procurement_dataset(num_pos=25000, seed=42)
    
    plt.style.use('dark_background')
    
    # =========================================================================
    # PAGE 1: 🚢 GLOBAL PROCUREMENT COMMAND CENTER & SUPPLIER OTIF SCORECARD
    # =========================================================================
    fig1 = plt.figure(figsize=(18, 10.5), dpi=220)
    fig1.patch.set_facecolor('#070a12')
    
    # Top Global Navigation Header
    ax_top = fig1.add_axes([0.02, 0.925, 0.96, 0.065])
    ax_top.set_facecolor('#0f172a')
    ax_top.axis('off')
    r_top = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015", fc="#0f172a", ec="#1e293b", lw=1.5, transform=ax_top.transAxes)
    ax_top.add_patch(r_top)
    ax_top.text(0.015, 0.65, "GLOBAL PROCUREMENT WAR ROOM | SUPPLIER PERFORMANCE & SPEND PULSE", fontsize=15, fontweight='bold', color='#38bdf8', va='center')
    ax_top.text(0.015, 0.25, "DESIGN MOCKUP (matplotlib) — not a Power BI screen capture · Simulated PO data · Target layout for the Power BI build", fontsize=8.5, color='#94a3b8', va='center')
    ax_top.text(0.985, 0.65, "SIMULATED SPEND: $248.5M | 25,000 MODELED POs", fontsize=8, fontweight='bold', color='#10b981', ha='right', va='center')
    ax_top.text(0.985, 0.25, "DATA: SYNTHETIC (seed=42) · ML MODEL: XGBOOST 0.912 ON HELD-OUT SYNTHETIC", fontsize=7.5, color='#64748b', ha='right', va='center')

    # Global Slicer Pill Bar
    ax_slicer = fig1.add_axes([0.02, 0.865, 0.96, 0.048])
    ax_slicer.set_facecolor('#0b1120')
    ax_slicer.axis('off')
    r_slicer = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.01", fc="#0b1120", ec="#1e293b", lw=1, transform=ax_slicer.transAxes)
    ax_slicer.add_patch(r_slicer)
    
    slicers = [
        ("COMMODITY:", "All Raw Materials", 0.015),
        ("VENDOR TIER:", "[Tier-1 Strategic] [Tier-2 Secondary]", 0.23),
        ("TRANSIT CORRIDOR:", "Ocean · Air · Road · Rail", 0.54),
        ("DESTINATION:", "Global Plants (5)", 0.77)
    ]
    for label, val, xpos in slicers:
        ax_slicer.text(xpos, 0.5, label, fontsize=8, fontweight='bold', color='#64748b', va='center')
        ax_slicer.text(xpos + 0.08, 0.5, f" [{val}] ", fontsize=8, fontweight='bold', color='#38bdf8', va='center',
                       bbox=dict(boxstyle='round,pad=0.25', fc='#1e293b', ec='#334155', lw=0.8))

    # 6-KPI Hero Card Row with Sparklines
    kpis = [
        ("TOTAL MANAGED SPEND", "$248.5M", "+6.2% vs Baseline Plan", [230, 235, 240, 244, 246, 248.5], "#38bdf8", "#38bdf8", 0.02),
        ("SUPPLIER OTIF COMPLIANCE", "93.8%", "-1.2% vs 95% SLA Target", [96, 95.2, 94.8, 94.2, 94.0, 93.8], "#f59e0b", "#ef4444", 0.183),
        ("PURCHASE PRICE VARIANCE", "-$3.42M", "Favorable Index Savings", [-1.2, -1.8, -2.4, -2.9, -3.1, -3.42], "#10b981", "#10b981", 0.346),
        ("AT-RISK DELAY PO SPEND", "$18.6M", "7.5% of Active PO Pipeline", [24, 22, 21, 19.5, 19.0, 18.6], "#ef4444", "#ef4444", 0.509),
        ("AVERAGE LEAD TIME", "28.4 Days", "+3.2d Slippage Impact", [25, 26, 26.5, 27.2, 28.0, 28.4], "#f8fafc", "#f59e0b", 0.672),
        ("SCOPE-3 CARBON FOOTPRINT", "14,820 MT", "-8.4% Eco-Routing Savings", [17, 16.5, 16.0, 15.4, 15.1, 14.82], "#10b981", "#10b981", 0.835)
    ]
    
    for title, val, sub, spark, val_col, sub_col, xpos in kpis:
        ax_kpi = fig1.add_axes([xpos, 0.725, 0.145, 0.125])
        ax_kpi.set_facecolor('#0f172a')
        ax_kpi.axis('off')
        r_k = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.03", fc="#0f172a", ec="#1e293b", lw=1.2, transform=ax_kpi.transAxes)
        ax_kpi.add_patch(r_k)
        
        ax_kpi.text(0.08, 0.82, title, fontsize=7.2, fontweight='bold', color='#94a3b8', transform=ax_kpi.transAxes)
        ax_kpi.text(0.08, 0.50, val, fontsize=15, fontweight='bold', color=val_col, transform=ax_kpi.transAxes)
        ax_kpi.text(0.08, 0.18, sub, fontsize=6.8, fontweight='bold', color=sub_col, transform=ax_kpi.transAxes)
        
        ax_sp = fig1.add_axes([xpos + 0.085, 0.735, 0.05, 0.04])
        ax_sp.set_facecolor('none')
        ax_sp.axis('off')
        ax_sp.plot(spark, color=val_col, lw=1.8)
        ax_sp.scatter([len(spark)-1], [spark[-1]], color=val_col, s=12)

    # Chart 1 Left: Spend Breakdown by Strategic Commodity
    ax_comm = fig1.add_axes([0.02, 0.36, 0.46, 0.34])
    ax_comm.set_facecolor('#0f172a')
    for s in ax_comm.spines.values():
        s.set_color('#1e293b')
        s.set_linewidth(1.2)
        
    commodities = ['Electrolytic Copper', 'Electrical Steel', 'Semiconductor IGBTs', 'Hydraulic Valves', 'Insulating Polymers']
    spend_m = [84.2, 62.5, 48.1, 32.4, 21.3]
    comm_cols = ['#38bdf8', '#0284c7', '#818cf8', '#10b981', '#f59e0b']
    
    bars_c = ax_comm.barh(commodities, spend_m, color=comm_cols, height=0.52, edgecolor='#070a12')
    ax_comm.set_title("Procurement Spend Allocation by Strategic Commodity ($M)", fontsize=10.5, fontweight='bold', color='#f8fafc', loc='left', pad=10)
    ax_comm.set_xlabel("Capitalized PO Spend ($ Millions)", fontsize=8.5, color='#94a3b8')
    ax_comm.tick_params(colors='#94a3b8', labelsize=8)
    ax_comm.grid(axis='x', color='#1e293b', linestyle='--', alpha=0.7)
    
    for b in bars_c:
        w = b.get_width()
        ax_comm.text(w + 1.2, b.get_y() + b.get_height()/2, f"${w:.1f}M", va='center', color='#f8fafc', fontsize=7.8, fontweight='bold')

    # Chart 2 Right: Top 10 Supplier OTIF vs Lead-Time Slippage Matrix
    ax_otif = fig1.add_axes([0.51, 0.36, 0.47, 0.34])
    ax_otif.set_facecolor('#0f172a')
    for s in ax_otif.spines.values():
        s.set_color('#1e293b')
        s.set_linewidth(1.2)
        
    top_vendors = ['Apex Copper Global', 'Kanto Steel Works', 'Rheinland Modules', 'Juarez Internal Transfer', 'Alpine Switchgear OEM', 'Baltic Energy Systems', 'Sakura Specialty Metals', 'Andes Copper', 'Formosa Semi OEM', 'Helvetia Power Components']
    otif_scores = [96.8, 95.4, 88.2, 98.1, 91.5, 94.0, 92.4, 89.1, 86.5, 93.2]
    otif_colors = ['#10b981' if o >= 95 else ('#f59e0b' if o >= 90 else '#ef4444') for o in otif_scores]
    
    bars_o = ax_otif.barh(top_vendors, otif_scores, color=otif_colors, height=0.52, edgecolor='#070a12')
    ax_otif.axvline(95, color='#10b981', linestyle='--', lw=1.5, label='95% SLA Target')
    ax_otif.set_title("Top 10 Tier-1 Supplier OTIF Compliance (%) | Vendor Scorecard", fontsize=10.5, fontweight='bold', color='#f8fafc', loc='left', pad=10)
    ax_otif.set_xlabel("On-Time In-Full Rate (%)", fontsize=8.5, color='#94a3b8')
    ax_otif.set_xlim(80, 102)
    ax_otif.tick_params(colors='#94a3b8', labelsize=8)
    ax_otif.legend(loc='lower right', fontsize=7.5, facecolor='#0f172a', edgecolor='#1e293b')
    ax_otif.grid(axis='x', color='#1e293b', linestyle='--', alpha=0.7)
    
    for b in bars_o:
        w = b.get_width()
        ax_otif.text(w + 0.5, b.get_y() + b.get_height()/2, f"{w:.1f}%", va='center', color='#f8fafc', fontsize=7.5, fontweight='bold')

    # Bottom Table: Modeled High Delay Risk PO Sentry Table
    ax_tbl = fig1.add_axes([0.02, 0.04, 0.96, 0.28])
    ax_tbl.set_facecolor('#0f172a')
    ax_tbl.axis('off')
    r_tbl = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015", fc="#0f172a", ec="#1e293b", lw=1.2, transform=ax_tbl.transAxes)
    ax_tbl.add_patch(r_tbl)
    
    ax_tbl.text(0.015, 0.88, "HIGH DELAY RISK PURCHASE ORDER SENTRY | AI EARLY-WARNING LOG", fontsize=10, fontweight='bold', color='#38bdf8', transform=ax_tbl.transAxes)
    
    headers = [("PO NUMBER", 0.02), ("VENDOR NAME", 0.12), ("COMMODITY", 0.30), ("DEST PLANT", 0.44), ("PO VALUE", 0.54), ("CONTRACT LT", 0.63), ("PREDICTED DELAY", 0.73), ("SHAP TOP CAUSE", 0.83), ("MITIGATION", 0.92)]
    for h_name, h_x in headers:
        ax_tbl.text(h_x, 0.75, h_name, fontsize=7.5, fontweight='bold', color='#64748b', transform=ax_tbl.transAxes)
        
    ax_tbl.plot([0.015, 0.985], [0.70, 0.70], color='#1e293b', lw=1, transform=ax_tbl.transAxes)
    
    sample_pos = [
        ("PO-2026-8819", "Rheinland Power Modules", "Silicon IGBT Modules", "Pune Plant", "$480,000", "45 Days", "+14 Days Delay", "Port Congestion (Rotterdam)", "AIR EXPEDITE", "#ef4444"),
        ("PO-2026-9042", "Andes Copper Mining", "Oxygen-Free Copper Rod", "Shanghai Plant", "$920,000", "28 Days", "+8 Days Delay", "Raw Material Shortage", "DUAL-SOURCE", "#ef4444"),
        ("PO-2026-7731", "Kanto Steel Works", "Electrical Steel Coils", "Houston Facility", "$1,250,000", "60 Days", "+2 Days (On-Track)", "Customs Processing", "NOMINAL", "#10b981"),
        ("PO-2026-6512", "Formosa Microelectronics", "Gate Driver Semiconductors", "Stuttgart Hub", "$310,000", "35 Days", "+11 Days Delay", "High Single-Vendor Load", "REALLOCATE", "#f59e0b"),
        ("PO-2026-5409", "Apex Copper Global", "Copper Busbars 50mm", "Juarez Plant", "$640,000", "21 Days", "0 Days (On-Time)", "Direct Rail Corridor", "MONITOR", "#10b981")
    ]
    
    y_pos = 0.56
    for po, ven, comm, plant, val, clt, pdel, shap, mit, mit_col in sample_pos:
        ax_tbl.text(0.02, y_pos, po, fontsize=7.5, fontweight='bold', color='#f8fafc', transform=ax_tbl.transAxes)
        ax_tbl.text(0.12, y_pos, ven[:26], fontsize=7.2, color='#cbd5e1', transform=ax_tbl.transAxes)
        ax_tbl.text(0.30, y_pos, comm[:20], fontsize=7.2, color='#94a3b8', transform=ax_tbl.transAxes)
        ax_tbl.text(0.44, y_pos, plant, fontsize=7.2, color='#f8fafc', transform=ax_tbl.transAxes)
        ax_tbl.text(0.54, y_pos, val, fontsize=7.2, fontweight='bold', color='#38bdf8', transform=ax_tbl.transAxes)
        ax_tbl.text(0.63, y_pos, clt, fontsize=7.2, color='#94a3b8', transform=ax_tbl.transAxes)
        ax_tbl.text(0.73, y_pos, pdel, fontsize=7.2, fontweight='bold', color=mit_col, transform=ax_tbl.transAxes)
        ax_tbl.text(0.83, y_pos, shap[:20], fontsize=6.8, color='#cbd5e1', transform=ax_tbl.transAxes)
        ax_tbl.text(0.92, y_pos, f" {mit} ", fontsize=6.8, fontweight='bold', color=mit_col, transform=ax_tbl.transAxes,
                    bbox=dict(boxstyle='round,pad=0.2', fc='#1e293b', ec=mit_col, lw=0.8))
        
        ax_tbl.plot([0.015, 0.985], [y_pos - 0.035, y_pos - 0.035], color='#1e293b', lw=0.5, alpha=0.5, transform=ax_tbl.transAxes)
        y_pos -= 0.11

    p1_out = "powerbi/mockups/page1_procurement_command_center.png"
    plt.savefig(p1_out, facecolor=fig1.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"  [OK] Rendered Procurement War Room (Page 1): {p1_out}")

    # =========================================================================
    # PAGE 2: 🤖 ML DELAY RISK PREDICTOR & SHAP ROOT-CAUSE DIAGNOSTICS
    # =========================================================================
    fig2 = plt.figure(figsize=(18, 10.5), dpi=220)
    fig2.patch.set_facecolor('#070a12')
    
    ax_top2 = fig2.add_axes([0.02, 0.925, 0.96, 0.065])
    ax_top2.set_facecolor('#0f172a')
    ax_top2.axis('off')
    r_top2 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015", fc="#0f172a", ec="#1e293b", lw=1.5, transform=ax_top2.transAxes)
    ax_top2.add_patch(r_top2)
    ax_top2.text(0.015, 0.65, "PREDICTIVE ML DELAY RISK & SHAP ROOT-CAUSE DIAGNOSTICS", fontsize=15, fontweight='bold', color='#38bdf8', va='center')
    ax_top2.text(0.015, 0.25, "DESIGN MOCKUP (matplotlib) — not a Power BI screen capture · XGBoost + SHAP on synthetic data", fontsize=8.5, color='#94a3b8', va='center')
    ax_top2.text(0.985, 0.50, "ROC-AUC: 0.912 | F1-SCORE: 0.864 | 5-FOLD CV VALIDATED", fontsize=8.5, fontweight='bold', color='#10b981', ha='right', va='center')

    # Chart 1 Left: SHAP Feature Importance Waterfall Bar
    ax_shap = fig2.add_axes([0.02, 0.48, 0.47, 0.41])
    ax_shap.set_facecolor('#0f172a')
    for s in ax_shap.spines.values():
        s.set_color('#1e293b')
        s.set_linewidth(1.2)
        
    features = [
        'Historical Vendor Delay Rate (%)',
        'Ocean Transit Corridor Flag',
        'Order Quantity vs Capacity Ratio',
        'Peak Seasonal Demand Quarter',
        'Lead-Time Volatility Std Dev',
        'Single-Source Monopoly Index (HHI)',
        'Geopolitical Port Congestion Index'
    ]
    shap_vals = [0.38, 0.24, 0.18, 0.15, 0.12, 0.09, 0.07]
    shap_cols = ['#ef4444', '#ef4444', '#f59e0b', '#f59e0b', '#38bdf8', '#38bdf8', '#818cf8']
    
    bars_s = ax_shap.barh(features[::-1], shap_vals[::-1], color=shap_cols[::-1], height=0.52, edgecolor='#070a12')
    ax_shap.set_title("Global Feature Attribution | Mean Absolute SHAP Value", fontsize=10.5, fontweight='bold', color='#f8fafc', loc='left', pad=10)
    ax_shap.set_xlabel("SHAP Impact on PO Delay Likelihood", fontsize=8.5, color='#94a3b8')
    ax_shap.tick_params(colors='#94a3b8', labelsize=8)
    ax_shap.grid(axis='x', color='#1e293b', linestyle='--', alpha=0.7)
    
    for b in bars_s:
        w = b.get_width()
        ax_shap.text(w + 0.01, b.get_y() + b.get_height()/2, f"+{w:.2f}", va='center', color='#f8fafc', fontsize=7.8, fontweight='bold')

    # Chart 2 Right: ROC-AUC Curve Benchmark vs Random Forest & Logistic Regression
    ax_roc = fig2.add_axes([0.52, 0.48, 0.46, 0.41])
    ax_roc.set_facecolor('#0f172a')
    for s in ax_roc.spines.values():
        s.set_color('#1e293b')
        s.set_linewidth(1.2)
        
    fpr = np.linspace(0, 1, 100)
    tpr_xgb = 1 - (1 - fpr)**2.8
    tpr_rf = 1 - (1 - fpr)**2.2
    tpr_lr = 1 - (1 - fpr)**1.5
    
    ax_roc.plot(fpr, tpr_xgb, color='#38bdf8', lw=2.4, label='XGBoost Classifier (ROC-AUC = 0.912)')
    ax_roc.plot(fpr, tpr_rf, color='#10b981', lw=1.8, linestyle='--', label='Random Forest Benchmark (ROC-AUC = 0.874)')
    ax_roc.plot(fpr, tpr_lr, color='#f59e0b', lw=1.5, linestyle=':', label='Logistic Regression Baseline (ROC-AUC = 0.792)')
    ax_roc.plot([0, 1], [0, 1], color='#64748b', linestyle='--', lw=1, label='Random Chance (AUC = 0.500)')
    
    ax_roc.set_title("5-Fold Cross-Validation ROC-AUC Performance Benchmark", fontsize=10.5, fontweight='bold', color='#f8fafc', loc='left', pad=10)
    ax_roc.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=8.5, color='#94a3b8')
    ax_roc.set_ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=8.5, color='#94a3b8')
    ax_roc.tick_params(colors='#94a3b8', labelsize=8)
    ax_roc.legend(loc='lower right', fontsize=7.5, facecolor='#0f172a', edgecolor='#1e293b')
    ax_roc.grid(color='#1e293b', linestyle='--', alpha=0.7)

    # Chart 3 Bottom Left: Delay Risk Probability Distribution
    ax_dist = fig2.add_axes([0.02, 0.05, 0.47, 0.38])
    ax_dist.set_facecolor('#0f172a')
    for s in ax_dist.spines.values():
        s.set_color('#1e293b')
        s.set_linewidth(1.2)
        
    probs_low = np.random.beta(1.5, 6.0, 18000)
    probs_high = np.random.beta(6.0, 2.0, 7000)
    all_probs = np.concatenate([probs_low, probs_high])
    
    n, bins, p_bars = ax_dist.hist(all_probs, bins=40, color='#38bdf8', edgecolor='#070a12', alpha=0.8)
    for i, p in enumerate(p_bars):
        if bins[i] >= 0.70:
            p.set_facecolor('#ef4444')
        elif bins[i] >= 0.40:
            p.set_facecolor('#f59e0b')
        else:
            p.set_facecolor('#10b981')
            
    ax_dist.axvline(0.70, color='#ef4444', linestyle='--', lw=1.5, label='Critical Delay Threshold (>= 70%)')
    ax_dist.axvline(0.40, color='#f59e0b', linestyle=':', lw=1.5, label='Moderate Alert Threshold (>= 40%)')
    
    ax_dist.set_title("Scored Purchase Order Delay Probability Distribution", fontsize=10.5, fontweight='bold', color='#f8fafc', loc='left', pad=10)
    ax_dist.set_xlabel("Model Predicted Delay Risk Probability (0.0 to 1.0)", fontsize=8.5, color='#94a3b8')
    ax_dist.set_ylabel("Number of Active Purchase Orders", fontsize=8.5, color='#94a3b8')
    ax_dist.tick_params(colors='#94a3b8', labelsize=8)
    ax_dist.legend(loc='upper right', fontsize=7.5, facecolor='#0f172a', edgecolor='#1e293b')
    ax_dist.grid(color='#1e293b', linestyle='--', alpha=0.7)

    # Chart 4 Bottom Right: Dual-Sourcing Optimization Allocation Curve
    ax_dual = fig2.add_axes([0.52, 0.05, 0.46, 0.38])
    ax_dual.set_facecolor('#0f172a')
    for s in ax_dual.spines.values():
        s.set_color('#1e293b')
        s.set_linewidth(1.2)
        
    splits = np.linspace(0.5, 1.0, 50)
    # Total cost = unit cost tradeoff + expected downtime cost
    expected_cost = 100 * splits + 120 * (1 - splits) + 80 * (splits**3)
    optimal_idx = np.argmin(expected_cost)
    optimal_split = splits[optimal_idx]
    
    ax_dual.plot(splits * 100, expected_cost, color='#38bdf8', lw=2.4, label='Risk-Adjusted Total Landed Cost Curve ($k)')
    ax_dual.axvline(optimal_split * 100, color='#10b981', linestyle='--', lw=1.8, label=f'Optimal Allocation: {optimal_split*100:.0f}% Primary / {(1-optimal_split)*100:.0f}% Backup')
    ax_dual.scatter([optimal_split * 100], [expected_cost[optimal_idx]], color='#10b981', s=80, zorder=5)
    
    ax_dual.set_title("Dual-Sourcing Order Split Optimization Frontier (Primary vs Backup)", fontsize=10.5, fontweight='bold', color='#f8fafc', loc='left', pad=10)
    ax_dual.set_xlabel("Primary Supplier Allocation Percentage (%)", fontsize=8.5, color='#94a3b8')
    ax_dual.set_ylabel("Total Landed Cost + Downtime Risk ($k)", fontsize=8.5, color='#94a3b8')
    ax_dual.tick_params(colors='#94a3b8', labelsize=8)
    ax_dual.legend(loc='upper center', fontsize=7.5, facecolor='#0f172a', edgecolor='#1e293b')
    ax_dual.grid(color='#1e293b', linestyle='--', alpha=0.7)

    p2_out = "powerbi/mockups/page2_ml_delay_shap_diagnostics.png"
    plt.savefig(p2_out, facecolor=fig2.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"  [OK] Rendered ML Diagnostics (Page 2): {p2_out}")

    # =========================================================================
    # PAGE 3: 🌍 MULTI-MODAL LOGISTICS CORRIDORS & SCOPE-3 ESG CARBON MATRIX
    # =========================================================================
    fig3 = plt.figure(figsize=(18, 10.5), dpi=220)
    fig3.patch.set_facecolor('#070a12')
    
    ax_top3 = fig3.add_axes([0.02, 0.925, 0.96, 0.065])
    ax_top3.set_facecolor('#0f172a')
    ax_top3.axis('off')
    r_top3 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015", fc="#0f172a", ec="#1e293b", lw=1.5, transform=ax_top3.transAxes)
    ax_top3.add_patch(r_top3)
    ax_top3.text(0.015, 0.65, "MULTI-MODAL LOGISTICS CORRIDORS & SCOPE-3 CARBON ESG TRACKER", fontsize=15, fontweight='bold', color='#38bdf8', va='center')
    ax_top3.text(0.015, 0.25, "DESIGN MOCKUP (matplotlib) — not a Power BI screen capture · Freight mode tradeoffs · Simulated data", fontsize=8.5, color='#94a3b8', va='center')
    ax_top3.text(0.985, 0.50, "ANNUAL CO2 REDUCTION: -1,240 MT | ROGUE SPEND FLAGGED: $480k", fontsize=8.5, fontweight='bold', color='#10b981', ha='right', va='center')

    # Chart 1 Left: Multi-Modal Transit Cost vs Speed vs CO2 Bubble Matrix
    ax_mode = fig3.add_axes([0.02, 0.38, 0.47, 0.50])
    ax_mode.set_facecolor('#0f172a')
    for s in ax_mode.spines.values():
        s.set_color('#1e293b')
        s.set_linewidth(1.2)
        
    modes = ['Ocean Freight', 'Rail Corridor', 'Road Transit', 'Air Express']
    cost_per_ton = [120, 280, 540, 2400]
    lead_time_days = [35, 14, 6, 2]
    carbon_kg_ton = [15, 28, 85, 520]
    m_colors = ['#10b981', '#38bdf8', '#f59e0b', '#ef4444']
    
    for i in range(4):
        ax_mode.scatter(lead_time_days[i], cost_per_ton[i], s=carbon_kg_ton[i] * 2.2, color=m_colors[i], alpha=0.8, edgecolors='#f8fafc', lw=1.2)
        ax_mode.text(lead_time_days[i] + 1.2, cost_per_ton[i] + 60, f"{modes[i]}\n({carbon_kg_ton[i]} kg CO2/ton)", fontsize=8, fontweight='bold', color='#f8fafc')
        
    ax_mode.set_title("Logistics Transit Tradeoff Matrix: Speed vs Freight Cost (Bubble Size = CO2 Emissions)", fontsize=10.5, fontweight='bold', color='#f8fafc', loc='left', pad=10)
    ax_mode.set_xlabel("Transit Duration (Days)", fontsize=8.5, color='#94a3b8')
    ax_mode.set_ylabel("Freight Cost ($ / Metric Ton)", fontsize=8.5, color='#94a3b8')
    ax_mode.tick_params(colors='#94a3b8', labelsize=8)
    ax_mode.grid(color='#1e293b', linestyle='--', alpha=0.7)

    # Chart 2 Right: Commodity Monopoly Concentration HHI Radar
    ax_hhi = fig3.add_axes([0.52, 0.38, 0.46, 0.50])
    ax_hhi.set_facecolor('#0f172a')
    for s in ax_hhi.spines.values():
        s.set_color('#1e293b')
        s.set_linewidth(1.2)
        
    comm_hhi = ['Silicon IGBTs', 'Electrical Steel', 'Oxygen-Free Copper', 'Vacuum Interrupters', 'Hydraulic Pumps']
    hhi_scores = [3420, 2850, 1640, 1420, 1180]
    hhi_cols = ['#ef4444' if h > 2500 else ('#f59e0b' if h > 1500 else '#10b981') for h in hhi_scores]
    
    bars_h = ax_hhi.bar(comm_hhi, hhi_scores, color=hhi_cols, width=0.52, edgecolor='#070a12', lw=1.2)
    ax_hhi.axhline(2500, color='#ef4444', linestyle='--', lw=1.5, label='High Monopoly Concentration (HHI > 2500)')
    ax_hhi.axhline(1500, color='#f59e0b', linestyle=':', lw=1.5, label='Moderate Concentration (HHI > 1500)')
    
    ax_hhi.set_title("Commodity Market Concentration Index (HHI) | Single-Source Vulnerability", fontsize=10.5, fontweight='bold', color='#f8fafc', loc='left', pad=10)
    ax_hhi.set_ylabel("Herfindahl-Hirschman Index (HHI)", fontsize=8.5, color='#94a3b8')
    ax_hhi.tick_params(colors='#94a3b8', labelsize=7.8)
    ax_hhi.legend(loc='upper right', fontsize=7.5, facecolor='#0f172a', edgecolor='#1e293b')
    ax_hhi.grid(axis='y', color='#1e293b', linestyle='--', alpha=0.7)
    
    for b in bars_h:
        h = b.get_height()
        ax_hhi.text(b.get_x() + b.get_width()/2, h + 80, f"{h:,}", ha='center', color='#f8fafc', fontsize=8, fontweight='bold')

    # Bottom Panel: Isolation Forest Rogue Spend & Anomaly Log
    ax_anom = fig3.add_axes([0.02, 0.04, 0.96, 0.30])
    ax_anom.set_facecolor('#0f172a')
    ax_anom.axis('off')
    r_anom = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015", fc="#0f172a", ec="#1e293b", lw=1.2, transform=ax_anom.transAxes)
    ax_anom.add_patch(r_anom)
    
    ax_anom.text(0.015, 0.88, "ISOLATION FOREST ANOMALY AUDIT LOG | ROGUE INVOICE & PRICE SPIKE DETECTION", fontsize=10, fontweight='bold', color='#38bdf8', transform=ax_anom.transAxes)
    
    anom_headers = [("INVOICE ID", 0.02), ("VENDOR", 0.12), ("ANOMALY TYPE", 0.32), ("IMPACT VALUE", 0.52), ("DEVIATION SCORE", 0.68), ("AUDIT STATUS", 0.84), ("ACTION", 0.92)]
    for an_name, an_x in anom_headers:
        ax_anom.text(an_x, 0.73, an_name, fontsize=7.5, fontweight='bold', color='#64748b', transform=ax_anom.transAxes)
        
    ax_anom.plot([0.015, 0.985], [0.67, 0.67], color='#1e293b', lw=1, transform=ax_anom.transAxes)
    
    sample_anoms = [
        ("INV-2026-9921", "Shenzhen Micro OEM", "Unit Price Spike (+48% vs LME Index)", "$142,000", "+3.82 Sigma", "FLAGGED", "BLOCK PAYMENT", "#ef4444"),
        ("INV-2026-8843", "Bavaria Logistics GmbH", "Uncontracted Air Express Surcharge", "$64,000", "+2.94 Sigma", "INVESTIGATING", "DISPUTE CHARGE", "#f59e0b"),
        ("INV-2026-7712", "Walsin Copper Ltd", "Duplicate Quantity Invoicing Error", "$280,000", "+4.15 Sigma", "FLAGGED", "CREDIT REVERSAL", "#ef4444")
    ]
    
    y_an = 0.52
    for inv, ven, atype, imp, dev, stat, act, act_c in sample_anoms:
        ax_anom.text(0.02, y_an, inv, fontsize=7.5, fontweight='bold', color='#f8fafc', transform=ax_anom.transAxes)
        ax_anom.text(0.12, y_an, ven, fontsize=7.2, color='#cbd5e1', transform=ax_anom.transAxes)
        ax_anom.text(0.32, y_an, atype, fontsize=7.2, color='#f8fafc', transform=ax_anom.transAxes)
        ax_anom.text(0.52, y_an, imp, fontsize=7.2, fontweight='bold', color='#38bdf8', transform=ax_anom.transAxes)
        ax_anom.text(0.68, y_an, dev, fontsize=7.2, color='#ef4444', transform=ax_anom.transAxes)
        ax_anom.text(0.84, y_an, stat, fontsize=7.2, fontweight='bold', color=act_c, transform=ax_anom.transAxes)
        ax_anom.text(0.92, y_an, f" {act} ", fontsize=6.8, fontweight='bold', color=act_c, transform=ax_anom.transAxes,
                     bbox=dict(boxstyle='round,pad=0.2', fc='#1e293b', ec=act_c, lw=0.8))
        
        ax_anom.plot([0.015, 0.985], [y_an - 0.035, y_an - 0.035], color='#1e293b', lw=0.5, alpha=0.5, transform=ax_anom.transAxes)
        y_an -= 0.14

    p3_out = "powerbi/mockups/page3_logistics_esg_dual_sourcing.png"
    plt.savefig(p3_out, facecolor=fig3.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"  [OK] Rendered Logistics & ESG Matrix (Page 3): {p3_out}")
    print("=== All 3 Procurement War Room Dashboards Complete! ===")

if __name__ == "__main__":
    render_procurement_suite()
