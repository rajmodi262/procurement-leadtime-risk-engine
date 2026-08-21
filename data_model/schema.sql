-- ============================================================================
-- GLOBAL PROCUREMENT & PREDICTIVE LEAD-TIME RISK PLATFORM
-- High-Throughput Procurement Analytics Schema (DuckDB / PostgreSQL)
-- ============================================================================

-- 1. VENDOR / SUPPLIER MASTER
CREATE TABLE IF NOT EXISTS dim_supplier_procurement (
    supplier_id VARCHAR(20) PRIMARY KEY,
    supplier_name VARCHAR(120) NOT NULL,
    tier_level VARCHAR(20) NOT NULL,          -- Strategic, Preferred, Approved, High-Risk
    commodity_category VARCHAR(80) NOT NULL,  -- Copper, Silicon Steel, Semiconductors, Polymers, Fasteners
    headquarters_country VARCHAR(50) NOT NULL,
    contract_incoterms VARCHAR(10) NOT NULL,  -- FOB, DDP, CIF, EXW
    payment_terms_days INT DEFAULT 60,
    credit_rating VARCHAR(5) DEFAULT 'A',
    is_single_source BOOLEAN DEFAULT FALSE
);

-- 2. COMMODITY / MATERIAL MASTER
CREATE TABLE IF NOT EXISTS dim_commodity_part (
    part_number VARCHAR(30) PRIMARY KEY,
    part_description VARCHAR(150) NOT NULL,
    commodity_group VARCHAR(80) NOT NULL,
    standard_cost_usd NUMERIC(12,2) NOT NULL,
    unit_of_measure VARCHAR(20) NOT NULL,
    criticality_tier VARCHAR(10) NOT NULL     -- Class 1 (Line-Stoppage Risk), Class 2 (Standard), Class 3 (Commodity)
);

-- 3. PURCHASE ORDER HEADER & LINE ITEM FACT
CREATE TABLE IF NOT EXISTS fact_purchase_orders (
    po_number VARCHAR(30) PRIMARY KEY,
    po_line_item INT NOT NULL,
    supplier_id VARCHAR(20) REFERENCES dim_supplier_procurement(supplier_id),
    part_number VARCHAR(30) REFERENCES dim_commodity_part(part_number),
    destination_plant_id VARCHAR(10) NOT NULL,
    
    -- Date Timestamps
    po_creation_date DATE NOT NULL,
    promised_delivery_date DATE NOT NULL,
    actual_receipt_date DATE,
    contracted_lead_time_days INT NOT NULL,
    actual_lead_time_days INT,
    
    -- Quantity & Financials
    ordered_quantity NUMERIC(12,2) NOT NULL,
    received_quantity NUMERIC(12,2) NOT NULL,
    po_unit_price_usd NUMERIC(12,2) NOT NULL,
    standard_unit_cost_usd NUMERIC(12,2) NOT NULL,
    total_spend_usd NUMERIC(15,2) NOT NULL,
    purchase_price_variance_usd NUMERIC(15,2) NOT NULL, -- (Unit_Price - Std_Cost) * Received_Qty
    
    -- Logistics & Transit Parameters
    freight_mode VARCHAR(20) NOT NULL,        -- Ocean, Air Express, Road Freight, Rail
    origin_country VARCHAR(50) NOT NULL,
    transit_lane VARCHAR(100) NOT NULL,
    port_congestion_index NUMERIC(4,2) DEFAULT 1.0, -- Multiplier 1.0 to 2.5
    
    -- Performance & ML Target Indicators
    is_on_time BOOLEAN NOT NULL,
    is_in_full BOOLEAN NOT NULL,
    is_otif BOOLEAN NOT NULL,                 -- On-Time AND In-Full
    is_delayed BOOLEAN NOT NULL,              -- Target Variable for ML
    days_delayed INT DEFAULT 0,
    predicted_delay_probability NUMERIC(5,4),
    anomaly_flag BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_po_supplier ON fact_purchase_orders(supplier_id);
CREATE INDEX idx_po_date ON fact_purchase_orders(po_creation_date);
CREATE INDEX idx_po_otif ON fact_purchase_orders(is_otif);
CREATE INDEX idx_po_ppv ON fact_purchase_orders(purchase_price_variance_usd);
