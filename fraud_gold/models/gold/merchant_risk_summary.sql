{{ config(materialized='table') }}

select

    ProductCD,

    card4,

    card6,

    count(*) as merchant_transaction_count,

    avg(risk_score) as avg_risk_score,

    {{ high_risk_transactions() }} as fraud_transactions,

    sum(TransactionAmt) as total_amount

from {{ ref('stg_transactions') }}

group by

    ProductCD,
    card4,
    card6