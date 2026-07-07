{% snapshot customer_risk_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key=['card4','card6'],
        strategy='check',
        check_cols=[
            'avg_risk_score',
            'fraud_transactions',
            'total_amount'
        ]
    )
}}

select *

from {{ ref('customer_risk_summary') }}

{% endsnapshot %}