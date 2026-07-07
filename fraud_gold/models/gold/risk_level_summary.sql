{{ config(materialized='table') }}

select

    risk_level,

    count(*) as total_transactions,

    {{ high_risk_transactions() }} as fraud_transactions,

    avg(risk_score) as avg_risk_score,

    sum(TransactionAmt) as total_amount,

    {{ fraud_rate() }} as fraud_rate

from {{ ref('stg_transactions') }}

group by risk_level

order by avg_risk_score desc