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
  release_date,
  runtime,
  status,
  popularity,
  tmdb_score,
  tmdb_count,
  budget,
  revenue,
  original_country,
  original_language,
  _ingested_at

FROM {{ ref('stg_movie') }}
{% if is_incremental() %}
WHERE _ingested_at > (SELECT max(_ingested_at) FROM {{ this }})
{% endif %}





