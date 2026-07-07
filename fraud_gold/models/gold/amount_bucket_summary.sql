{{ config(materialized='table') }}

select

    amount_bucket,

    count(*) as total_transactions,

    {{ high_risk_transactions() }} as fraud_transactions,

    avg(risk_score) as avg_risk_score,

    sum(TransactionAmt) as total_amount,

    {{ fraud_rate() }} as fraud_rate

from {{ ref('stg_transactions') }}

group by amount_bucket

order by avg_risk_score desc