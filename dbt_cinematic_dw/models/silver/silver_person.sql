{{ config(
    materialized='incremental',
    schema='silver',
    engine='MergeTree()',
    unique_key='person_id',
    incremental_strategy='delete+insert',
    partition_by='toYYYYMM(_ingested_at)',
    order_by='person_id',
    on_schema_change='fail'
) }}

with person_data as (
    SELECT 
        person_id, imdb_id, 
        name,
        birthday,
        deathday,
        gender,
        profession,
        place_of_birth,
        popularity,
        _ingested_at
    FROM bronze.person_details
    {% if is_incremental() %}
    WHERE _ingested_at > (SELECT max(_ingested_at) FROM {{ this }})
    {% endif %}
)

SELECT 
    person_id,
    if(imdb_id is null or trim(imdb_id) = '', 'Unknown', imdb_id) as imdb_id,
    trim(name) AS name,  
    -- Ép kiểu ngày tháng, nếu lỗi hoặc rỗng thì để NULL
    CAST(nullIf(birthday, '') AS Nullable(Date)) AS birthday,
    CAST(nullIf(deathday, '') AS Nullable(Date)) AS deathday,
    CASE 
        WHEN deathday IS NULL THEN 'Yes' 
        ELSE 'No' 
    END AS is_alive,
    CASE 
        -- Nếu TMDB không có ngày sinh -> Không thể tính tuổi, trả về NULL
        WHEN birthday IS NULL THEN NULL
        WHEN deathday IS NOT NULL THEN floor((toYYYYMMDD(deathday) - toYYYYMMDD(birthday)) / 10000)
        ELSE floor((toYYYYMMDD(today()) - toYYYYMMDD(birthday)) / 10000)       
    END AS age,
    CASE 
        WHEN gender = 1 THEN 'Female'
        WHEN gender = 2 THEN 'Male'
        ELSE 'Unknown'
    END AS gender,
    trim(profession) as profession,
    if(trim(place_of_birth) = '' or place_of_birth is null, 'Unknown', trim(place_of_birth)) AS place_of_birth,
    popularity,
    _ingested_at
    
FROM person_data