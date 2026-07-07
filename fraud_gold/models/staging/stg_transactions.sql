{{ config(materialized='view') }}

select *

from {{ source('scored','transactions_scored') }}