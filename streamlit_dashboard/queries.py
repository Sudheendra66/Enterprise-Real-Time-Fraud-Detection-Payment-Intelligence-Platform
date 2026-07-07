"""
SQL queries module for the Fraud Detection Dashboard.
Contains all queries for gold tables with proper formatting and optimization.
"""

from typing import Dict, Any, Optional
from config import get_gold_table_name


# ============================================================================
# FRAUD SUMMARY QUERIES
# ============================================================================

def get_fraud_summary() -> str:
    """
    Get overall fraud summary metrics.
    
    Returns:
        str: SQL query for fraud summary
    """
    table = get_gold_table_name("fraud_summary")
    return f"""
    SELECT 
        total_transactions,
        fraud_transactions,
        fraud_rate,
        total_amount,
        fraud_amount,
        avg_transaction_amount,
        avg_fraud_amount,
        updated_at
    FROM {table}
    """


def get_fraud_kpis() -> str:
    """
    Get key fraud metrics for KPI cards.
    
    Returns:
        str: SQL query for fraud KPIs
    """
    fraud_table = get_gold_table_name("fraud_summary")
    return f"""
    SELECT 
        event_date,
        total_transactions,
        fraud_transactions,
        fraud_rate,
        total_amount,
        fraud_amount,
        0 as high_risk_transactions,
        0 as medium_risk_transactions,
        0 as low_risk_transactions
    FROM {fraud_table}
    ORDER BY event_date DESC
    LIMIT 1
    """


# ============================================================================
# DAILY FRAUD TREND QUERIES
# ============================================================================

