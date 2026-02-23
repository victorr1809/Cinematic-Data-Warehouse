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






	
	

