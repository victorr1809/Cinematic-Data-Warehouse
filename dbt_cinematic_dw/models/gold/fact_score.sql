{{config(
    materialized='incremental',
    schema='gold',
    engine='MergeTree()',
    unique_key=['id', 'media_type'],
    incremental_strategy='delete+insert',
    parition_by='toYYYYMM(_updated_at)',
    order_by='(id, media_type)',
    on_schema_change='fail'
)}}

WITH movies_data AS (
    SELECT 
        id, media_type,

        tmdb_score,
        tmdb_count,
        
        CAST(NULL AS Nullable(Float32)) AS tmdb_last_ep_score,
        CAST(NULL AS Nullable(Int32)) AS tmdb_last_ep_count,

        popularity,
        
        _ingested_at AS _updated_at

    FROM {{ ref('silver_movie') }}
    
    {% if is_incremental() %}
    WHERE _ingested_at > (SELECT max(_updated_at) FROM {{ this }} WHERE media_type = 'movie')
    {% endif %}
),

series_data AS (
    SELECT 
        id, media_type,
        
        tmdb_score,
        tmdb_count,
        
        CAST(tmdb_last_ep_score AS Nullable(Float32)) AS tmdb_last_ep_score,
        CAST(tmdb_last_ep_count AS Nullable(Int32)) AS tmdb_last_ep_count,
        popularity,
        _ingested_at AS _updated_at

    FROM {{ ref('silver_series') }}
    
    {% if is_incremental() %}
    WHERE _ingested_at > (SELECT max(_updated_at) FROM {{ this }} WHERE media_type = 'tv series')
    {% endif %}
),

all_data AS (
    SELECT * FROM movies_data
    UNION ALL
    SELECT * FROM series_data
)

SELECT * FROM all_data