{{config(
    materialized='incremental',
    schema='gold',
    engine='MergeTree()',
    incremental_strategy='append',
    partition_by='toYYYYMM(_updated_at)',
    order_by='(id, media_type)',
    on_schema_change='fail'
)}}

SELECT 
    id, media_type, person_id, 
    position, character,
    _ingested_at as _updated_at

FROM {{ ref('silver_credits') }}
{% if is_incremental() %}
WHERE (id, media_type) not in (SELECT distinct id,media_type from {{this}})
{% endif %}

