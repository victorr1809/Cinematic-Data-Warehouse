{{ config(
    materialized='incremental',
    schema='silver',
    engine='MergeTree()',
    unique_key=['id', 'media_type', 'production_company_id'],
    incremental_strategy='delete+insert',
    partition_by='toYYYYMM(_ingested_at)',
    order_by='(id, media_type, production_company_id)',
    on_schema_change='fail'
) }}

with cte as (
    -- Movie_details
    select 
        id, media_type,
        case
            when empty(production_companies_id) then [-1] else production_companies_id
        end as production_company_id,
        case
            when empty(production_companies_name) then ['Unknown'] else production_companies_name
        end as production_company_name,
        _ingested_at
    from {{ ref('stg_movie') }}
    {% if is_incremental() %}
    WHERE _ingested_at > (SELECT max(_ingested_at) FROM {{ this }})
    {% endif %}
    
    union all
    -- Series_details
    select 
        id, media_type,
        case
            when empty(production_companies_id) then [-1] else production_companies_id
        end as production_company_id,
        case
            when empty(production_companies_name) then ['Unknown'] else production_companies_name
        end as production_company_name,
        _ingested_at
    from {{ ref('stg_series') }}
    {% if is_incremental() %}
    WHERE _ingested_at > (SELECT max(_ingested_at) FROM {{ this }})
    {% endif %}
)
select * from cte 
array join production_company_id, production_company_name




