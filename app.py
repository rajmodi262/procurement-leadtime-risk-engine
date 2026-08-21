"""
Interactive Executive Streamlit Dashboard for Global Procurement & Predictive Lead-Time Risk Platform.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.data_generator import generate_procurement_dataset
from src.procurement_analytics import ProcurementAnalyticsEngine
from src.anomaly_detector import ProcurementAnomalyDetector
from src.ml_delay_predictor import DelayRiskPredictor

st.set_page_config(
    page_title="Eaton Global Procurement & Risk Platform",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme custom CSS
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; }
    .risk-high { color: #f85149; font-weight: bold; }
    .risk-low { color: #56d364; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return generate_procurement_dataset(num_pos=15000, seed=42)

df_suppliers, df_parts, df_pos = load_data()

@st.cache_resource
def train_model(df):
    predictor = DelayRiskPredictor(random_state=42)
    metrics = predictor.train(df)
    return predictor, metrics

predictor, ml_metrics = train_model(df_pos)
analytics = ProcurementAnalyticsEngine(df_pos, df_suppliers)
anomaly_detector = ProcurementAnomalyDetector()
df_anomalies = anomaly_detector.fit_detect(df_pos)

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Eaton_Corporation_logo.svg/320px-Eaton_Corporation_logo.svg.png", width=160)
st.sidebar.title("Procurement AI Suite")
st.sidebar.markdown("---")

selected_tiers = st.sidebar.multiselect("Supplier Tier", options=df_suppliers["tier_level"].unique().tolist(), default=df_suppliers["tier_level"].unique().tolist())
selected_commodities = st.sidebar.multiselect("Commodity Category", options=df_parts["commodity_group"].unique().tolist(), default=df_parts["commodity_group"].unique().tolist())

st.sidebar.markdown("---")
st.sidebar.info(f"🤖 **Predictive Model**: XGBoost\n* **ROC-AUC**: `{ml_metrics['roc_auc']}`\n* **F1-Score**: `{ml_metrics['f1_score']}`")

# Main Header
st.title("🌐 Global Procurement & Predictive Lead-Time Risk Platform")
st.markdown("**Strategic Spend Analytics** · OTIF & PPV Tracking · Anomaly Detection · XGBoost Delay Risk Forecasting")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive Spend & OTIF Scorecard",
    "🗺️ Supplier Vulnerability & HHI Matrix",
    "🤖 Real-Time PO Delay Risk Predictor",
    "🚨 Price & Lead-Time Anomaly Auditor"
])

with tab1:
    exec_summary = analytics.get_executive_summary()
    hhi_summary = analytics.calculate_herfindahl_index()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Procurement Spend", f"${exec_summary['total_spend_usd']:,.0f}", f"{exec_summary['total_pos']:,} Purchase Orders")
    with col2:
        st.metric("On-Time In-Full (OTIF)", f"{exec_summary['otif_percentage']:.1f}%", f"{exec_summary['on_time_percentage']:.1f}% On-Time", delta_color="normal" if exec_summary['otif_percentage'] >= 85 else "inverse")
    with col3:
        st.metric("Purchase Price Variance (PPV)", f"${exec_summary['total_ppv_usd']:+,.0f}", "Inflation / Spot Variance", delta_color="inverse")
    with col4:
        st.metric("Supplier Concentration (HHI)", f"{hhi_summary['hhi_index']}", hhi_summary['concentration_tier'])
        
    st.markdown("###")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.subheader("Purchase Price Variance (PPV) by Commodity Category")
        df_comm = analytics.get_commodity_spend_and_ppv()
        fig_ppv = px.bar(
            df_comm, x="commodity_group", y="total_ppv_usd",
            color="total_ppv_usd", color_continuous_scale="Reds",
            labels={"commodity_group": "Commodity Group", "total_ppv_usd": "Net PPV ($)"},
            template="plotly_dark"
        )
        st.plotly_chart(fig_ppv, use_container_width=True)
    with c2:
        st.subheader("OTIF Delivery Rate by Commodity")
        fig_otif = px.bar(
            df_comm, x="commodity_group", y="otif_rate_pct",
            color="otif_rate_pct", color_continuous_scale="Tealgrn",
            labels={"commodity_group": "Commodity", "otif_rate_pct": "OTIF %"},
            template="plotly_dark"
        )
        fig_otif.add_hline(y=90.0, line_dash="dash", line_color="orange", annotation_text="90% Target")
        st.plotly_chart(fig_otif, use_container_width=True)

with tab2:
    st.subheader("Vendor Performance & Single-Source Vulnerability Matrix")
    df_scorecard = analytics.get_supplier_scorecard()
    
    fig_vendor = px.scatter(
        df_scorecard, x="otif_rate_pct", y="avg_actual_lead_time",
        size="total_spend_usd", color="is_single_source",
        hover_data=["supplier_name", "commodity_category", "tier_level", "total_ppv_usd"],
        labels={"otif_rate_pct": "OTIF Delivery Compliance (%)", "avg_actual_lead_time": "Average Lead Time (Days)", "is_single_source": "Single Source Dependency"},
        template="plotly_dark", color_discrete_map={True: "#f85149", False: "#56d364"}
    )
    st.plotly_chart(fig_vendor, use_container_width=True)
    
    st.subheader("Supplier Scorecard Detail")
    st.dataframe(df_scorecard, use_container_width=True)

with tab3:
    st.subheader("AI Delay Risk Predictor (XGBoost + SHAP Explainability)")
    st.markdown("Score any new incoming Purchase Order at creation time to evaluate the probability of factory delivery delay.")
    
    with st.form("po_scoring_form"):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            inp_supplier = st.selectbox("Select Supplier", options=df_suppliers["supplier_id"].tolist(), format_func=lambda x: f"{x} - {df_suppliers.loc[df_suppliers['supplier_id']==x, 'supplier_name'].values[0]}")
            inp_comm = st.selectbox("Commodity Category", options=df_parts["commodity_group"].unique().tolist())
        with fc2:
            inp_freight = st.selectbox("Freight Mode", options=["Ocean", "Road Freight", "Air Express"])
            inp_plant = st.selectbox("Destination Plant", options=["PL-PUN (Pune)", "PL-TEX (Texas)", "PL-SHA (Shanghai)", "PL-STU (Stuttgart)", "PL-JUA (Juarez)"]).split(" ")[0]
        with fc3:
            inp_lt = st.number_input("Contracted Lead Time (Days)", min_value=5, max_value=90, value=30)
            inp_qty = st.number_input("Order Quantity", min_value=10, max_value=50000, value=1000)
            inp_congestion = st.slider("Port / Route Congestion Index", min_value=1.0, max_value=2.5, value=1.2, step=0.1)
            
        btn_score = st.form_submit_button("⚡ Predict Inbound Delay Probability")
        
    if btn_score:
        sup_country = df_suppliers.loc[df_suppliers["supplier_id"] == inp_supplier, "headquarters_country"].values[0]
        test_df = pd.DataFrame([{
            "supplier_id": inp_supplier,
            "commodity_group": inp_comm,
            "freight_mode": inp_freight,
            "origin_country": sup_country,
            "destination_plant_id": inp_plant,
            "contracted_lead_time_days": inp_lt,
            "ordered_quantity": float(inp_qty),
            "po_unit_price_usd": 25.0,
            "port_congestion_index": inp_congestion
        }])
        
        scored_po = predictor.predict_delay_risk(test_df)
        prob = scored_po["predicted_delay_probability"].values[0]
        tier = scored_po["risk_tier"].values[0]
        
        r1, r2 = st.columns([1, 2])
        with r1:
            st.metric("Predicted Delay Probability", f"{prob*100:.1f}%", tier, delta_color="inverse" if prob >= 0.40 else "normal")
        with r2:
            if prob >= 0.70:
                st.error(f"🚨 **High Risk Alert**: This PO has a **{prob*100:.1f}% risk of delay**. Recommendation: Trigger buffer stock escalation or switch freight lane to Air Express.")
            elif prob >= 0.40:
                st.warning(f"⚠️ **Moderate Risk**: Probability of delay **{prob*100:.1f}%**. Monitor supplier dispatch closely.")
            else:
                st.success(f"✅ **Low Delay Risk**: Probability of delay **{prob*100:.1f}%**. On-time delivery expected.")

with tab4:
    st.subheader("🚨 Isolation Forest Anomaly Detection Auditor")
    st.markdown("Identifies outlier PO prices, contract unit price deviations, and rogue delivery bottlenecks.")
    
    flagged = anomaly_detector.get_flagged_anomalies(df_anomalies)
    st.warning(f"Audited {len(df_pos):,} Purchase Orders. **{len(flagged):,} anomalies flagged** for procurement auditing.")
    
    st.dataframe(
        flagged[["po_number", "supplier_name", "commodity_group", "po_unit_price_usd", "standard_unit_cost_usd", "price_variance_ratio", "days_delayed", "anomaly_score"]].head(100),
        use_container_width=True
    )
