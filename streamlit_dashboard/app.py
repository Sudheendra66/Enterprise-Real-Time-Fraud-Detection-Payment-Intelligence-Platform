"""
Enterprise Fraud Detection Platform - Streamlit Dashboard
Real-time fraud analytics and payment intelligence dashboard.
"""

from pathlib import Path

import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from typing import Optional, Dict, Any

# Import custom modules
from config import databricks_config, dashboard_config, missing_config_keys, validate_config
from databricks_client import get_databricks_client, execute_query
from queries import (
    get_fraud_kpis,
    get_risk_level_distribution,
    get_fraud_trend_last_30_days,
    get_payment_method_summary,
    get_amount_bucket_summary,
    get_customer_risk_summary,
    get_transaction_details,
    get_transaction_count,
    get_filter_values
)
from kpis import KPI, KPICalculator, render_kpi_cards
from charts import (
    create_risk_level_donut,
    create_fraud_trend_line,
    create_payment_method_stacked_bar,
    create_amount_bucket_pie,
    create_customer_risk_bar,
    create_empty_chart
)
from utils import (
    initialize_session_state,
    reset_filters,
    paginate_dataframe,
    search_dataframe,
    apply_filters,
    generate_csv_download,
    format_currency,
    format_number,
    format_percentage
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=dashboard_config.page_title,
        page_icon=dashboard_config.page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )


# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

