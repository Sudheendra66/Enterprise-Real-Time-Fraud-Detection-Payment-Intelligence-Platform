"""
Charts module for the Fraud Detection Dashboard.
Contains all Plotly chart implementations with professional styling.
"""

from typing import Optional, Dict, Any
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from config import dashboard_config


# ============================================================================
# CHART STYLING CONFIGURATION
# ============================================================================

# Professional color palette
COLORS = {
    'primary': '#00E5FF',
    'secondary': '#1E293B',
    'accent': '#22C55E',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'background': '#0F172A',
    'card': '#1E293B',
    'text_primary': '#F1F5F9',
    'text_secondary': '#94A3B8',
    'text_muted': '#64748B',
    
    # Chart colors
    'high_risk': '#EF4444',
    'medium_risk': '#F59E0B',
    'low_risk': '#22C55E',
    'blue': '#3B82F6',
    'purple': '#A855F7',
    'pink': '#EC4899',
    'cyan': '#06B6D4',
    'teal': '#14B8A6',
    'orange': '#F97316',
    'indigo': '#6366F1'
}

# Extended color palette for multiple series
CHART_COLORS = [
    '#00E5FF', '#3B82F6', '#A855F7', '#EC4899', '#F97316',
    '#14B8A6', '#F59E0B', '#EF4444', '#22C55E', '#6366F1',
    '#06B6D4', '#EC4899'
]


