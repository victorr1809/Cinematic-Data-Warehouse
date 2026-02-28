{{ config(
    materialized='incremental',
    schema='silver',
    engine='MergeTree()',
    incremental_strategy='append',
    partition_by='toYYYYMM(_ingested_at)',
    order_by='(id, media_type)',
    on_schema_change='fail'
) }}

WITH credits_data as (
	select 
		id, media_type, cast_id, cast_character, director_id, director_name, writer_id, writer_name, composer_id, composer_name, _ingested_at
	from {{ ref('stg_movie') }}
	union all
	select 
		id, media_type, cast_id, cast_character, director_id, director_name, writer_id, writer_name, composer_id, composer_name, _ingested_at
	from {{ ref('stg_series') }}
),

new_records AS (
    SELECT * FROM credits_data  
    {% if is_incremental() %}
    WHERE (id, media_type) NOT IN (SELECT DISTINCT id, media_type FROM {{ this }})
    {% endif %}
),

cast_data AS (
    SELECT 
        id, media_type,
       	p_id AS person_id,
        if(p_id=0, 'cast unknown', 'cast') AS position,
        if(empty(trim(p_char)), 'Unknown', trim(p_char)) AS character,
        _ingested_at
    from new_records
    ARRAY JOIN
        if(empty(cast_id), [0], cast_id) AS p_id,
        if(empty(cast_character), ['Unknown'], cast_character) AS p_char
),

director_data AS (
    SELECT 
        id, media_type,
        p_id AS person_id,
        if(p_id=0, 'director unknown', 'director') AS position,
        'Unknown' AS character,
        _ingested_at
    FROM new_records
    LEFT ARRAY JOIN
        if(empty(director_id), [0], director_id) AS p_id
),

composer_data AS (
    SELECT 
        id, media_type,
        p_id AS person_id,       
        if(p_id=0, 'composer unknown', 'composer') AS position,        
        'Unknown' AS character,
        _ingested_at
    from new_records
    LEFT ARRAY JOIN
        if(empty(composer_id), [0], composer_id) AS p_id
),

writer_data AS (
    SELECT 
        id, media_type,
        p_id AS person_id,
        if(p_id=0, 'writer unknown', 'writer') AS position,
        'Unknown' AS character,
        _ingested_at
    FROM new_records
    LEFT ARRAY JOIN
        if(empty(writer_id), [0], writer_id) AS p_id
)

SELECT * FROM cast_data
UNION ALL
SELECT * FROM director_data
UNION ALL
SELECT * FROM composer_data
UNION ALL
SELECT * FROM writer_data




