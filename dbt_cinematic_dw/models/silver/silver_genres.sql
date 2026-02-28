{{ config(
    materialized='incremental',
    schema='silver',
    engine='MergeTree()',
    incremental_strategy='append',
    partition_by='toYYYYMM(_ingested_at)',
    order_by='(id, media_type)',
    on_schema_change='fail'
) }}

with cte as (
    select id, media_type, genres_id, genres_name, _ingested_at
    from {{ ref('stg_movie') }}
    array join genres_id, genres_name

    union all

    select id, media_type, genres_id, genres_name, _ingested_at
    from {{ ref('stg_series') }}
    array join genres_id, genres_name
) 
select distinct * from cte
{% if is_incremental() %}
WHERE (id, media_type) NOT IN (SELECT DISTINCT id, media_type FROM {{ this }})
{% endif %}