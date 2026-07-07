{{ config(materialized='table') }}

select

    card4,

    card6,

    count(*) as total_transactions,

    {{ high_risk_transactions() }} as fraud_transactions,

    avg(TransactionAmt) as avg_transaction_amount,

    avg(risk_score) as avg_risk_score,

    {{ fraud_rate() }} as fraud_rate

from {{ ref('stg_transactions') }}

where card4 is not null
  and card6 is not null

group by
    card4,
    card6

order by fraud_rate desc
