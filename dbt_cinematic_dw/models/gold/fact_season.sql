{{config(
    materialized='incremental',
    schema='gold',
    engine='MergeTree()',
    unique_key=['id', 'season_number'],
    incremental_strategy='delete+insert',
    parition_by='toYYYYMM(_updated_at)',
    order_by='(id, season_number)',
    on_schema_change='fail'
)}}

select 
    id, season_number,
    tmdb_season_score,
    _ingested_at as _updated_at
from {{ ref('silver_season') }}
{% if is_incremental() %}
Where _ingested_at > (SELECT max(_updated_at) from {{this}})
{% endif %}

