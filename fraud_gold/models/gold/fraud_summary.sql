{{ config(materialized='table') }}

select

    event_date,

    count(*) as total_transactions,

    {{ high_risk_transactions() }} as fraud_transactions,

    {{ fraud_rate() }} as fraud_rate,

    sum(TransactionAmt) as total_amount,

    {{ fraud_amount() }} as fraud_amount

from {{ ref('stg_transactions') }}

group by event_date