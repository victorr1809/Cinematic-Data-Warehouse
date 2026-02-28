insert into bronze.movie_details
SELECT *
FROM s3(
    'http://minio:9000/tmdb-api-data/movie/*.jsonl',
    'victor', 
    'victor1234',
    'JSONEachRow' -- Format doc file JSONL
);


insert into bronze.series_details
SELECT *
FROM s3(
    'http://minio:9000/tmdb-api-data/tv/*jsonl',
    'victor', 
    'victor1234',
    'JSONEachRow' -- Format doc file JSONL
);

insert into bronze.person_details
SELECT *
FROM s3(
    'http://minio:9000/tmdb-api-data/person/*jsonl',
    'victor', 
    'victor1234',
    'JSONEachRow' -- Format doc file JSONL
);


insert into bronze.country_dict
SELECT 
	iso_3166_1,
	english_name
FROM s3(
    'http://minio:9000/tmdb-api-data/static_data/countries_iso_dict.jsonl',
    'victor', 
    'victor1234',
    'JSONEachRow' -- Format doc file JSONL
);

insert into bronze.language_dict
SELECT 
	iso_639_1,
	english_name
FROM s3(
    'http://minio:9000/tmdb-api-data/static_data/languages_iso_dict.jsonl',
    'victor', 
    'victor1234',
    'JSONEachRow' -- Format doc file JSONL
);





	
	

