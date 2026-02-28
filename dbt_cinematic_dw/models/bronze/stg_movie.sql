{{ config(
	materialized='incremental',
	schema="bronze",
	engine='MergeTree()',
	unique_key='id',
	incremental_strategy='delete+insert',
	partition_by='toYYYYMM(_ingested_at)',
	order_by='id',
	on_schema_change='fail'
)}}

select 
	-- Khoá chính
	id, media_type,
	if(imdb_id is null or trim(imdb_id) = '', 'Unknown', imdb_id) as imdb_id,

	-- Tên định danh
	title, 
	original_title,

	toDateOrNull(release_date) AS release_date,

	if(runtime <= 0 and imdb_id is not null, 90, runtime) as runtime,
	status, 
	
	-- Điểm
	popularity, 
	vote_average as tmdb_score, 
	vote_count as tmdb_count,

	-- Doanh thu
	budget, 
	revenue,

	genres_id,
	genres_name,

	production_companies_id,
	production_companies_name,

	if(length(origin_country)>0, origin_country[1], 'Unknown') as original_country,
	lower(trim(original_language)) as original_language,

	cast_id,
	cast_name,
	cast_character,
	director_id,
	director_name,
	writer_id,
	writer_name,
	composer_id,
	composer_name,
	_ingested_at

from {{ source('bronze', 'movie_details') }}
{% if is_incremental() %}
Where _ingested_at > (Select max(_ingested_at) from {{this}})
{% endif %}