-- Lay du lieu tu vung staging MinIO (S3) va insert vao cac bang

insert into bronze.name_basics
select *
from s3(
	'http://minio:9000/movie-data/name.basics.tsv.gz',
	'victor',
	'victor1234',
	'TSVWithNames'
);

insert into bronze.title_akas
select *
from s3(
	'http://minio:9000/movie-data/title.akas.tsv.gz',
	'victor',
	'victor1234',
	'TSVWithNames'
);

insert into bronze.title_basics
select *
from s3(
	'http://minio:9000/movie-data/title.basics.tsv.gz',
	'victor',
	'victor1234',
	'TSVWithNames'
);

insert into bronze.title_crew
select *
from s3(
	'http://minio:9000/movie-data/title.crew.tsv.gz',
	'victor',
	'victor1234',
	'TSVWithNames'
);

insert into bronze.title_episode
select *
from s3(
	'http://minio:9000/movie-data/title.episode.tsv.gz',
	'victor',
	'victor1234',
	'TSVWithNames'
);

insert into bronze.title_principals
select *
from s3(
	'http://minio:9000/movie-data/title.principals.tsv.gz',
	'victor',
	'victor1234',
	'TSVWithNames'
);

insert into bronze.title_ratings
select *
from s3(
	'http://minio:9000/movie-data/title.ratings.tsv.gz',
	'victor',
	'victor1234',
	'TSVWithNames'
);