def get_chart_layout(
    title: str,
    height: int = 400,
    show_legend: bool = True,
    xaxis_title: Optional[str] = None,
    yaxis_title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get standard chart layout configuration.
    
    Args:
        title: Chart title
        height: Chart height in pixels
        show_legend: Whether to show legend
        xaxis_title: X-axis title
        yaxis_title: Y-axis title
        
    Returns:
        Dict[str, Any]: Layout configuration
    """
    layout = {
        'title': {
            'text': title,
            'font': {
                'size': 18,
                'color': COLORS['text_primary'],
                'family': 'Arial, sans-serif'
            },
            'x': 0.5,
            'xanchor': 'center'
        },
        'height': height,
        'paper_bgcolor': COLORS['card'],
        'plot_bgcolor': COLORS['secondary'],
        'font': {
            'color': COLORS['text_primary'],
            'size': 12,
            'family': 'Arial, sans-serif'
        },
        'showlegend': show_legend,
        'legend': {
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': 1.02,
            'xanchor': 'right',
            'x': 1,
            'font': {
                'size': 11,
                'color': COLORS['text_secondary']
            }
        },
        'margin': {
            'l': 60,
            'r': 40,
            't': 80,
            'b': 60
        },
        'hovermode': 'closest',
        'transition': {
            'duration': 500,
            'easing': 'cubic-in-out'
        }
    }
    
    # X-axis configuration
    layout['xaxis'] = {
        'title': {
            'text': xaxis_title,
            'font': {
                'size': 13,
                'color': COLORS['text_secondary']
            }
        },
        'gridcolor': '#334155',
        'linecolor': '#475569',
        'tickfont': {
            'color': COLORS['text_secondary'],
            'size': 11
        },
        'showgrid': True,
        'gridwidth': 0.5
    }
    
    # Y-axis configuration
    layout['yaxis'] = {
        'title': {
            'text': yaxis_title,
            'font': {
                'size': 13,
                'color': COLORS['text_secondary']
            }
        },
        'gridcolor': '#334155',
        'linecolor': '#475569',
        'tickfont': {
            'color': COLORS['text_secondary'],
            'size': 11
        },
        'showgrid': True,
        'gridwidth': 0.5
    }
    
    return layout


# ============================================================================
# RISK LEVEL DISTRIBUTION - DONUT CHART
# ============================================================================

def create_risk_level_donut(df: pd.DataFrame) -> go.Figure:
    """
    Create a donut chart for risk level distribution.
    
    Args:
        df: DataFrame with risk level summary data
        
    Returns:
        go.Figure: Plotly figure object
    """
    if df.empty:
        return go.Figure()
    
    # Prepare data
    labels = df['risk_level'].tolist()
    values = df['total_transactions'].tolist()
    
    # Color mapping
    color_map = {
        'HIGH': COLORS['high_risk'],
        'MEDIUM': COLORS['medium_risk'],
        'LOW': COLORS['low_risk']
    }
    colors = [color_map.get(label, COLORS['primary']) for label in labels]
    
    # Create donut chart with clear labels
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(
            colors=colors,
            line=dict(color=COLORS['card'], width=4)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(
            size=13,
            color=COLORS['text_primary'],
            weight='bold'
        ),
        hovertemplate='<b>%{label}</b><br>' +
                      'Transactions: %{value:,.0f}<br>' +
                      'Percentage: %{percent}<br>' +
                      '<extra></extra>',
        pull=[0.1 if label == 'HIGH' else 0.02 for label in labels],
        sort=False  # Maintain the order from the query
    )])
    
    # Update layout
    layout = get_chart_layout(
        title='Risk Level Distribution',
        height=500,
        show_legend=False
    )
    
    # Add center text
    total = sum(values)
    layout['annotations'] = [
        dict(
            text=f'<b>{total:,.0f}</b><br><span style="font-size:14px;color:#94A3B8">Total</span>',
            font=dict(size=20, color=COLORS['text_primary']),
            showarrow=False,
            x=0.5,
            y=0.5
        )
    ]
    
    # Increase margins for better spacing
    layout['margin'] = {
        'l': 50,
        'r': 50,
        't': 80,
        'b': 50
    }
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# FRAUD TREND - INTERACTIVE LINE CHART
# ============================================================================

def create_fraud_trend_line(df: pd.DataFrame) -> go.Figure:
    """
    Create an interactive line chart for fraud trends.
    
    Args:
        df: DataFrame with daily fraud trend data
        
    Returns:
        go.Figure: Plotly figure object
    """
    if df.empty:
        return go.Figure()
    
    # Create figure with secondary y-axis
    fig = make_subplots(
        specs=[[{"secondary_y": True}]],
        subplot_titles=('')
    )
    
    # Total transactions line
    fig.add_trace(
        go.Scatter(
            x=df['transaction_date'],
            y=df['total_transactions'],
            name='Total Transactions',
            mode='lines+markers',
            line=dict(
                color=COLORS['primary'],
                width=3,
                shape='spline'
            ),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>' +
                          'Total: %{y:,.0f}<br>' +
                          '<extra></extra>'
        ),
        secondary_y=False
    )
    
    # Fraud transactions line
    fig.add_trace(
        go.Scatter(
            x=df['transaction_date'],
            y=df['fraud_transactions'],
            name='Fraud Transactions',
            mode='lines+markers',
            line=dict(
                color=COLORS['danger'],
                width=3,
                shape='spline'
            ),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>' +
                          'Fraud: %{y:,.0f}<br>' +
                          '<extra></extra>'
        ),
        secondary_y=False
    )
    
    # Fraud rate line (secondary axis)
    fig.add_trace(
        go.Scatter(
            x=df['transaction_date'],
            y=df['fraud_rate'],
            name='Fraud Rate %',
            mode='lines+markers',
            line=dict(
                color=COLORS['warning'],
                width=2,
                shape='spline',
                dash='dot'
            ),
            marker=dict(size=5),
            hovertemplate='<b>%{x}</b><br>' +
                          'Rate: %{y:.2f}%<br>' +
                          '<extra></extra>'
        ),
        secondary_y=True
    )
    
    # Update layout
    layout = get_chart_layout(
        title='Fraud Trend Analysis',
        height=400,
        xaxis_title='Date',
        yaxis_title='Transaction Count'
    )
    
    # Increase top margin to fix title spacing
    layout['margin']['t'] = 100
    
    # Update y-axes
    layout['yaxis2'] = {
        'title': {
            'text': 'Fraud Rate (%)',
            'font': {
                'size': 13,
                'color': COLORS['warning']
            }
        },
        'gridcolor': '#334155',
        'linecolor': '#475569',
        'tickfont': {
            'color': COLORS['warning'],
            'size': 11
        },
        'showgrid': False
    }
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# PAYMENT METHOD ANALYSIS - STACKED BAR CHART
# ============================================================================

def create_payment_method_stacked_bar(df: pd.DataFrame) -> go.Figure:
    """
    Create a stacked bar chart for payment method analysis.
    
    Args:
        df: DataFrame with payment method summary data
        
    Returns:
        go.Figure: Plotly figure object
    """
    if df.empty:
        return go.Figure()
    
    # Group by payment method and card type
    # Use card4 as payment_method and card6 as card_type
    pivot_df = df.pivot_table(
        index='payment_method',
        columns='card_type',
        values='total_transactions',
        fill_value=0
    ).reset_index()
    
    # Create figure
    fig = go.Figure()
    
    # Add a bar for each card type
    for idx, card_type in enumerate(pivot_df.columns[1:]):
        fig.add_trace(
            go.Bar(
                x=pivot_df['payment_method'],
                y=pivot_df[card_type],
                name=card_type,
                marker_color=CHART_COLORS[idx % len(CHART_COLORS)],
                hovertemplate='<b>%{x}</b><br>' +
                              f'Card Type: {card_type}<br>' +
                              'Transactions: %{y:,.0f}<br>' +
                              '<extra></extra>'
            )
        )
    
    # Update layout
    layout = get_chart_layout(
        title='Payment Method Analysis by Card Type',
        height=400,
        xaxis_title='Payment Method',
        yaxis_title='Transaction Count',
        show_legend=True
    )
    
    layout['barmode'] = 'stack'
    layout['xaxis']['tickangle'] = -45
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# MERCHANT RISK ANALYSIS - HORIZONTAL BAR CHART
# ============================================================================

def create_merchant_risk_horizontal_bar(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    """
    Create a horizontal bar chart for merchant risk analysis.
    
    Args:
        df: DataFrame with merchant risk summary data
        top_n: Number of top merchants to display
        
    Returns:
        go.Figure: Plotly figure object
    """
    if df.empty:
        return go.Figure()
    
    # Sort and get top N
    df_sorted = df.head(top_n).sort_values('risk_score', ascending=True)
    
    # Create figure
    fig = go.Figure()
    
    # Use merchant_id if merchant_name is not available
    y_axis_label = df_sorted['merchant_name'] if 'merchant_name' in df_sorted.columns else df_sorted['merchant_id']
    
    fig.add_trace(
        go.Bar(
            y=y_axis_label,
            x=df_sorted['risk_score'],
            orientation='h',
            marker_color=COLORS['warning'],
            text=df_sorted['risk_score'].apply(lambda x: f'{x:.2f}'),
            textposition='outside',
            textfont=dict(size=10, color=COLORS['text_secondary']),
            hovertemplate='<b>%{y}</b><br>' +
                          'Risk Score: %{x:.2f}<br>' +
                          'Transactions: %{customdata[0]:,.0f}<br>' +
                          '<extra></extra>',
            customdata=df_sorted[['total_transactions']].values
        )
    )
    
    # Update layout
    layout = get_chart_layout(
        title=f'Top {top_n} Merchants by Risk Score',
        height=500,
        xaxis_title='Risk Score',
        yaxis_title='Merchant',
        show_legend=False
    )
    
    layout['yaxis']['categoryorder'] = 'total ascending'
    layout['yaxis']['tickfont'] = dict(size=10)
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# AMOUNT BUCKET DISTRIBUTION - PIE CHART
# ============================================================================

def create_amount_bucket_pie(df: pd.DataFrame) -> go.Figure:
    """
    Create a pie chart for amount bucket distribution.
    
    Args:
        df: DataFrame with amount bucket summary data
        
    Returns:
        go.Figure: Plotly figure object
    """
    if df.empty:
        return go.Figure()
    
    # Prepare data
    labels = df['amount_bucket'].tolist()
    values = df['total_transactions'].tolist()
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=CHART_COLORS[:len(labels)],
            line=dict(color=COLORS['card'], width=3)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(
            size=12,
            color=COLORS['text_primary']
        ),
        hovertemplate='<b>%{label}</b><br>' +
                      'Transactions: %{value:,.0f}<br>' +
                      'Percentage: %{percent}<br>' +
                      '<extra></extra>',
        pull=[0.05] * len(labels)
    )])
    
    # Update layout
    layout = get_chart_layout(
        title='Amount Bucket Distribution',
        height=400,
        show_legend=False
    )
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# CUSTOMER RISK ANALYSIS - BAR CHART
# ============================================================================

def create_customer_risk_bar(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    """
    Create a bar chart for customer risk analysis.
    
    Args:
        df: DataFrame with customer risk summary data
        top_n: Number of top customers to display
        
    Returns:
        go.Figure: Plotly figure object
    """
    if df.empty:
        return go.Figure()
    
    # Sort and get top N
    df_sorted = df.head(top_n).sort_values('risk_score', ascending=False)
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=df_sorted['customer_id'],
            y=df_sorted['risk_score'],
            marker_color=COLORS['warning'],
            text=df_sorted['risk_score'].apply(lambda x: f'{x:.2f}'),
            textposition='outside',
            textfont=dict(size=10, color=COLORS['text_secondary']),
            hovertemplate='<b>Customer: %{x}</b><br>' +
                          'Risk Score: %{y:.2f}<br>' +
                          'Transactions: %{customdata[0]:,.0f}<br>' +
                          '<extra></extra>',
            customdata=df_sorted[['total_transactions']].values
        )
    )
    
    # Update layout
    layout = get_chart_layout(
        title=f'Top {top_n} Customers by Risk Score',
        height=500,
        xaxis_title='Customer ID',
        yaxis_title='Risk Score',
        show_legend=False
    )
    
    layout['xaxis']['tickangle'] = -45
    
    fig.update_layout(**layout)
    
    return fig


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def apply_dark_theme(fig: go.Figure) -> go.Figure:
    """
    Apply dark theme to a Plotly figure.
    
    Args:
        fig: Plotly figure object
        
    Returns:
        go.Figure: Updated figure with dark theme
    """
    fig.update_layout(
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['secondary'],
        font_color=COLORS['text_primary'],
        title_font_color=COLORS['text_primary']
    )
    
    return fig


def create_empty_chart(message: str = "No data available") -> go.Figure:
    """
    Create an empty chart with a message.
    
    Args:
        message: Message to display
        
    Returns:
        go.Figure: Empty figure with message
    """
    fig = go.Figure()
    
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(
            size=16,
            color=COLORS['text_muted']
        )
    )
    
    layout = get_chart_layout(
        title='',
        height=400,
        show_legend=False
    )
    
    fig.update_layout(**layout)
    
    return fig


def get_chart_color_palette() -> list:
    """
    Get the chart color palette.
    
    Returns:
        list: List of color hex codes
    """
    return CHART_COLORS


def get_risk_level_colors() -> Dict[str, str]:
    """
    Get risk level color mapping.
    
    Returns:
        Dict[str, str]: Mapping of risk levels to colors
    """
    return {
        'HIGH': COLORS['danger'],
        'MEDIUM': COLORS['warning'],
        'LOW': COLORS['accent']
    }