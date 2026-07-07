{{ config(materialized='table') }}

select

    event_date,

    count(*) as total_transactions,

    {{ high_risk_transactions() }} as fraud_transactions,

    {{ fraud_rate() }} as fraud_rate

from {{ ref('stg_transactions') }}

group by event_date

order by event_date