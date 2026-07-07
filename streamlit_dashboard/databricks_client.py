"""
Databricks SQL Warehouse client module.
Provides a reusable, cached connection to Databricks SQL Warehouse.
"""

import streamlit as st
from typing import Optional, List, Dict, Any, TYPE_CHECKING
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config
import logging
from functools import lru_cache

from config import databricks_config, DashboardConfig

# Import Connection type only for type checking to avoid runtime errors
if TYPE_CHECKING:
    from databricks.sql import Connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabricksClient:
    """
    Singleton client for Databricks SQL Warehouse connections.
    Ensures single connection reuse across the application.
    """
    
    _instance: Optional["DatabricksClient"] = None
    _connection: Optional["Connection"] = None
    
    def __new__(cls) -> "DatabricksClient":
        """Singleton pattern to ensure single instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the Databricks client."""
        if self._initialized:
            return
        
        self._initialized = True
        self.config = databricks_config
        self.cache_ttl = DashboardConfig.cache_ttl
        
        if not self._validate_config():
            raise ValueError(
                "Databricks configuration is incomplete. "
                "Please set DATABRICKS_SERVER_HOSTNAME, "
                "DATABRICKS_HTTP_PATH, and DATABRICKS_ACCESS_TOKEN "
                "environment variables."
            )
    
    def _validate_config(self) -> bool:
        """
        Validate Databricks configuration.
        
        Returns:
            bool: True if configuration is valid
        """
        return all([
            self.config.server_hostname,
            self.config.http_path,
            self.config.access_token
        ])
    
    def get_connection(self) -> "Connection":
        """
        Get or create a Databricks SQL connection.
        Reuses existing connection if available.
        
        Returns:
            Connection: Active Databricks SQL connection
        """
        if self._connection is None:
            try:
                logger.info("Creating new Databricks SQL connection...")
                self._connection = sql.connect(
                    server_hostname=self.config.server_hostname,
                    http_path=self.config.http_path,
                    access_token=self.config.access_token
                )
                logger.info("Databricks SQL connection established successfully")
                
                # Set catalog and schema for all subsequent queries
                self._set_catalog_and_schema()
                
            except Exception as e:
                logger.error(f"Failed to connect to Databricks: {str(e)}")
                raise ConnectionError(f"Failed to connect to Databricks: {str(e)}")
        
        return self._connection
    
    def _set_catalog_and_schema(self) -> None:
        """
        Set the catalog and schema for the current session.
        This ensures all queries run against the correct schema.
        """
        try:
            with self._connection.cursor() as cursor:
                # Set catalog
                catalog_query = f"USE CATALOG {self.config.catalog}"
                cursor.execute(catalog_query)
                logger.info(f"Set catalog to: {self.config.catalog}")
                
                # Set schema
                schema_query = f"USE SCHEMA {self.config.schema}"
                cursor.execute(schema_query)
                logger.info(f"Set schema to: {self.config.schema}")
                
        except Exception as e:
            logger.warning(f"Could not set catalog/schema: {str(e)}")
            # Don't raise - this is not critical, queries can still use fully qualified names
    
    def close_connection(self) -> None:
        """Close the Databricks SQL connection."""
        if self._connection:
            try:
                self._connection.close()
                logger.info("Databricks SQL connection closed")
            except Exception as e:
                logger.error(f"Error closing connection: {str(e)}")
            finally:
                self._connection = None
    
    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a pandas DataFrame.
        
        Args:
            query: SQL query to execute
            params: Optional query parameters for parameterized queries
            
        Returns:
            pd.DataFrame: Query results
            
        Raises:
            Exception: If query execution fails
        """
        connection = None
        try:
            connection = self.get_connection()
            logger.info(f"Executing query: {query[:100]}...")
            
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Fetch results
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                # Convert to DataFrame
                df = pd.DataFrame(rows, columns=columns)
                logger.info(f"Query returned {len(df)} rows")
                
                return df
                
        except Exception as e:
            error_msg = f"Query execution failed: {str(e)}"
            logger.error(error_msg)
            
            # Create detailed error information
            detailed_error = {
                'error': str(e),
                'executed_sql': query,
                'catalog': self.config.catalog,
                'schema': self.config.schema,
                'warehouse_id': self.config.http_path
            }
            
            # Raise with detailed information
            raise Exception(f"{error_msg}\n\n**Diagnostics:**\n- Catalog: {self.config.catalog}\n- Schema: {self.config.schema}\n- Warehouse: {self.config.http_path}\n- SQL: {query[:200]}...")
    
    def execute_query_cached(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Execute a cached SQL query with TTL.
        
        Args:
            query: SQL query to execute
            params: Optional query parameters
            ttl: Cache TTL in seconds (uses default if not provided)
            
        Returns:
            pd.DataFrame: Query results
        """
        ttl = ttl or self.cache_ttl
        
        # Use Streamlit's caching with TTL
        @st.cache_data(ttl=ttl)
        def _cached_query(q: str, p: Optional[Dict]) -> pd.DataFrame:
            return self.execute_query(q, p)
        
        return _cached_query(query, params)
    
    def test_connection(self) -> bool:
        """
        Test the Databricks connection.
        
        Returns:
            bool: True if connection is successful
        """
        try:
            test_query = "SELECT 1 as test"
            result = self.execute_query(test_query)
            return len(result) > 0 and result['test'][0] == 1
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False


