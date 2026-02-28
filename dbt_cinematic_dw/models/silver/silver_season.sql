{{ config(
    materialized='incremental',
    schema='silver',
    engine='MergeTree()',
    unique_key=['id', 'season_number'],
    incremental_strategy='delete+insert',
    partition_by='toYYYYMM(_ingested_at)',
    order_by='(id, season_number)',
    on_schema_change='fail'
) }}

SELECT 
    id, season_number, 
    season_name, 
    tmdb_season_score, 
    _ingested_at
from {{ ref('stg_series') }}
array join season_number, season_name, tmdb_season_score
where season_number != 0  
{% if is_incremental() %}
and _ingested_at > (SELECT max(_ingested_at) FROM {{ this }})
{% endif %}