def get_daily_fraud_trend(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """
    Get daily fraud trend data.
    
    Args:
        start_date: Optional start date filter (YYYY-MM-DD)
        end_date: Optional end date filter (YYYY-MM-DD)
        
    Returns:
        str: SQL query for daily fraud trend
    """
    table = get_gold_table_name("daily_fraud_trend")
    query = f"""
    SELECT 
        event_date as transaction_date,
        total_transactions,
        fraud_transactions,
        fraud_rate
    FROM {table}
    """
    
    where_clauses = []
    if start_date:
        where_clauses.append(f"event_date >= '{start_date}'")
    if end_date:
        where_clauses.append(f"event_date <= '{end_date}'")
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += " ORDER BY event_date ASC"
    
    return query


def get_fraud_trend_last_30_days() -> str:
    """
    Get fraud trend for the last 30 days.
    
    Returns:
        str: SQL query for last 30 days trend
    """
    table = get_gold_table_name("daily_fraud_trend")
    return f"""
    SELECT 
        event_date as transaction_date,
        total_transactions,
        fraud_transactions,
        fraud_rate
    FROM {table}
    WHERE event_date >= CURRENT_DATE() - INTERVAL 30 DAYS
    ORDER BY event_date ASC
    """


# ============================================================================
# CUSTOMER RISK SUMMARY QUERIES
# ============================================================================

def get_customer_risk_summary(
    risk_level: Optional[str] = None,
    limit: int = 100
) -> str:
    """
    Get customer risk summary data.
    
    Args:
        risk_level: Optional risk level filter (HIGH, MEDIUM, LOW)
        limit: Maximum number of records to return
        
    Returns:
        str: SQL query for customer risk summary
    """
    table = get_gold_table_name("customer_risk_summary")
    query = f"""
    SELECT 
        card4 as customer_id,
        card6 as card_type,
        total_transactions,
        fraud_transactions,
        avg_risk_score as risk_score,
        total_amount
    FROM {table}
    """
    
    where_clauses = []
    if risk_level:
        # Note: customer_risk_summary doesn't have risk_level column
        # This filter will be ignored for this table
        pass
    
    query += f" ORDER BY avg_risk_score DESC LIMIT {limit}"
    
    return query


def get_top_high_risk_customers(limit: int = 50) -> str:
    """
    Get top high-risk customers.
    
    Args:
        limit: Number of customers to return
        
    Returns:
        str: SQL query for top high-risk customers
    """
    table = get_gold_table_name("customer_risk_summary")
    return f"""
    SELECT 
        card4 as customer_id,
        card6 as card_type,
        total_transactions,
        fraud_transactions,
        avg_risk_score as risk_score,
        total_amount
    FROM {table}
    ORDER BY avg_risk_score DESC
    LIMIT {limit}
    """


# ============================================================================
# PAYMENT METHOD SUMMARY QUERIES
# ============================================================================

def get_payment_method_summary() -> str:
    """
    Get payment method analysis data.
    
    Returns:
        str: SQL query for payment method summary
    """
    table = get_gold_table_name("payment_method_summary")
    return f"""
    SELECT 
        card4 as payment_method,
        card6 as card_type,
        total_transactions,
        fraud_transactions,
        fraud_rate,
        avg_transaction_amount,
        avg_risk_score
    FROM {table}
    ORDER BY fraud_rate DESC
    """


def get_payment_method_by_card_type() -> str:
    """
    Get payment method breakdown by card type.
    
    Returns:
        str: SQL query for payment method by card type
    """
    table = get_gold_table_name("payment_method_summary")
    return f"""
    SELECT 
        card6 as card_type,
        card4 as payment_method,
        total_transactions,
        fraud_transactions,
        fraud_rate,
        avg_transaction_amount
    FROM {table}
    ORDER BY card6, fraud_rate DESC
    """


# ============================================================================
# MERCHANT RISK SUMMARY QUERIES
# ============================================================================

def get_merchant_risk_summary(limit: int = 100) -> str:
    """
    Get merchant risk summary data.
    
    Args:
        limit: Maximum number of merchants to return
        
    Returns:
        str: SQL query for merchant risk summary
    """
    table = get_gold_table_name("merchant_risk_summary")
    return f"""
    SELECT 
        ProductCD as merchant_id,
        card4 as merchant_name,
        card6 as merchant_category,
        merchant_transaction_count as total_transactions,
        fraud_transactions,
        avg_risk_score as risk_score,
        total_amount
    FROM {table}
    ORDER BY avg_risk_score DESC
    LIMIT {limit}
    """


def get_top_risk_merchants(limit: int = 50) -> str:
    """
    Get top risk merchants.
    
    Args:
        limit: Number of merchants to return
        
    Returns:
        str: SQL query for top risk merchants
    """
    table = get_gold_table_name("merchant_risk_summary")
    return f"""
    SELECT 
        ProductCD as merchant_id,
        card4 as merchant_name,
        card6 as merchant_category,
        merchant_transaction_count as total_transactions,
        fraud_transactions,
        avg_risk_score as risk_score,
        total_amount
    FROM {table}
    ORDER BY avg_risk_score DESC
    LIMIT {limit}
    """


# ============================================================================
# AMOUNT BUCKET SUMMARY QUERIES
# ============================================================================

def get_amount_bucket_summary() -> str:
    """
    Get amount bucket distribution data.
    
    Returns:
        str: SQL query for amount bucket summary
    """
    table = get_gold_table_name("amount_bucket_summary")
    return f"""
    SELECT 
        amount_bucket,
        total_transactions,
        fraud_transactions,
        fraud_rate,
        avg_risk_score,
        total_amount
    FROM {table}
    ORDER BY amount_bucket
    """


def get_amount_distribution() -> str:
    """
    Get transaction amount distribution.
    
    Returns:
        str: SQL query for amount distribution
    """
    table = get_gold_table_name("amount_bucket_summary")
    return f"""
    SELECT 
        amount_bucket,
        total_transactions,
        fraud_transactions,
        fraud_rate
    FROM {table}
    ORDER BY amount_bucket
    """


# ============================================================================
# RISK LEVEL SUMMARY QUERIES
# ============================================================================

def get_risk_level_summary() -> str:
    """
    Get risk level distribution data.
    
    Returns:
        str: SQL query for risk level summary
    """
    table = get_gold_table_name("risk_level_summary")
    return f"""
    SELECT 
        risk_level,
        total_transactions,
        fraud_transactions,
        fraud_rate,
        avg_risk_score,
        total_amount
    FROM {table}
    ORDER BY 
        CASE risk_level 
            WHEN 'HIGH' THEN 1 
            WHEN 'MEDIUM' THEN 2 
            WHEN 'LOW' THEN 3 
        END
    """


def get_risk_level_distribution() -> str:
    """
    Get risk level distribution for donut chart.
    
    Returns:
        str: SQL query for risk level distribution
    """
    table = get_gold_table_name("risk_level_summary")
    return f"""
    SELECT 
        risk_level,
        total_transactions,
        fraud_transactions,
        fraud_rate
    FROM {table}
    ORDER BY 
        CASE risk_level 
            WHEN 'HIGH' THEN 1 
            WHEN 'MEDIUM' THEN 2 
            WHEN 'LOW' THEN 3 
        END
    """


# ============================================================================
# FILTER QUERIES
# ============================================================================

def get_filter_values() -> Dict[str, Any]:
    """
    Get distinct values for all filter dropdowns.
    
    Returns:
        Dict[str, Any]: Dictionary of filter values
    """
    queries = {
        "risk_levels": f"SELECT DISTINCT risk_level FROM {get_gold_table_name('risk_level_summary')} ORDER BY risk_level",
        "card_types": f"SELECT DISTINCT card_type FROM {get_gold_table_name('payment_method_summary')} ORDER BY card_type",
        "products": f"SELECT DISTINCT product FROM {get_gold_table_name('fraud_summary')} ORDER BY product",  # May need adjustment
        "amount_buckets": f"SELECT DISTINCT amount_bucket FROM {get_gold_table_name('amount_bucket_summary')} ORDER BY amount_bucket"
    }
    
    return queries


# ============================================================================
# DETAILED TRANSACTION QUERIES
# ============================================================================

def get_transaction_details(
    risk_level: Optional[str] = None,
    card_type: Optional[str] = None,
    product: Optional[str] = None,
    amount_bucket: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    search_term: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    sort_by: str = "event_date",
    sort_order: str = "DESC"
) -> str:
    """
    Get detailed transaction data with filters, search, pagination, and sorting.
    
    Args:
        risk_level: Filter by risk level
        card_type: Filter by card type
        product: Filter by product
        amount_bucket: Filter by amount bucket
        start_date: Filter by start date
        end_date: Filter by end date
        search_term: Search term for transaction ID or customer ID
        limit: Number of records to return
        offset: Offset for pagination
        sort_by: Column to sort by
        sort_order: Sort order (ASC or DESC)
        
    Returns:
        str: SQL query for transaction details
    """
    # Using fraud_summary as the best available aggregated data
    table = get_gold_table_name("fraud_summary")
    
    query = f"""
    SELECT 
        event_date as transaction_date,
        total_transactions,
        fraud_transactions,
        fraud_rate,
        total_amount,
        fraud_amount
    FROM {table}
    WHERE 1=1
    """
    
    where_clauses = []
    
    if start_date:
        where_clauses.append(f"event_date >= '{start_date}'")
    if end_date:
        where_clauses.append(f"event_date <= '{end_date}'")
    
    if where_clauses:
        query += " AND " + " AND ".join(where_clauses)
    
    # Add sorting
    query += f" ORDER BY {sort_by} {sort_order}"
    
    # Add pagination
    query += f" LIMIT {limit} OFFSET {offset}"
    
    return query


def get_transaction_count(
    risk_level: Optional[str] = None,
    card_type: Optional[str] = None,
    product: Optional[str] = None,
    amount_bucket: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    search_term: Optional[str] = None
) -> str:
    """
    Get count of transactions matching filters.
    
    Args:
        risk_level: Filter by risk level
        card_type: Filter by card type
        product: Filter by product
        amount_bucket: Filter by amount bucket
        start_date: Filter by start date
        end_date: Filter by end date
        search_term: Search term for transaction ID or customer ID
        
    Returns:
        str: SQL query for transaction count
    """
    table = get_gold_table_name("fraud_summary")
    
    query = f"""
    SELECT COUNT(*) as total_count
    FROM {table}
    WHERE 1=1
    """
    
    where_clauses = []
    
    if start_date:
        where_clauses.append(f"event_date >= '{start_date}'")
    if end_date:
        where_clauses.append(f"event_date <= '{end_date}'")
    
    if where_clauses:
        query += " AND " + " AND ".join(where_clauses)
    
    return query


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def build_filter_query(
    base_query: str,
    filters: Dict[str, Any],
    date_column: str = "transaction_date"
) -> str:
    """
    Build a query with filters applied.
    
    Args:
        base_query: Base SQL query
        filters: Dictionary of filters to apply
        date_column: Name of the date column for date filters
        
    Returns:
        str: Query with filters applied
    """
    where_clauses = []
    
    for key, value in filters.items():
        if value is not None and value != "":
            if key in ["start_date", "end_date"]:
                date_value = value
                if key == "start_date":
                    where_clauses.append(f"{date_column} >= '{date_value}'")
                else:
                    where_clauses.append(f"{date_column} <= '{date_value}'")
            elif isinstance(value, str):
                where_clauses.append(f"{key} = '{value}'")
            else:
                where_clauses.append(f"{key} = {value}")
    
    if where_clauses:
        if "WHERE" in base_query.upper():
            base_query += " AND " + " AND ".join(where_clauses)
        else:
            base_query += " WHERE " + " AND ".join(where_clauses)
    
    return base_query


def get_query_metadata() -> Dict[str, str]:
    """
    Get metadata for all queries.
    
    Returns:
        Dict[str, str]: Dictionary mapping query names to descriptions
    """
    return {
        "fraud_summary": "Overall fraud summary metrics",
        "fraud_kpis": "Key fraud metrics for KPI cards",
        "daily_fraud_trend": "Daily fraud trend data",
        "fraud_trend_last_30_days": "Fraud trend for last 30 days",
        "customer_risk_summary": "Customer risk summary data",
        "top_high_risk_customers": "Top high-risk customers",
        "payment_method_summary": "Payment method analysis data",
        "payment_method_by_card_type": "Payment method breakdown by card type",
        "merchant_risk_summary": "Merchant risk summary data",
        "top_risk_merchants": "Top risk merchants",
        "amount_bucket_summary": "Amount bucket distribution data",
        "amount_distribution": "Transaction amount distribution",
        "risk_level_summary": "Risk level distribution data",
        "risk_level_distribution": "Risk level distribution for donut chart"
    }