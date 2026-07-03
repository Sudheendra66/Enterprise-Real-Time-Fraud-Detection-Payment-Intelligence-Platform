# Enterprise Real-Time Fraud Detection & Payment Intelligence Platform

## Project Goal

Build an enterprise-grade batch + streaming data engineering platform inspired by Stripe's fraud analytics ecosystem.

The platform ingests real historical fraud transactions, replays them into Kafka to simulate a real-time payment stream, enriches them with reference/master data, applies configurable fraud rules, builds analytical marts using dbt, and visualizes operational insights through Streamlit.

---

## Business Problem

Payment companies process millions of transactions daily.

The goal is to:

- detect suspicious payment behaviour
- enrich transactions with customer, merchant and country intelligence
- calculate fraud scores
- notify fraud teams
- build executive dashboards
- demonstrate enterprise Data Engineering practices

This is NOT an authorization system.

This is a Near Real-Time Fraud Analytics Platform.

---

## Technology Stack

Streaming
- Apache Kafka
- Spark Structured Streaming

Orchestration
- Apache Airflow
- Databricks Workflows

Lakehouse
- Databricks
- Delta Lake
- Unity Catalog

Transformation
- PySpark
- dbt

Serving
- Databricks SQL Warehouse
- Streamlit

Data Quality
- dbt Tests
- Great Expectations

DevOps
- GitHub
- GitHub Actions
- Docker

Monitoring
- Databricks Monitoring
- Kafka Metrics
- Airflow Monitoring

---

## Data Sources

Streaming

- IEEE-CIS Fraud Detection Dataset
- Replay Producer (Python)
- Apache Kafka

Batch

- Customer Master
- Merchant Master
- OFAC Sanctions List
- Country Risk Index
- Exchange Rate API
- Historical Fraud Labels

---

## Final Architecture

Hybrid

Batch + Streaming

Streaming:

Kafka
↓

Spark Structured Streaming

↓

Bronze

↓

Silver

↓

Feature Engineering

↓

Fraud Rule Engine

↓

Scored

↓

dbt

↓

Gold

Batch:

Airflow

↓

Reference APIs

↓

Bronze

↓

Silver

↓

Feature Tables

↓

dbt Gold

---

## Key Features

- Hybrid Architecture
- Kafka Streaming
- Spark Structured Streaming
- Airflow Orchestration
- Unity Catalog Governance
- Medallion Architecture
- Config Driven Fraud Rules
- Dead Letter Queue
- dbt Gold Models
- CI/CD
- Data Quality
- Streamlit Dashboards
- Enterprise Monitoring

---

Architecture Status

LOCKED

No architectural changes unless implementation requires them.
