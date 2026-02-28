{{ config(
    materialized='incremental',
    schema='gold',
    engine='MergeTree()',
    unique_key='id',
    incremental_strategy='delete+insert',
    partition_by='toYYYYMM(_updated_at)',
    order_by='id',
    on_schema_change='fail'
) }}

select 
    s.id, s.media_type,
    s.title,
    s.original_title,
    s.first_air_date,
    s.last_air_date,

    c.english_name as original_country,
    l.english_name as original_language,

    s.status,
    s.type,
    s.in_production,
    s._ingested_at as _updated_at

from {{ ref('silver_series') }} s
left join bronze.country_dict c
on s.original_country = c.iso_code
left join bronze.language_dict l
on s.original_language = l.iso_code

{% if is_incremental() %}
WHERE s._ingested_at > (SELECT max(_updated_at) FROM {{ this }})
{% endif %}