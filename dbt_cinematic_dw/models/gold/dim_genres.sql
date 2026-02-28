{{config(
    materialized='table',
    schema='gold',
    engine='MergeTree()',
    order_by='genres_id',
    on_schema_change='fail'
)}}

select distinct genres_id, genres_name
from {{ ref('silver_genres') }}