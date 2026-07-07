"""
Utility functions module for the Fraud Detection Dashboard.
Contains helper functions for formatting, data processing, and common operations.
"""

from typing import Optional, List, Dict, Any, Tuple
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import re


# ============================================================================
# FORMATTING UTILITIES
# ============================================================================

def format_currency(value: float, currency_symbol: str = "$") -> str:
    """
    Format a number as currency.
    
    Args:
        value: Numeric value to format
        currency_symbol: Currency symbol to use
        
    Returns:
        str: Formatted currency string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    if value >= 1_000_000_000:
        return f"{currency_symbol}{value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{currency_symbol}{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{currency_symbol}{value/1_000:.2f}K"
    else:
        return f"{currency_symbol}{value:.2f}"


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    Format a number as percentage.
    
    Args:
        value: Numeric value to format
        decimal_places: Number of decimal places
        
    Returns:
        str: Formatted percentage string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    return f"{value:.{decimal_places}f}%"


def format_number(value: float, decimal_places: int = 0) -> str:
    """
    Format a number with thousand separators.
    
    Args:
        value: Numeric value to format
        decimal_places: Number of decimal places
        
    Returns:
        str: Formatted number string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    return f"{value:,.{decimal_places}f}"


def format_compact_number(value: float) -> str:
    """
    Format a number in compact form (K, M, B).
    
    Args:
        value: Numeric value to format
        
    Returns:
        str: Formatted compact number string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.2f}K"
    else:
        return f"{value:.0f}"


# ============================================================================
# DATE UTILITIES
# ============================================================================

def get_date_range_options() -> List[Tuple[str, str, str]]:
    """
    Get predefined date range options.
    
    Returns:
        List[Tuple[str, str, str]]: List of (label, start_date, end_date) tuples
    """
    today = datetime.now()
    
    options = [
        ("Last 7 Days", (today - timedelta(days=7)).strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")),
        ("Last 30 Days", (today - timedelta(days=30)).strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")),
        ("Last 90 Days", (today - timedelta(days=90)).strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")),
        ("Last 6 Months", (today - timedelta(days=180)).strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")),
        ("Last Year", (today - timedelta(days=365)).strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")),
        ("Year to Date", datetime(today.year, 1, 1).strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")),
    ]
    
    return options


def parse_date_range(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse and validate date range.
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        
    Returns:
        Tuple[Optional[str], Optional[str]]: Validated start and end dates
    """
    validated_start = None
    validated_end = None
    
    if start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            validated_start = start_date
        except ValueError:
            st.warning(f"Invalid start date format: {start_date}. Use YYYY-MM-DD")
    
    if end_date:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
            validated_end = end_date
        except ValueError:
            st.warning(f"Invalid end date format: {end_date}. Use YYYY-MM-DD")
    
    # Validate date range
    if validated_start and validated_end:
        if validated_start > validated_end:
            st.warning("Start date cannot be after end date")
            validated_start = None
            validated_end = None
    
    return validated_start, validated_end


# ============================================================================
# DATA UTILITIES
# ============================================================================

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize column names.
    
    Args:
        df: Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with cleaned column names
    """
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df


def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate that DataFrame has required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        bool: True if all required columns exist
    """
    if df.empty:
        return False
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return False
    
    return True


