{{ config(
    materialized='incremental',
    schema='gold',
    engine='MergeTree()',
    incremental_strategy='append',
    partition_by='toYYYYMM(_updated_at)',
    order_by='id',
    on_schema_change='fail'
) }}

SELECT 
    id, media_type, budget, revenue,
    CASE 
        WHEN budget = 0 OR revenue = 0 THEN NULL
        ELSE (revenue - budget)
    END AS profit,
    CASE 
        WHEN budget = 0 OR revenue = 0 THEN NULL
        ELSE CAST( (revenue - budget) AS Float64) / CAST(budget AS Float64)
    END AS roi,
    _ingested_at as _updated_at
from {{ ref('silver_movie') }}

{% if is_incremental() %}
WHERE _ingested_at > (SELECT max(_updated_at) FROM {{ this }})
{% endif %}