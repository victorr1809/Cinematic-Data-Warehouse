{{ config(
    materialized='incremental',
    schema='gold',
    engine='MergeTree()',
    unique_key='person_id',
    incremental_strategy='delete+insert',
    partition_by='toYYYYMM(_updated_at)',
    order_by='person_id',
    on_schema_change='fail'
) }}

select 
    person_id,
    imdb_id,
    name,
    birthday,
    deathday,
    is_alive,
    age,
    gender,
    profession,
    place_of_birth,
    popularity,
    _ingested_at as _updated_at
from {{ ref('silver_person') }}

{% if is_incremental() %}
WHERE _ingested_at > (SELECT max(_ingested_at) FROM {{ this }})
{% endif %}