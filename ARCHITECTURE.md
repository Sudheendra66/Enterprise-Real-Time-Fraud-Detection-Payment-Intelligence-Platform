# Architecture Decisions

## Streaming

Source

IEEE-CIS Fraud Dataset

↓

Replay Producer

↓

Kafka

↓

Spark Structured Streaming

Streaming is Near Real-Time.

Latency target

2–10 seconds.

---

## Batch

Airflow ingests

- Customer Master
- Merchant Master
- Country Risk
- OFAC
- Exchange Rates

---

## Medallion Layers

metadata

pipeline configs

fraud rules

thresholds

job configs

---

audit

pipeline logs

stream logs

DLQ logs

quality logs

---

bronze

raw ingestion

---

silver

cleaned + enriched

---

feature_store

engineered features

---

scored

fraud scores

triggered rules

---

gold

executive marts

---

## Fraud Rules

Stored inside

metadata.fraud_rules

No hardcoded rules.

---

## dbt owns Gold

Databricks owns

Bronze

Silver

Feature Store

Scored

dbt owns

Gold

Only dbt writes marts.

---

## Governance

Unity Catalog

- Metadata
- Lineage
- Audit
- Row Security
- Column Security
- Access Control

---

## Dead Letter Queue

Kafka

↓

deadletter.events

↓

bronze.dead_letter_events

↓

audit.dead_letter_logs

---

## Serving

Databricks SQL Warehouse

↓

Streamlit

---

## Alerting

Slack

Email

Webhook

Investigation Queue

---

## Monitoring

Kafka

Airflow

Databricks

Pipeline Health

Streaming Metrics

Cost Monitoring