def safe_convert_to_numeric(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Safely convert columns to numeric type.
    
    Args:
        df: Input DataFrame
        columns: List of column names to convert
        
    Returns:
        pd.DataFrame: DataFrame with converted columns
    """
    df = df.copy()
    
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def calculate_percentage_of_total(df: pd.DataFrame, value_column: str) -> pd.DataFrame:
    """
    Calculate percentage of total for a column.
    
    Args:
        df: Input DataFrame
        value_column: Column name to calculate percentage for
        
    Returns:
        pd.DataFrame: DataFrame with added percentage column
    """
    df = df.copy()
    total = df[value_column].sum()
    
    if total > 0:
        df['percentage_of_total'] = (df[value_column] / total) * 100
    else:
        df['percentage_of_total'] = 0
    
    return df


# ============================================================================
# SEARCH AND FILTER UTILITIES
# ============================================================================

def search_dataframe(
    df: pd.DataFrame,
    search_term: str,
    search_columns: List[str]
) -> pd.DataFrame:
    """
    Search DataFrame for a term in specified columns.
    
    Args:
        df: Input DataFrame
        search_term: Search term
        search_columns: List of columns to search in
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    if not search_term or df.empty:
        return df
    
    search_term = search_term.lower()
    mask = df[search_columns].apply(
        lambda row: row.astype(str).str.lower().str.contains(search_term, na=False)
    ).any(axis=1)
    
    return df[mask]


def apply_filters(
    df: pd.DataFrame,
    filters: Dict[str, Any]
) -> pd.DataFrame:
    """
    Apply multiple filters to a DataFrame.
    
    Args:
        df: Input DataFrame
        filters: Dictionary of column:value filters
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    if df.empty or not filters:
        return df
    
    filtered_df = df.copy()
    
    for column, value in filters.items():
        if value and value != "" and column in filtered_df.columns:
            if isinstance(value, list):
                filtered_df = filtered_df[filtered_df[column].isin(value)]
            else:
                filtered_df = filtered_df[filtered_df[column] == value]
    
    return filtered_df


# ============================================================================
# PAGINATION UTILITIES
# ============================================================================

def paginate_dataframe(
    df: pd.DataFrame,
    page_size: int,
    page_number: int
) -> Tuple[pd.DataFrame, int, int]:
    """
    Paginate a DataFrame.
    
    Args:
        df: Input DataFrame
        page_size: Number of rows per page
        page_number: Current page number (1-indexed)
        
    Returns:
        Tuple[pd.DataFrame, int, int]: (page_data, total_pages, total_rows)
    """
    if df.empty:
        return df, 0, 0
    
    total_rows = len(df)
    total_pages = (total_rows + page_size - 1) // page_size
    
    # Validate page number
    if page_number < 1:
        page_number = 1
    elif page_number > total_pages:
        page_number = total_pages
    
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    
    page_data = df.iloc[start_idx:end_idx]
    
    return page_data, total_pages, total_rows


# ============================================================================
# DOWNLOAD UTILITIES
# ============================================================================

def generate_csv_download(
    df: pd.DataFrame,
    filename: str = "data.csv"
) -> None:
    """
    Generate and display a CSV download button.
    
    Args:
        df: DataFrame to download
        filename: Name of the download file
    """
    if df.empty:
        st.warning("No data available to download")
        return
    
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv",
        key=f"download_{filename}"
    )


# ============================================================================
# SESSION STATE UTILITIES
# ============================================================================

def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'risk_level': None,
            'card_type': None,
            'product': None,
            'amount_bucket': None,
            'start_date': None,
            'end_date': None
        }
    
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ""
    
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
    
    if 'page_size' not in st.session_state:
        st.session_state.page_size = 25
    
    if 'sort_by' not in st.session_state:
        st.session_state.sort_by = "transaction_date"
    
    if 'sort_order' not in st.session_state:
        st.session_state.sort_order = "DESC"
    
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = None


def reset_filters() -> None:
    """Reset all filters to default values."""
    st.session_state.filters = {
        'risk_level': None,
        'card_type': None,
        'product': None,
        'amount_bucket': None,
        'start_date': None,
        'end_date': None
    }
    st.session_state.search_term = ""
    st.session_state.page_number = 1

    widget_defaults = {
        "risk_level_filter": "All",
        "card_type_filter": "All",
        "amount_bucket_filter": "All",
        "date_preset_filter": "All time",
        "search_input": "",
        "page_size_select": st.session_state.get("page_size", 25),
    }
    for key, value in widget_defaults.items():
        if key in st.session_state:
            st.session_state[key] = value

    for key in ("start_date_filter", "end_date_filter"):
        if key in st.session_state:
            st.session_state[key] = None


def get_filter_values() -> Dict[str, Any]:
    """
    Get current filter values from session state.
    
    Returns:
        Dict[str, Any]: Dictionary of current filter values
    """
    return st.session_state.filters


# ============================================================================
# DISPLAY UTILITIES
# ============================================================================

def show_error_message(message: str, exception: Optional[Exception] = None) -> None:
    """
    Display a formatted error message.
    
    Args:
        message: Error message to display
        exception: Optional exception object
    """
    error_msg = f"❌ **Error:** {message}"
    
    if exception:
        error_msg += f"\n\n**Details:** {str(exception)}"
    
    st.error(error_msg)


def show_success_message(message: str) -> None:
    """
    Display a formatted success message.
    
    Args:
        message: Success message to display
    """
    st.success(f"✅ {message}")


def show_warning_message(message: str) -> None:
    """
    Display a formatted warning message.
    
    Args:
        message: Warning message to display
    """
    st.warning(f"⚠️ {message}")


def show_info_message(message: str) -> None:
    """
    Display a formatted info message.
    
    Args:
        message: Info message to display
    """
    st.info(f"ℹ️ {message}")


# ============================================================================
# VALIDATION UTILITIES
# ============================================================================

def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if email is valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    Validate date range.
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        
    Returns:
        bool: True if date range is valid
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    except ValueError:
        return False


# ============================================================================
# METRIC UTILITIES
# ============================================================================

def calculate_change_percentage(current: float, previous: float) -> Optional[float]:
    """
    Calculate percentage change between two values.
    
    Args:
        current: Current value
        previous: Previous value
        
    Returns:
        Optional[float]: Percentage change or None if invalid
    """
    if previous == 0 or pd.isna(previous) or pd.isna(current):
        return None
    
    return ((current - previous) / previous) * 100


def get_trend_indicator(current: float, previous: float, invert: bool = False) -> Tuple[str, str]:
    """
    Get trend indicator (up/down/neutral) and color.
    
    Args:
        current: Current value
        previous: Previous value
        invert: If True, invert the indicator (for metrics where down is good)
        
    Returns:
        Tuple[str, str]: (indicator, color)
    """
    if previous == 0 or pd.isna(previous) or pd.isna(current):
        return "→", "#94A3B8"
    
    change_pct = ((current - previous) / previous) * 100
    
    if abs(change_pct) < 1:  # Less than 1% change
        return "→", "#94A3B8"
    
    if invert:
        # For fraud metrics, down is good (green), up is bad (red)
        if change_pct > 0:
            return "↑", "#EF4444"
        else:
            return "↓", "#22C55E"
    else:
        # For positive metrics, up is good (green), down is bad (red)
        if change_pct > 0:
            return "↑", "#22C55E"
        else:
            return "↓", "#EF4444"


# ============================================================================
# CACHE UTILITIES
# ============================================================================

def get_cache_key(*args, **kwargs) -> str:
    """
    Generate a cache key from arguments.
    
    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        str: Cache key string
    """
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
    return "_".join(key_parts)


def clear_cache() -> None:
    """Clear all Streamlit caches."""
    st.cache_data.clear()
    st.cache_resource.clear()


# ============================================================================
# TEXT UTILITIES
# ============================================================================

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def highlight_text(text: str, highlight_term: str) -> str:
    """
    Highlight a term in text using markdown.
    
    Args:
        text: Text to highlight in
        highlight_term: Term to highlight
        
    Returns:
        str: Text with highlighted term
    """
    if not highlight_term:
        return text
    
    pattern = re.compile(re.escape(highlight_term), re.IGNORECASE)
    highlighted = pattern.sub(f"**:blue[{highlight_term}]**", text)
    
    return highlighted
