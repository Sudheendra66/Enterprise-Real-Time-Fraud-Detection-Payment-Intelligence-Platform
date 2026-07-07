"""
KPI module for the Fraud Detection Dashboard.
Handles KPI calculations, formatting, and display logic.
"""

from typing import Dict, Any, Optional, Tuple
import pandas as pd
from dataclasses import dataclass


@dataclass
class KPI:
    """KPI data structure."""
    title: str
    value: Any
    subtitle: str
    icon: str
    delta: Optional[float] = None
    delta_label: Optional[str] = None
    color: str = "#00E5FF"
    format_type: str = "number"  # number, percentage, currency, compact


class KPICalculator:
    """Calculates and formats KPIs from fraud data."""
    
    @staticmethod
    def format_number(value: float, format_type: str = "number") -> str:
        """
        Format a number based on format type.
        
        Args:
            value: Number to format
            format_type: Format type (number, percentage, currency, compact)
            
        Returns:
            str: Formatted number string
        """
        if pd.isna(value):
            return "N/A"
        
        if format_type == "percentage":
            return f"{value:.2f}%"
        elif format_type == "currency":
            if value >= 1_000_000:
                return f"${value/1_000_000:.2f}M"
            elif value >= 1_000:
                return f"${value/1_000:.2f}K"
            else:
                return f"${value:.2f}"
        elif format_type == "compact":
            if value >= 1_000_000:
                return f"{value/1_000_000:.2f}M"
            elif value >= 1_000:
                return f"{value/1_000:.2f}K"
            else:
                return f"{value:,.0f}"
        else:  # number
            return f"{value:,.0f}"
    
    @staticmethod
    def calculate_delta(current: float, previous: float) -> Tuple[float, str]:
        """
        Calculate percentage change between two values.
        
        Args:
            current: Current value
            previous: Previous value
            
        Returns:
            Tuple[float, str]: Delta percentage and direction (up/down)
        """
        if previous == 0 or pd.isna(previous) or pd.isna(current):
            return 0.0, "neutral"
        
        delta_pct = ((current - previous) / previous) * 100
        
        if delta_pct > 0:
            return delta_pct, "up"
        elif delta_pct < 0:
            return abs(delta_pct), "down"
        else:
            return 0.0, "neutral"
    
    @staticmethod
    def get_delta_color(delta_pct: float, direction: str, invert: bool = False) -> str:
        """
        Get color for delta indicator.
        
        Args:
            delta_pct: Delta percentage
            direction: Direction (up/down/neutral)
            invert: If True, invert colors (good = down for fraud metrics)
            
        Returns:
            str: Color hex code
        """
        if direction == "neutral" or delta_pct == 0:
            return "#94A3B8"  # Gray
        
        if invert:
            # For fraud metrics, down is good (green), up is bad (red)
            return "#22C55E" if direction == "down" else "#EF4444"
        else:
            # For positive metrics, up is good (green), down is bad (red)
            return "#22C55E" if direction == "up" else "#EF4444"
    
    @classmethod
    def create_total_transactions_kpi(cls, df: pd.DataFrame) -> KPI:
        """
        Create Total Transactions KPI.
        
        Args:
            df: DataFrame with fraud summary data
            
        Returns:
            KPI: Total transactions KPI object
        """
        if df.empty:
            return KPI(
                title="Total Transactions",
                value="N/A",
                subtitle="No data available",
                icon="💳",
                format_type="compact"
            )
        
        total = df['total_transactions'].iloc[0]
        
        return KPI(
            title="Total Transactions",
            value=cls.format_number(total, "compact"),
            subtitle="All transactions",
            icon="💳",
            color="#00E5FF",
            format_type="compact"
        )
    
    @classmethod
    def create_fraud_transactions_kpi(cls, df: pd.DataFrame) -> KPI:
        """
        Create Fraud Transactions KPI.
        
        Args:
            df: DataFrame with fraud summary data
            
        Returns:
            KPI: Fraud transactions KPI object
        """
        if df.empty:
            return KPI(
                title="Fraud Transactions",
                value="N/A",
                subtitle="No data available",
                icon="⚠️",
                color="#EF4444",
                format_type="number"
            )
        
        fraud_count = df['fraud_transactions'].iloc[0]
        
        return KPI(
            title="Fraud Transactions",
            value=cls.format_number(fraud_count, "number"),
            subtitle="Flagged transactions",
            icon="⚠️",
            color="#EF4444",
            format_type="number"
        )
    
    @classmethod
    def create_fraud_rate_kpi(cls, df: pd.DataFrame) -> KPI:
        """
        Create Fraud Rate % KPI.
        
        Args:
            df: DataFrame with fraud summary data
            
        Returns:
            KPI: Fraud rate KPI object
        """
        if df.empty:
            return KPI(
                title="Fraud Rate %",
                value="N/A",
                subtitle="No data available",
                icon="📊",
                color="#F59E0B",
                format_type="percentage"
            )
        
        # Get fraud_rate from dataframe
        if 'fraud_rate' in df.columns:
            fraud_rate = df['fraud_rate'].iloc[0]
        else:
            return KPI(
                title="Fraud Rate %",
                value="N/A",
                subtitle="No data available",
                icon="📊",
                color="#F59E0B",
                format_type="percentage"
            )
        
        # Determine if rate is concerning (above 5% is high)
        if fraud_rate > 5:
            color = "#EF4444"  # Red
        elif fraud_rate > 2:
            color = "#F59E0B"  # Warning
        else:
            color = "#22C55E"  # Green
        
        return KPI(
            title="Fraud Rate %",
            value=cls.format_number(fraud_rate, "percentage"),
            subtitle="Fraud percentage",
            icon="📊",
            color=color,
            format_type="percentage"
        )
    
    @classmethod
    def create_risk_level_kpi(cls, df: pd.DataFrame, risk_level: str) -> KPI:
        """
        Create Risk Level KPI (High, Medium, Low).
        
        Args:
            df: DataFrame with fraud summary data
            risk_level: Risk level (HIGH, MEDIUM, LOW)
            
        Returns:
            KPI: Risk level KPI object
        """
        if df.empty:
            return KPI(
                title=f"{risk_level} Risk",
                value="N/A",
                subtitle="No data available",
                icon="🎯",
                color="#94A3B8",
                format_type="number"
            )
        
        column_map = {
            "HIGH": "high_risk_transactions",
            "MEDIUM": "medium_risk_transactions",
            "LOW": "low_risk_transactions"
        }
        
        column = column_map.get(risk_level)
        if not column or column not in df.columns:
            return KPI(
                title=f"{risk_level} Risk",
                value="N/A",
                subtitle="No data available",
                icon="🎯",
                color="#94A3B8",
                format_type="number"
            )
        
        count = df[column].iloc[0]
        
        # Color based on risk level
        color_map = {
            "HIGH": "#EF4444",
            "MEDIUM": "#F59E0B",
            "LOW": "#22C55E"
        }
        
        icon_map = {
            "HIGH": "🔴",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }
        
        return KPI(
            title=f"{risk_level} Risk",
            value=cls.format_number(count, "number"),
            subtitle=f"{risk_level} risk transactions",
            icon=icon_map.get(risk_level, "🎯"),
            color=color_map.get(risk_level, "#00E5FF"),
            format_type="number"
        )
    
    @classmethod
    def get_all_kpis(cls, df: pd.DataFrame) -> Dict[str, KPI]:
        """
        Get all KPIs from fraud summary data.
        
        Args:
            df: DataFrame with fraud summary data
            
        Returns:
            Dict[str, KPI]: Dictionary of all KPIs
        """
        kpis = {
            "total_transactions": cls.create_total_transactions_kpi(df),
            "fraud_transactions": cls.create_fraud_transactions_kpi(df),
            "fraud_rate": cls.create_fraud_rate_kpi(df),
            "high_risk": cls.create_risk_level_kpi(df, "HIGH"),
            "medium_risk": cls.create_risk_level_kpi(df, "MEDIUM"),
            "low_risk": cls.create_risk_level_kpi(df, "LOW")
        }
        
        return kpis
    
    @classmethod
    def calculate_fraud_metrics(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate additional fraud metrics.
        
        Args:
            df: DataFrame with fraud summary data
            
        Returns:
            Dict[str, Any]: Dictionary of calculated metrics
        """
        if df.empty:
            return {}
        
        metrics = {}
        
        # Total metrics
        metrics['total_transactions'] = df['total_transactions'].iloc[0]
        metrics['fraud_transactions'] = df['fraud_transactions'].iloc[0]
        
        # Get fraud_rate from dataframe
        if 'fraud_rate' in df.columns:
            metrics['fraud_rate'] = df['fraud_rate'].iloc[0]
        else:
            metrics['fraud_rate'] = 0
        
        # Amount metrics
        if 'total_amount' in df.columns:
            metrics['total_amount'] = df['total_amount'].iloc[0]
        else:
            metrics['total_amount'] = 0
            
        if 'fraud_amount' in df.columns:
            metrics['fraud_amount'] = df['fraud_amount'].iloc[0]
        else:
            metrics['fraud_amount'] = 0
            
        if 'avg_transaction_amount' in df.columns:
            metrics['avg_transaction_amount'] = df['avg_transaction_amount'].iloc[0]
        else:
            metrics['avg_transaction_amount'] = 0
        
        # Risk distribution (not available in current schema)
        metrics['high_risk'] = 0
        metrics['medium_risk'] = 0
        metrics['low_risk'] = 0
        
        # Calculated metrics
        if metrics['total_amount'] > 0:
            metrics['fraud_amount_percentage'] = (metrics['fraud_amount'] / metrics['total_amount']) * 100
        else:
            metrics['fraud_amount_percentage'] = 0
        
        if metrics['fraud_transactions'] > 0:
            metrics['avg_fraud_amount'] = metrics['fraud_amount'] / metrics['fraud_transactions']
        else:
            metrics['avg_fraud_amount'] = 0
        
        return metrics
    
    @classmethod
    def get_kpi_summary(cls, df: pd.DataFrame) -> str:
        """
        Get a text summary of KPIs.
        
        Args:
            df: DataFrame with fraud summary data
            
        Returns:
            str: Summary text
        """
        if df.empty:
            return "No data available"
        
        metrics = cls.calculate_fraud_metrics(df)
        
        summary = f"""
        **Fraud Detection Summary:**
        - Total Transactions: {cls.format_number(metrics.get('total_transactions', 0), 'compact')}
        - Fraud Transactions: {cls.format_number(metrics.get('fraud_transactions', 0), 'number')}
        - Fraud Rate: {cls.format_number(metrics.get('fraud_rate', 0), 'percentage')}
        - Total Amount: {cls.format_number(metrics.get('total_amount', 0), 'currency')}
        - Fraud Amount: {cls.format_number(metrics.get('fraud_amount', 0), 'currency')}
        - High Risk: {cls.format_number(metrics.get('high_risk', 0), 'number')}
        - Medium Risk: {cls.format_number(metrics.get('medium_risk', 0), 'number')}
        - Low Risk: {cls.format_number(metrics.get('low_risk', 0), 'number')}
        """
        
        return summary


def render_kpi_card(kpi: KPI, column) -> None:
    """
    Render a KPI card in a Streamlit column.
    
    Args:
        kpi: KPI object to render
        column: Streamlit column to render in
    """
    import streamlit as st
    
    with column:
        # Use Streamlit's native metric component - no HTML
        st.metric(
            label=kpi.title,
            value=kpi.value,
            help=f"{kpi.icon} {kpi.subtitle}"
        )


def render_kpi_cards(kpis: Dict[str, KPI], num_columns: int = 6) -> None:
    """
    Render multiple KPI cards in a row.
    
    Args:
        kpis: Dictionary of KPI objects
        num_columns: Number of columns to display
    """
    import streamlit as st
    
    # Create columns
    cols = st.columns(num_columns)
    
    # Render each KPI in its column
    for idx, (key, kpi) in enumerate(kpis.items()):
        if idx < num_columns:
            render_kpi_card(kpi, cols[idx])