# Global client instance
@st.cache_resource
def get_databricks_client() -> DatabricksClient:
    """
    Get or create the global Databricks client instance.
    Cached as a resource to persist across reruns.
    
    Returns:
        DatabricksClient: Singleton Databricks client instance
    """
    return DatabricksClient()


def execute_query(
    query: str,
    params: Optional[Dict[str, Any]] = None,
    use_cache: bool = True,
    ttl: Optional[int] = None
) -> pd.DataFrame:
    """
    Convenience function to execute a query using the global client.
    
    Args:
        query: SQL query to execute
        params: Optional query parameters
        use_cache: Whether to use caching
        ttl: Cache TTL in seconds
        
    Returns:
        pd.DataFrame: Query results
    """
    client = get_databricks_client()
    
    if use_cache:
        return client.execute_query_cached(query, params, ttl)
    else:
        return client.execute_query(query, params)


def get_table_data(
    table_name: str,
    filters: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None
) -> pd.DataFrame:
    """
    Get data from a gold table with optional filters.
    
    Args:
        table_name: Name of the gold table
        filters: Optional dictionary of filters to apply
        limit: Optional row limit
        
    Returns:
        pd.DataFrame: Table data
    """
    from config import get_gold_table_name
    
    fully_qualified_name = get_gold_table_name(table_name)
    
    # Build query
    query = f"SELECT * FROM {fully_qualified_name}"
    
    # Add filters
    if filters:
        where_clauses = []
        for key, value in filters.items():
            if value is not None and value != "":
                if isinstance(value, str):
                    where_clauses.append(f"{key} = '{value}'")
                else:
                    where_clauses.append(f"{key} = {value}")
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
    
    # Add limit
    if limit:
        query += f" LIMIT {limit}"
    
    return execute_query(query)


def get_distinct_values(table_name: str, column_name: str) -> List[str]:
    """
    Get distinct values from a column in a gold table.
    
    Args:
        table_name: Name of the gold table
        column_name: Name of the column
        
    Returns:
        List[str]: List of distinct values
    """
    from config import get_gold_table_name
    
    fully_qualified_name = get_gold_table_name(table_name)
    query = f"SELECT DISTINCT {column_name} FROM {fully_qualified_name} ORDER BY {column_name}"
    
    result = execute_query(query, use_cache=True, ttl=600)  # Cache for 10 minutes
    
    return result[column_name].tolist()