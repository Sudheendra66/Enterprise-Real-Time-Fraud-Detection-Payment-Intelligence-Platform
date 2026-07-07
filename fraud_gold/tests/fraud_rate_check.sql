select *

from {{ ref('fraud_summary') }}

where fraud_rate > 100