{{config(
    materialized='table',
    schema='gold',
    engine='MergeTree()',
    order_by='production_company_id',
    on_schema_change='fail'
)}}

select distinct 
    production_company_id, 
    production_company_name
from {{ ref('silver_company') }}
