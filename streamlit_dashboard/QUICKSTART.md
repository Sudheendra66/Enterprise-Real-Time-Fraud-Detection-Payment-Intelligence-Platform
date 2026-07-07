# Quick Start Guide - Fraud Detection Dashboard

Get your dashboard up and running in 5 minutes!

## Prerequisites

- Python 3.9+
- Databricks workspace with SQL Warehouse
- dbt gold tables populated

## Step 1: Install Dependencies

```bash
cd streamlit_dashboard
pip install -r requirements.txt
```

## Step 2: Configure Credentials

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Databricks credentials
notepad .env  # Windows
# OR
nano .env     # Linux/Mac
```

Fill in these three required values:

```env
DATABRICKS_SERVER_HOSTNAME=adb-1234567890123456.17.azuredatabricks.net
DATABRICKS_HTTP_PATH=sql/protocol/v1/warehouse/1234567890123456
DATABRICKS_ACCESS_TOKEN=dapi1234567890abcdef
```

### How to Find Your Credentials

**Server Hostname:**
1. Open your Databricks workspace URL
2. Example: `https://adb-1234567890123456.17.azuredatabricks.net`
3. Copy: `adb-1234567890123456.17.azuredatabricks.net`

**HTTP Path:**
1. Go to Databricks > SQL > SQL Warehouses
2. Click on your warehouse
3. Click "Connection Details"
4. Copy the HTTP path (e.g., `/sql/1.0/warehouses/1234567890123456`)

**Access Token:**
1. Click your profile icon (top right)
2. Settings > Developer > Access Tokens
3. Generate New Token
4. Copy the token

## Step 3: Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## Step 4: Verify Connection

When the dashboard loads:

1. Check the sidebar for "✅ Databricks Connected"
2. Verify KPI cards show data
3. Confirm charts are displaying

## Troubleshooting

### Connection Failed

**Error:** `❌ Connection Failed`

**Solution:**
- Verify all three credentials are correct in `.env`
- Check that your SQL Warehouse is running
- Ensure your access token hasn't expired

### No Data Available

**Error:** Charts show "No data available"

**Solution:**
- Verify dbt has run successfully
- Check that gold tables exist in Databricks
- Run this query in Databricks SQL to verify:
  ```sql
  SELECT COUNT(*) FROM main.fraud_gold.fraud_summary
  ```

### Module Not Found

**Error:** `ModuleNotFoundError`

**Solution:**
```bash
# Make sure you're in the streamlit_dashboard directory
cd streamlit_dashboard

# Reinstall dependencies
pip install -r requirements.txt
```

## Project Structure

```
streamlit_dashboard/
├── app.py                    # Main application
├── config.py                 # Configuration
├── databricks_client.py      # Database connection
├── queries.py                # SQL queries
├── kpis.py                   # KPI calculations
├── charts.py                 # Plotly charts
├── utils.py                  # Utilities
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore
└── README.md                # Full documentation
```

## Next Steps

1. **Customize Filters**: Modify sidebar filters in `app.py`
2. **Add Charts**: Extend chart library in `charts.py`
3. **Adjust Caching**: Modify TTL values in `config.py`
4. **Deploy**: See README.md for deployment options

## Support

- Full documentation: See [README.md](README.md)
- Issues: Create an issue in the repository
- Contact: Data Engineering Team

## Quick Commands

```bash
# Run dashboard
streamlit run app.py

# Clear cache and restart
streamlit run app.py -- --clear-cache

# Run on specific port
streamlit run app.py --server.port 8080

# Run in production mode
streamlit run app.py --server.headless true
```

---

**You're all set! 🎉**

Open http://localhost:8501 in your browser to see your dashboard.