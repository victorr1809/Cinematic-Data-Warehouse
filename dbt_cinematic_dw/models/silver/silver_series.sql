{{ config(
    materialized='incremental',
    schema='silver',
    engine='MergeTree()',
    unique_key='id',
    incremental_strategy='delete+insert',
    partition_by='toYYYYMM(_ingested_at)',
    order_by='id',
    on_schema_change='fail'
) }}

SELECT 
  id, media_type, imdb_id,
  title, original_title,
  first_air_date, last_air_date,
  status, in_production, type,
  number_of_seasons
  number_of_episodes,
  popularity,
  tmdb_score,
  tmdb_count,
  tmdb_last_ep_score,
  tmdb_last_ep_count,
  original_country,
  original_language,
  _ingested_at

FROM {{ ref('stg_series') }}
{% if is_incremental() %}
WHERE _ingested_at > (SELECT max(_ingested_at) FROM {{ this }})
{% endif %}