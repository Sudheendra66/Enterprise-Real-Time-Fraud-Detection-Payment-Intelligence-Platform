"""Configuration for the Streamlit fraud analytics dashboard."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ENV_PATHS = (
    Path(__file__).parent / ".env",
    Path.cwd() / ".env",
    Path(__file__).parent.parent / ".env",
)

for env_path in ENV_PATHS:
    if env_path.exists():
        load_dotenv(env_path, override=False)
        break

try:
    import streamlit as st
except ImportError:
    st = None

if st is not None:
    for key in (
        "DATABRICKS_SERVER_HOSTNAME",
        "DATABRICKS_HTTP_PATH",
        "DATABRICKS_ACCESS_TOKEN",
        "DATABRICKS_CATALOG",
        "DATABRICKS_SCHEMA",
    ):
        if not os.getenv(key) and key in st.secrets:
            os.environ[key] = str(st.secrets[key])


@dataclass(frozen=True)
class DatabricksConfig:
    """Databricks SQL Warehouse connection settings."""

    server_hostname: str
    http_path: str
    access_token: str
    catalog: str = "fraud_platform"
    schema: str = "gold"

    @classmethod
    def from_env(cls) -> "DatabricksConfig":
        """Load Databricks settings from environment variables or Streamlit secrets."""
        return cls(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME", ""),
            http_path=os.getenv("DATABRICKS_HTTP_PATH", ""),
            access_token=os.getenv("DATABRICKS_ACCESS_TOKEN", ""),
            catalog=os.getenv("DATABRICKS_CATALOG", "fraud_platform"),
            schema=os.getenv("DATABRICKS_SCHEMA", "gold"),
        )


@dataclass(frozen=True)
class DashboardConfig:
    """Dashboard presentation and caching settings."""

    page_title: str = "Enterprise Fraud Detection Platform"
    page_icon: str = ":shield:"
    layout: str = "wide"
    sidebar_state: str = "expanded"
    primary_color: str = "#00E5FF"
    secondary_color: str = "#1E293B"
    accent_color: str = "#22C55E"
    danger_color: str = "#EF4444"
    warning_color: str = "#F59E0B"
    background_color: str = "#0F172A"
    card_background: str = "#1E293B"
    cache_ttl: int = 300
    default_page_size: int = 25
    page_size_options: tuple[int, ...] = (10, 25, 50, 100)


databricks_config = DatabricksConfig.from_env()
dashboard_config = DashboardConfig()


def missing_config_keys() -> list[str]:
    """Return required Databricks settings that are not configured."""
    required = {
        "DATABRICKS_SERVER_HOSTNAME": databricks_config.server_hostname,
        "DATABRICKS_HTTP_PATH": databricks_config.http_path,
        "DATABRICKS_ACCESS_TOKEN": databricks_config.access_token,
    }
    return [key for key, value in required.items() if not value]


def validate_config() -> bool:
    """Return True when the dashboard has the minimum Databricks settings."""
    return not missing_config_keys()


def get_gold_table_name(table_name: str) -> str:
    """Return a fully qualified Databricks Unity Catalog table name."""
    return f"{databricks_config.catalog}.{databricks_config.schema}.{table_name}"