def load_custom_css():
    """Load custom CSS for dark theme and professional styling."""
    st.markdown("""
    <style>
    :root {
        --fraud-bg: #0B1120;
        --fraud-panel: #111827;
        --fraud-card: #162033;
        --fraud-border: #26364F;
        --fraud-text: #E5E7EB;
        --fraud-muted: #94A3B8;
        --fraud-cyan: #00E5FF;
        --fraud-green: #22C55E;
        --fraud-red: #EF4444;
        --fraud-amber: #F59E0B;
    }

    .stApp {
        background: radial-gradient(circle at top left, rgba(0, 229, 255, 0.08), transparent 28%),
                    linear-gradient(180deg, #0B1120 0%, #111827 100%);
        color: var(--fraud-text);
    }

    section[data-testid="stSidebar"] {
        background: #0F172A;
        border-right: 1px solid var(--fraud-border);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {
        color: var(--fraud-text) !important;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .main-header {
        padding: 22px 26px;
        margin-bottom: 22px;
        border: 1px solid var(--fraud-border);
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(22, 32, 51, 0.96), rgba(15, 23, 42, 0.96));
        box-shadow: 0 18px 50px rgba(0, 0, 0, 0.24);
    }

    .main-header h1 {
        color: #F8FAFC;
        font-size: 2rem;
        line-height: 1.15;
        margin: 0 0 0.4rem 0;
        letter-spacing: 0;
    }

    .subtitle {
        color: var(--fraud-muted);
        margin: 0;
        font-size: 1rem;
    }

    .refresh-info {
        color: var(--fraud-cyan);
        margin: 0.85rem 0 0 0;
        font-size: 0.85rem;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #162033 0%, #0F172A 100%);
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #00E5FF;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        min-height: 132px;
    }
    
    div[data-testid="stMetricValue"] {
        color: #00E5FF !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #F1F5F9 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
    }

    .chart-container,
    .data-table {
        background: rgba(17, 24, 39, 0.76);
        border: 1px solid var(--fraud-border);
        border-radius: 8px;
        padding: 16px 18px 10px 18px;
        margin-bottom: 8px;
    }

    .status-strip {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin: 0 0 18px 0;
    }

    .status-pill {
        border: 1px solid var(--fraud-border);
        border-radius: 999px;
        padding: 7px 12px;
        color: var(--fraud-muted);
        background: rgba(15, 23, 42, 0.82);
        font-size: 0.82rem;
        font-weight: 600;
    }

    .section-note {
        color: var(--fraud-muted);
        font-size: 0.9rem;
        margin: -0.45rem 0 1rem 0;
    }
    
    /* Hide Streamlit branding while keeping the header/sidebar toggle available. */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# HEADER COMPONENT
# ============================================================================

def render_header():
    """Render the dashboard header."""
    # Get last refresh time
    last_refresh = st.session_state.get('last_refresh')
    refresh_text = f"Last refreshed: {last_refresh.strftime('%Y-%m-%d %H:%M:%S')}" if last_refresh else "Loading data..."
    
    st.markdown(f"""
    <div class="main-header">
        <h1>Enterprise Fraud Detection Platform</h1>
        <p class="subtitle">Real-Time Fraud Analytics & Payment Intelligence Dashboard</p>
        <p class="refresh-info">ðŸ• {refresh_text}</p>
    </div>
    """, unsafe_allow_html=True)


def render_status_strip(filters: Dict[str, Any]) -> None:
    """Render compact context badges for the active dashboard state."""
    active_filters = sum(1 for value in filters.values() if value)
    cache_minutes = int(dashboard_config.cache_ttl / 60)
    st.markdown(f"""
    <div class="status-strip">
        <span class="status-pill">Active filters: {active_filters}</span>
        <span class="status-pill">Cache TTL: {cache_minutes} min</span>
        <span class="status-pill">Catalog: {databricks_config.catalog}</span>
        <span class="status-pill">Schema: {databricks_config.schema}</span>
    </div>
    """, unsafe_allow_html=True)


def render_configuration_error() -> None:
    """Show a friendly blocking message when required Databricks settings are missing."""
    missing_keys = missing_config_keys()
    st.error(
        "Configuration incomplete. Add the missing Databricks settings in "
        "Streamlit Community Cloud secrets or local environment variables, "
        "then refresh the dashboard."
    )
    st.code("\n".join(missing_keys), language="text")

    with st.expander("Configuration diagnostics", expanded=False):
        st.write(f"Working directory: `{Path.cwd()}`")
        st.write(f"App directory: `{Path(__file__).parent}`")
        st.write(f"Project .env found: `{(Path(__file__).parent.parent / '.env').exists()}`")
        st.write(f"Missing keys: `{', '.join(missing_keys)}`")


# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

def render_sidebar_filters() -> Dict[str, Any]:
    """
    Render sidebar filters and return selected filter values.
    
    Returns:
        Dict[str, Any]: Dictionary of selected filter values
    """
    with st.sidebar:
        st.title("Filters")
        st.write("---")
        
        filters = {}
        
        # Risk Level Filter
        st.markdown("### Risk Level")
        risk_levels = ["All", "HIGH", "MEDIUM", "LOW"]
        selected_risk = st.selectbox(
            "Select Risk Level",
            options=risk_levels,
            index=0,
            key="risk_level_filter"
        )
        filters['risk_level'] = None if selected_risk == "All" else selected_risk
        
        # Card Type Filter
        st.markdown("### Card Type")
        try:
            card_types_df = execute_query(
                "SELECT DISTINCT card6 as card_type FROM fraud_platform.gold.payment_method_summary ORDER BY card_type",
                use_cache=True,
                ttl=600
            )
            card_types = ["All"] + card_types_df['card_type'].tolist() if not card_types_df.empty else ["All"]
        except Exception as e:
            st.warning(f"Could not load card types: {str(e)}")
            card_types = ["All"]
        
        selected_card = st.selectbox(
            "Select Card Type",
            options=card_types,
            index=0,
            key="card_type_filter"
        )
        filters['card_type'] = None if selected_card == "All" else selected_card
        
        # Amount Bucket Filter
        st.markdown("### Amount Bucket")
        try:
            amount_buckets_df = execute_query(
                "SELECT DISTINCT amount_bucket FROM fraud_platform.gold.amount_bucket_summary ORDER BY amount_bucket",
                use_cache=True,
                ttl=600
            )
            amount_buckets = ["All"] + amount_buckets_df['amount_bucket'].tolist() if not amount_buckets_df.empty else ["All"]
        except:
            amount_buckets = ["All"]
        
        selected_bucket = st.selectbox(
            "Select Amount Bucket",
            options=amount_buckets,
            index=0,
            key="amount_bucket_filter"
        )
        filters['amount_bucket'] = None if selected_bucket == "All" else selected_bucket
        
        # Date Range Filter
        st.markdown("### Date Range")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=None,
                key="start_date_filter"
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=None,
                key="end_date_filter"
            )
        
        filters['start_date'] = start_date.strftime("%Y-%m-%d") if start_date else None
        filters['end_date'] = end_date.strftime("%Y-%m-%d") if end_date else None
        
        # Action Buttons
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("ðŸ”„ Refresh", use_container_width=True):
                st.cache_data.clear()
                st.session_state.last_refresh = datetime.now()
                st.rerun()
        
        with col2:
            if st.button("ðŸ”„ Reset", use_container_width=True):
                reset_filters()
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Connection Status
        st.markdown("---")
        st.markdown("### Connection Status")
        try:
            client = get_databricks_client()
            if client.test_connection():
                st.success("âœ… Databricks Connected")
            else:
                st.error("âŒ Connection Failed")
        except Exception as e:
            st.error(f"âŒ Error: {str(e)}")
    
    return filters


def render_sidebar_controls() -> Dict[str, Any]:
    """Render resilient sidebar controls that stay visible in all app states."""
    with st.sidebar:
        st.title("Fraud Controls")
        st.caption("Filters, refresh, and connection health")
        st.write("---")

        filters = {}
        config_ready = validate_config()

        st.markdown("### Risk Level")
        selected_risk = st.selectbox(
            "Select Risk Level",
            options=["All", "HIGH", "MEDIUM", "LOW"],
            index=0,
            key="risk_level_filter"
        )
        filters["risk_level"] = None if selected_risk == "All" else selected_risk

        st.markdown("### Card Type")
        card_types = ["All"]
        if config_ready:
            try:
                card_types_df = execute_query(
                    "SELECT DISTINCT card6 as card_type FROM fraud_platform.gold.payment_method_summary WHERE card6 IS NOT NULL ORDER BY card_type",
                    use_cache=True,
                    ttl=600
                )
                if not card_types_df.empty:
                    card_types += card_types_df["card_type"].dropna().astype(str).tolist()
            except Exception as e:
                st.warning(f"Could not load card types: {str(e)}")

        selected_card = st.selectbox(
            "Select Card Type",
            options=card_types,
            index=0,
            key="card_type_filter"
        )
        filters["card_type"] = None if selected_card == "All" else selected_card

        st.markdown("### Amount Bucket")
        amount_buckets = ["All"]
        if config_ready:
            try:
                amount_buckets_df = execute_query(
                    "SELECT DISTINCT amount_bucket FROM fraud_platform.gold.amount_bucket_summary WHERE amount_bucket IS NOT NULL ORDER BY amount_bucket",
                    use_cache=True,
                    ttl=600
                )
                if not amount_buckets_df.empty:
                    amount_buckets += amount_buckets_df["amount_bucket"].dropna().astype(str).tolist()
            except Exception as e:
                st.warning(f"Could not load amount buckets: {str(e)}")

        selected_bucket = st.selectbox(
            "Select Amount Bucket",
            options=amount_buckets,
            index=0,
            key="amount_bucket_filter"
        )
        filters["amount_bucket"] = None if selected_bucket == "All" else selected_bucket

        st.markdown("### Date Range")
        date_preset = st.selectbox(
            "Preset",
            options=["All time", "Last 7 days", "Last 30 days", "Last 90 days", "Custom"],
            index=0,
            key="date_preset_filter"
        )

        start_date = None
        end_date = None
        today = date.today()
        if date_preset == "Last 7 days":
            start_date = today - timedelta(days=7)
            end_date = today
        elif date_preset == "Last 30 days":
            start_date = today - timedelta(days=30)
            end_date = today
        elif date_preset == "Last 90 days":
            start_date = today - timedelta(days=90)
            end_date = today
        elif date_preset == "Custom":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", value=None, key="start_date_filter")
            with col2:
                end_date = st.date_input("End Date", value=None, key="end_date_filter")

        filters["start_date"] = start_date.strftime("%Y-%m-%d") if start_date else None
        filters["end_date"] = end_date.strftime("%Y-%m-%d") if end_date else None

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Refresh", use_container_width=True):
                st.cache_data.clear()
                st.session_state.last_refresh = datetime.now()
                st.rerun()
        with col2:
            if st.button("Reset", use_container_width=True, on_click=reset_filters):
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Connection Status")
        if not config_ready:
            st.warning("Databricks config missing")
        else:
            try:
                client = get_databricks_client()
                if client.test_connection():
                    st.success("Databricks connected")
                else:
                    st.error("Connection failed")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

    return filters


# ============================================================================
# KPI ROW
# ============================================================================

def get_numeric_value(df: pd.DataFrame, column: str, default: float = 0.0) -> float:
    """Safely read a numeric value from the first row of a dataframe."""
    if df.empty or column not in df.columns:
        return default

    value = pd.to_numeric(pd.Series([df[column].iloc[0]]), errors="coerce").iloc[0]
    return default if pd.isna(value) else float(value)


def render_kpi_row(filters: Dict[str, Any]):
    """Render the KPI cards row."""
    st.markdown("## Key Performance Indicators")
    st.markdown('<p class="section-note">Latest fraud posture from the gold summary table.</p>', unsafe_allow_html=True)
    
    try:
        # Fetch KPI data
        kpi_query = get_fraud_kpis()
        kpi_df = execute_query(kpi_query, use_cache=True, ttl=300)
        
        if not kpi_df.empty:
            total_transactions = get_numeric_value(kpi_df, "total_transactions")
            total_amount = get_numeric_value(kpi_df, "total_amount")
            fraud_amount = get_numeric_value(kpi_df, "fraud_amount")
            # Get only main KPIs (skip risk level KPIs that are 0)
            kpis = {
                "total_transactions": KPICalculator.create_total_transactions_kpi(kpi_df),
                "fraud_transactions": KPICalculator.create_fraud_transactions_kpi(kpi_df),
                "fraud_rate": KPICalculator.create_fraud_rate_kpi(kpi_df),
                "total_amount": KPI(
                    title="Total Amount",
                    value=KPICalculator.format_number(total_amount, "currency"),
                    subtitle="Processed volume",
                    icon="$",
                    color="#22C55E",
                    format_type="currency"
                ),
                "fraud_amount": KPI(
                    title="Fraud Amount",
                    value=KPICalculator.format_number(fraud_amount, "currency"),
                    subtitle="Flagged value",
                    icon="!",
                    color="#EF4444",
                    format_type="currency"
                )
            }
            
            render_kpi_cards(kpis, num_columns=5)
        else:
            st.warning("No KPI data available")
    
    except Exception as e:
        st.error(f"Error loading KPIs: {str(e)}")


def render_risk_snapshot(filters: Dict[str, Any]):
    """Render compact risk-level cards using the existing risk distribution query."""
    st.markdown("## Risk Snapshot")
    st.markdown('<p class="section-note">Quick breakdown by risk band, transaction count, and fraud rate.</p>', unsafe_allow_html=True)

    try:
        risk_df = execute_query(get_risk_level_distribution(), use_cache=True, ttl=300)

        if risk_df.empty:
            st.info("No risk snapshot data available")
            return

        risk_order = ["HIGH", "MEDIUM", "LOW"]
        cols = st.columns(3)
        for idx, risk_level in enumerate(risk_order):
            row = risk_df[risk_df["risk_level"].astype(str).str.upper() == risk_level]
            total = get_numeric_value(row, "total_transactions")
            fraud = get_numeric_value(row, "fraud_transactions")
            fraud_rate = get_numeric_value(row, "fraud_rate")

            with cols[idx]:
                st.metric(
                    label=f"{risk_level} Risk",
                    value=format_number(total),
                    delta=f"{format_number(fraud)} fraud | {fraud_rate:.2f}% rate"
                )

    except Exception as e:
        st.error(f"Error loading risk snapshot: {str(e)}")


# ============================================================================
# CHARTS ROW 2
# ============================================================================

def render_charts_row_2(filters: Dict[str, Any]):
    """Render Row 2: Risk Level Distribution and Fraud Trend."""
    col1, col2 = st.columns(2)
    
    # Risk Level Distribution - Donut Chart
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### Risk Level Distribution")
        
        try:
            risk_query = get_risk_level_distribution()
            risk_df = execute_query(risk_query, use_cache=True, ttl=300)
            
            if not risk_df.empty:
                fig = create_risk_level_donut(risk_df)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.plotly_chart(create_empty_chart("No risk level data available"), use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading risk level data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fraud Trend - Line Chart
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### Fraud Trend Analysis")
        
        try:
            trend_query = get_fraud_trend_last_30_days()
            trend_df = execute_query(trend_query, use_cache=True, ttl=300)
            
            if not trend_df.empty:
                fig = create_fraud_trend_line(trend_df)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.plotly_chart(create_empty_chart("No trend data available"), use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading trend data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================================
# CHARTS ROW 3
# ============================================================================

def render_charts_row_3(filters: Dict[str, Any]):
    """Render Row 3: Payment Method Analysis."""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### Payment Method Analysis")

    try:
        payment_query = get_payment_method_summary()
        payment_df = execute_query(payment_query, use_cache=True, ttl=300)

        if not payment_df.empty:
            fig = create_payment_method_stacked_bar(payment_df)
            fig.update_layout(height=430)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(create_empty_chart("No payment method data available"), use_container_width=True)

    except Exception as e:
        st.error(f"Error loading payment method data: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================================
# CHARTS ROW 4
# ============================================================================

def render_charts_row_4(filters: Dict[str, Any]):
    """Render Row 4: Amount Bucket and Customer Risk Analysis."""
    col1, col2 = st.columns(2)
    
    # Amount Bucket Distribution - Pie Chart
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### Amount Bucket Distribution")
        
        try:
            amount_query = get_amount_bucket_summary()
            amount_df = execute_query(amount_query, use_cache=True, ttl=300)
            
            if not amount_df.empty:
                fig = create_amount_bucket_pie(amount_df)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.plotly_chart(create_empty_chart("No amount bucket data available"), use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading amount bucket data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Customer Risk Analysis - Bar Chart
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### Customer Risk Analysis")
        
        try:
            customer_query = get_customer_risk_summary(limit=100)
            customer_df = execute_query(customer_query, use_cache=True, ttl=300)
            
            if not customer_df.empty:
                fig = create_customer_risk_bar(customer_df, top_n=20)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.plotly_chart(create_empty_chart("No customer data available"), use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading customer data: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================================
# INTERACTIVE DATA TABLE
# ============================================================================

def render_data_table(filters: Dict[str, Any]):
    """Render the interactive data table with search, pagination, and download."""
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.markdown("## Transaction Details")
    
    try:
        # Search input
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            search_term = st.text_input(
                "ðŸ” Search Transactions",
                value=st.session_state.get('search_term', ''),
                placeholder="Search by Transaction ID or Customer ID...",
                key="search_input"
            )
            st.session_state.search_term = search_term
        
        with col2:
            page_size = st.selectbox(
                "Rows per page",
                options=[10, 25, 50, 100],
                index=1,
                key="page_size_select"
            )
            st.session_state.page_size = page_size
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ðŸ”„ Refresh Data", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        # Get total count
        count_query = get_transaction_count(
            risk_level=filters.get('risk_level'),
            card_type=filters.get('card_type'),
            amount_bucket=filters.get('amount_bucket'),
            start_date=filters.get('start_date'),
            end_date=filters.get('end_date'),
            search_term=search_term if search_term else None
        )
        
        count_df = execute_query(count_query, use_cache=False)
        total_rows = count_df['total_count'].iloc[0] if not count_df.empty else 0
        
        if total_rows == 0:
            st.info("No transactions found matching the criteria")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # Pagination
        total_pages = (total_rows + page_size - 1) // page_size
        page_number = st.session_state.get('page_number', 1)
        
        if page_number > total_pages:
            page_number = total_pages
            st.session_state.page_number = page_number
        
        # Pagination controls
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("â¬…ï¸ Previous", disabled=(page_number <= 1), use_container_width=True):
                st.session_state.page_number = page_number - 1
                st.rerun()
        
        with col2:
            st.markdown(f"<p style='text-align: center; color: #94A3B8;'>Page {page_number} of {total_pages} | Total: {format_number(total_rows)} transactions</p>", unsafe_allow_html=True)
        
        with col3:
            if st.button("Next âž¡ï¸", disabled=(page_number >= total_pages), use_container_width=True):
                st.session_state.page_number = page_number + 1
                st.rerun()
        
        # Get transaction data
        offset = (page_number - 1) * page_size
        transaction_query = get_transaction_details(
            risk_level=filters.get('risk_level'),
            card_type=filters.get('card_type'),
            amount_bucket=filters.get('amount_bucket'),
            start_date=filters.get('start_date'),
            end_date=filters.get('end_date'),
            search_term=search_term if search_term else None,
            limit=page_size,
            offset=offset,
            sort_by=st.session_state.get('sort_by', 'transaction_date'),
            sort_order=st.session_state.get('sort_order', 'DESC')
        )
        
        transaction_df = execute_query(transaction_query, use_cache=False)
        
        if not transaction_df.empty:
            # Display data table
            st.dataframe(
                transaction_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "transaction_id": st.column_config.TextColumn("Transaction ID", width="medium"),
                    "customer_id": st.column_config.TextColumn("Customer ID", width="medium"),
                    "transaction_date": st.column_config.DateColumn("Date", width="small"),
                    "transaction_amount": st.column_config.NumberColumn("Amount", width="small", format="$%.2f"),
                    "risk_level": st.column_config.TextColumn("Risk Level", width="small"),
                    "fraud_flag": st.column_config.CheckboxColumn("Fraud", width="small"),
                    "payment_method": st.column_config.TextColumn("Payment Method", width="medium"),
                    "merchant_id": st.column_config.TextColumn("Merchant ID", width="medium")
                }
            )
            
            # Download button
            generate_csv_download(
                transaction_df,
                filename=f"transactions_page_{page_number}.csv"
            )
        else:
            st.info("No transaction details available")
    
    except Exception as e:
        st.error(f"Error loading transaction data: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    # Setup page configuration
    setup_page()
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Update last refresh time
    if st.session_state.get('last_refresh') is None:
        st.session_state.last_refresh = datetime.now()

    # Render the dashboard shell before any blocking validation.
    render_header()
    filters = render_sidebar_controls()
    render_status_strip(filters)

    if not validate_config():
        render_configuration_error()
        st.stop()
    
    
    # Render KPI Row
    render_kpi_row(filters)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Render Risk Snapshot
    render_risk_snapshot(filters)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Charts Row 2
    render_charts_row_2(filters)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Charts Row 3
    render_charts_row_3(filters)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Charts Row 4
    render_charts_row_4(filters)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render Interactive Data Table
    render_data_table(filters)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        text-align: center;
        color: #64748B;
        font-size: 12px;
        padding: 20px;
    ">
        <p>Enterprise Fraud Detection Platform | Real-Time Analytics Dashboard</p>
        <p>Powered by Databricks & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()



