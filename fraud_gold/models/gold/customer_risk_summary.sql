{{ config(materialized='table') }}

select

    card4,

    card6,

    count(*) as total_transactions,

    avg(risk_score) as avg_risk_score,

    {{ high_risk_transactions() }} as fraud_transactions,

    sum(TransactionAmt) as total_amount

from {{ ref('stg_transactions') }}

where card4 is not null
  and card6 is not null

group by
    card4,
    card6