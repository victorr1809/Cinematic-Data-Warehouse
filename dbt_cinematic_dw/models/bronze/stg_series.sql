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
	id, media_type,
	if(imdb_id is null or trim(imdb_id) = '', 'Unknown', imdb_id) as imdb_id,

	title, 
	original_title,

	toDateOrNull(first_air_date) AS first_air_date,
	toDateOrNull(last_air_date) AS last_air_date,

	status, 
	in_production, 
	type, 
	number_of_seasons, 
	number_of_episodes,
	
	season_name,
	season_number,
	season_vote_average as tmdb_season_score,
	series_vote_average as tmdb_score,
	series_vote_count as tmdb_count,
	last_episode_vote_average as tmdb_last_ep_score,
	last_episode_vote_count as tmdb_last_ep_count,
	popularity,

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

from {{ source('bronze', 'series_details') }}
{% if is_incremental() %}
Where _ingested_at > (Select max(_ingested_at) from {{this}})
{% endif %}






	