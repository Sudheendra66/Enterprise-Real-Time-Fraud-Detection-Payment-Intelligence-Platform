# Enterprise Fraud Detection Platform - Streamlit Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Databricks](https://img.shields.io/badge/Databricks-SQL%20Warehouse-orange)
![Plotly](https://img.shields.io/badge/Plotly-5.17%2B-green)

A production-grade, enterprise-level real-time fraud analytics and payment intelligence dashboard built with Streamlit, featuring dark theme, interactive Plotly visualizations, and seamless Databricks integration.

## 🎯 Features

### Core Capabilities
- **Real-time Analytics**: Live fraud detection metrics and KPIs
- **Interactive Visualizations**: 6 professional Plotly charts with hover tooltips
- **Advanced Filtering**: Multi-dimensional filters in sidebar
- **Data Exploration**: Searchable, paginated transaction table with CSV export
- **Performance Optimized**: Cached queries, lazy loading, connection pooling
- **Professional UI**: Dark theme with custom styling and smooth animations

### Dashboard Components

#### Row 1: KPI Cards
- 💳 Total Transactions
- ⚠️ Fraud Transactions
- 📊 Fraud Rate %
- 🔴 High Risk Transactions
- 🟡 Medium Risk Transactions
- 🟢 Low Risk Transactions

#### Row 2: Risk & Trend Analysis
- **Risk Level Distribution**: Interactive donut chart showing HIGH/MEDIUM/LOW risk breakdown
- **Fraud Trend Analysis**: Multi-axis line chart with total transactions, fraud count, and fraud rate over 30 days

#### Row 3: Payment & Merchant Intelligence
- **Payment Method Analysis**: Stacked bar chart by card type
- **Merchant Risk Analysis**: Horizontal bar chart of top 20 high-risk merchants

#### Row 4: Amount & Customer Analysis
- **Amount Bucket Distribution**: Pie chart showing transaction amount ranges
- **Customer Risk Analysis**: Bar chart of top 20 high-risk customers

#### Row 5: Transaction Details
- Interactive data table with search, pagination, and CSV download
- Sortable columns with custom formatting
- Real-time filtering across all dimensions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   config.py  │  │   queries.py │  │    kpis.py   │     │
│  │              │  │              │  │              │     │
│  │ • Databricks │  │ • Gold Table │  │ • KPI Calc   │     │
│  │ • Dashboard  │  │   Queries    │  │ • Formatting │     │
│  │   Config     │  │ • Filters    │  │ • Rendering  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ databricks_  │  │   charts.py  │  │   utils.py   │     │
│  │   client.py  │  │              │  │              │     │
│  │              │  │ • Plotly     │  │ • Formatting │     │
│  │ • Singleton  │  │   Charts     │  │ • Pagination │     │
│  │ • Caching    │  │ • Styling    │  │ • Search     │     │
│  │ • Connection │  │ • Themes     │  │ • Validation │     │
│  │   Pooling    │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│                    ┌──────────────┐                         │
│                    │   app.py     │                         │
│                    │              │                         │
│                    │ • Main App   │                         │
│                    │ • Layout     │                         │
│                    │ • Components │                         │
│                    │ • Routing    │                         │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQL Queries
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Databricks SQL Warehouse                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌──────────────┐                         │
│                    │  dbt Gold    │                         │
│                    │   Layer      │                         │
│                    │              │                         │
│                    │ • fraud_     │                         │
│                    │   summary    │                         │
│                    │ • daily_     │                         │
│                    │   fraud_     │                         │
│                    │   trend      │                         │
│                    │ • customer_  │                         │
│                    │   risk_      │                         │
│                    │   summary    │                         │
│                    │ • payment_   │                         │
│                    │   method_    │                         │
│                    │   summary    │                         │
│                    │ • merchant_  │                         │
│                    │   risk_      │                         │
│                    │   summary    │                         │
│                    │ • amount_    │                         │
│                    │   bucket_    │                         │
│                    │   summary    │                         │
│                    │ • risk_      │                         │
│                    │   level_     │                         │
│                    │   summary    │                         │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **Databricks Workspace**: With SQL Warehouse configured
- **dbt Gold Tables**: All 7 gold tables must be populated
  - `fraud_summary`
  - `daily_fraud_trend`
  - `customer_risk_summary`
  - `payment_method_summary`
  - `merchant_risk_summary`
  - `amount_bucket_summary`
  - `risk_level_summary`

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Enterprise-Real-Time-Fraud-Detection-Payment-Intelligence-Platform
```

### 2. Navigate to Dashboard Directory
```bash
cd streamlit_dashboard
```

### 3. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Databricks credentials
# DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
# DATABRICKS_HTTP_PATH=sql/protocol/v1/warehouse/your-warehouse-id
# DATABRICKS_ACCESS_TOKEN=your-databricks-access-token
```

### 6. Run the Dashboard
```bash
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABRICKS_SERVER_HOSTNAME` | Databricks workspace hostname | Yes | - |
| `DATABRICKS_HTTP_PATH` | SQL Warehouse HTTP path | Yes | - |
| `DATABRICKS_ACCESS_TOKEN` | Databricks access token | Yes | - |
| `DATABRICKS_CATALOG` | Unity Catalog name | No | `main` |
| `DATABRICKS_SCHEMA` | Schema name | No | `fraud_gold` |

### Getting Databricks Credentials

#### 1. Server Hostname
```
1. Open your Databricks workspace
2. Look at the URL: https://adb-1234567890123456.17.azuredatabricks.net
3. Extract: adb-1234567890123456.17.azuredatabricks.net
```

#### 2. HTTP Path
```
1. Go to Databricks Workspace
2. Navigate to SQL > SQL Warehouses
3. Select your SQL Warehouse
4. Click "Connection Details"
5. Copy the HTTP path: /sql/1.0/warehouses/1234567890123456
```

#### 3. Access Token
```
1. Go to Databricks Workspace
2. Click on your profile icon (top right)
3. Select "Settings"
4. Go to "Developer" > "Access Tokens"
5. Click "Generate New Token"
6. Copy the token (save it securely!)
```

## 📊 Dashboard Features

### Sidebar Filters
- **Risk Level**: Filter by HIGH, MEDIUM, or LOW risk
- **Card Type**: Filter by credit/debit card type
- **Amount Bucket**: Filter by transaction amount range
- **Date Range**: Custom date range selection
- **Actions**: Refresh data or reset all filters

### KPI Cards
- Large, color-coded metric displays
- Real-time values with icons
- Professional gradient backgrounds
- Hover effects and smooth transitions

### Interactive Charts
All charts feature:
- ✅ Hover tooltips with detailed information
- ✅ Professional color palette
- ✅ Responsive resizing
- ✅ Smooth animations
- ✅ Legends and titles
- ✅ Dark theme styling

### Data Table
- **Search**: Real-time search by Transaction ID or Customer ID
- **Pagination**: Navigate through large datasets (10/25/50/100 rows per page)
- **Sorting**: Click column headers to sort
- **Download**: Export current page as CSV
- **Filtering**: Applies all sidebar filters

## 🎨 Theme & Styling

### Color Palette
```python
Primary:     #00E5FF  (Cyan)
Secondary:   #1E293B  (Dark Blue Gray)
Accent:      #22C55E  (Green)
Danger:      #EF4444  (Red)
Warning:     #F59E0B  (Orange)
Background:  #0F172A  (Dark Navy)
Cards:       #1E293B  (Dark Blue Gray)
```

### Typography
- **Font Family**: Arial, sans-serif
- **KPI Values**: 32px, bold
- **Chart Titles**: 18px, semi-bold
- **Body Text**: 12-14px, regular

## 🔧 Module Documentation

### config.py
Configuration management for Databricks connections and dashboard settings.

**Key Classes:**
- `DatabricksConfig`: Databricks connection parameters
- `DashboardConfig`: Dashboard UI/UX settings

### databricks_client.py
Singleton client for Databricks SQL Warehouse connections with caching.

**Key Features:**
- Singleton pattern for connection reuse
- Query result caching with TTL
- Connection pooling
- Error handling and logging

**Key Functions:**
- `execute_query()`: Execute SQL queries with optional caching
- `get_table_data()`: Fetch data from gold tables
- `get_distinct_values()`: Get filter values

### queries.py
SQL query definitions for all gold tables.

**Query Categories:**
- Fraud Summary Queries
- Daily Fraud Trend Queries
- Customer Risk Summary Queries
- Payment Method Summary Queries
- Merchant Risk Summary Queries
- Amount Bucket Summary Queries
- Risk Level Summary Queries
- Filter & Transaction Detail Queries

### kpis.py
KPI calculation, formatting, and rendering logic.

**Key Classes:**
- `KPI`: Data structure for KPI metrics
- `KPICalculator`: Static methods for KPI calculations

**Key Functions:**
- `render_kpi_card()`: Render individual KPI card
- `render_kpi_cards()`: Render multiple KPI cards in grid

### charts.py
Plotly chart implementations with professional styling.

**Chart Types:**
- `create_risk_level_donut()`: Donut chart for risk distribution
- `create_fraud_trend_line()`: Multi-axis line chart for trends
- `create_payment_method_stacked_bar()`: Stacked bar chart
- `create_merchant_risk_horizontal_bar()`: Horizontal bar chart
- `create_amount_bucket_pie()`: Pie chart for amount distribution
- `create_customer_risk_bar()`: Bar chart for customer risk

### utils.py
Utility functions for formatting, validation, and common operations.

**Utility Categories:**
- Formatting (currency, percentage, numbers)
- Date utilities
- Data processing
- Search and filter
- Pagination
- Download helpers
- Session state management

### app.py
Main application entry point with layout and component rendering.

**Key Functions:**
- `setup_page()`: Configure Streamlit page
- `load_custom_css()`: Load dark theme CSS
- `render_header()`: Render dashboard header
- `render_sidebar_filters()`: Render filter sidebar
- `render_kpi_row()`: Render KPI cards
- `render_charts_row_2/3/4()`: Render chart rows
- `render_data_table()`: Render interactive table
- `main()`: Application entry point

## 🚀 Performance Optimization

### Caching Strategy
- **KPI Data**: Cached for 5 minutes (300 seconds)
- **Chart Data**: Cached for 5 minutes (300 seconds)
- **Filter Values**: Cached for 10 minutes (600 seconds)
- **Connection**: Singleton pattern with connection reuse

### Best Practices
1. **Lazy Loading**: Data loads only when needed
2. **Query Optimization**: Efficient SQL with proper indexing
3. **Connection Pooling**: Single connection reused across queries
4. **Cache Invalidation**: Manual refresh button clears all caches
5. **Pagination**: Large datasets paginated to avoid memory issues

## 🐛 Troubleshooting

### Common Issues

#### 1. Connection Error
```
Error: Failed to connect to Databricks
```
**Solution**: Verify your Databricks credentials in `.env` file

#### 2. Missing Gold Tables
```
Error: Table 'fraud_summary' not found
```
**Solution**: Ensure dbt has run and populated all gold tables

#### 3. Empty Data
```
No data available
```
**Solution**: Check if your gold tables have data and filters aren't too restrictive

#### 4. Slow Performance
**Solution**: 
- Increase cache TTL values
- Reduce data volume in queries
- Check Databricks SQL Warehouse size

### Debug Mode
Enable debug logging by setting in `.env`:
```bash
STREAMLIT_LOGGING_LEVEL=debug
```

## 📦 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

#### Option 1: Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add secrets in Streamlit Cloud dashboard
4. Deploy

#### Option 2: Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t fraud-dashboard .
docker run -p 8501:8501 --env-file .env fraud-dashboard
```

#### Option 3: Kubernetes
See `k8s/deployment.yaml` for Kubernetes configuration

## 🔒 Security Considerations

1. **Access Tokens**: Use service principals instead of personal tokens in production
2. **Environment Variables**: Never commit `.env` file to version control
3. **Network Security**: Use VPC peering or private link for Databricks connectivity
4. **Authentication**: Implement SSO/OAuth for dashboard access
5. **Data Access**: Follow principle of least privilege for database access

## 📈 Monitoring

### Metrics to Track
- Dashboard load time
- Query execution time
- Cache hit/miss ratio
- User session duration
- Error rates

### Logging
Logs are written to:
- Console output
- `logs/dashboard.log` (if configured)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary and confidential.

## 👥 Support

For issues and questions:
- Create an issue in the repository
- Contact the data engineering team
- Check the project documentation

## 🗺️ Roadmap

- [ ] Add more chart types (heatmaps, treemaps)
- [ ] Implement user authentication
- [ ] Add export to PDF reports
- [ ] Real-time WebSocket updates
- [ ] Machine learning model explanations
- [ ] Custom alert configuration
- [ ] Mobile-responsive design
- [ ] Multi-language support

## 📚 Related Documentation

- [Databricks SQL Documentation](https://docs.databricks.com/sql/index.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [dbt Documentation](https://docs.getdbt.com/)

---

**Built with ❤️ by the Data Engineering Team**

**Version**: 1.0.0  
**Last Updated**: 2024