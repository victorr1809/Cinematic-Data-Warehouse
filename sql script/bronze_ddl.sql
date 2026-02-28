CREATE TABLE IF NOT exists bronze.movie_details(
    id UInt64,
    imdb_id Nullable(String),
    
    title_type String,
    title String,
    original_title String,
    
    release_date Nullable(String),
    runtime UInt16,
    status String,
    
    popularity Float32,
    vote_average Float32,
    vote_count UInt32,
    budget UInt64,
    revenue UInt64,
    

    genres_id Array(UInt32),
    genres_name Array(String),
    
    production_companies_id Array(UInt32),
    production_companies_name Array(String),
    
    production_countries Array(String),
    origin_country Array(String),
    original_language Nullable(String),
    
    cast_id Array(UInt64),
    cast_name Array(String),
    cast_character Array(String),
    
    director_id Array(UInt64),
    director_name Array(String),
    
    writer_id Array(UInt64),
    writer_name Array(String),
    
    composer_id Array(UInt64),
    composer_name Array(String),
    
   	_ingested_at DateTime default now()
) 
ENGINE = MergeTree
ORDER BY id;


CREATE TABLE IF NOT exists bronze.series_details(
    id UInt64,
    imdb_id Nullable(String),
    
    media_type String,
    title String,
    original_title String,
    
    first_air_date Nullable(String),
    last_air_date Nullable(String),
    status String,
    in_production Bool,
    
    languages Array(String),
    number_of_episodes UInt64,
    number_of_seasons UInt32,
    season_name Array(String),
    season_number Array(UInt32),
    season_vote_average Array(Float32), 
    
    popularity Float32,
    series_vote_average Float32,
    series_vote_count UInt32,
    last_episode_vote_average Float32,
    last_episode_vote_count UInt64,
    
    type Nullable(String), 
    genres_id Array(UInt32),
    genres_name Array(String),
    
    origin_country Array(String),
    original_language Nullable(String), 
    
    production_companies_id Array(UInt32),
    production_companies_name Array(String),  
    production_countries Array(String),
    
    cast_id Array(UInt64),
    cast_name Array(String),
    cast_character Array(String),
    
    director_id Array(UInt64),
    director_name Array(String),
    
    writer_id Array(UInt64),
    writer_name Array(String),
    
    composer_id Array(UInt64),
    composer_name Array(String),
    
    _ingested_at DateTime default now()
) 
ENGINE = MergeTree
ORDER BY id;


create table bronze.country_dict (
	iso_code String,
	english_name String
)
engine=MergeTree()
order by iso_code;



create table bronze.language_dict (
	iso_code String,
	english_name String
)
engine=MergeTree()
order by iso_code;

