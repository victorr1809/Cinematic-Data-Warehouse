-- Bang title_akas
CREATE TABLE bronze.title_akas (
    titleId String,
    ordering Int32,
    title String,
    region Nullable(String),
    language Nullable(String),
    types Nullable(String), -- Lưu tạm string để dbt tách array sau
    attributes Nullable(String),
    isOriginalTitle Nullable(UInt8)
)
ENGINE = MergeTree()
ORDER BY (titleId, ordering); 

-- Bang title_basics
CREATE TABLE bronze.title_basics (
    tconst String,
    titleType String,
    primaryTitle Nullable(String),
    originalTitle Nullable(String),
    isAdult Nullable(UInt8),
    startYear Nullable(UInt16),
    endYear Nullable(UInt16),
    runtimeMinutes Nullable(UInt32),
    genres Nullable(String)
)
ENGINE = MergeTree()
ORDER BY tconst; -- Sắp xếp theo ID phim để tìm kiếm nhanh

-- Bang title_crew
CREATE TABLE bronze.title_crew (
    tconst String,
    directors Nullable(String), -- Sẽ được parse thành Array ở tầng Silver
    writers Nullable(String)
)
ENGINE = MergeTree()
ORDER BY tconst;

-- Bang title_episode
CREATE TABLE bronze.title_episode (
    tconst String,
    parentTconst String,
    seasonNumber Nullable(Int32),
    episodeNumber Nullable(Int32)
)
ENGINE = MergeTree()
ORDER BY (parentTconst, tconst);

-- Bang title_principal
CREATE TABLE bronze.title_principals (
    tconst String,
    ordering Int32,
    nconst String,
    category Nullable(String),
    job Nullable(String),
    characters Nullable(String)
)
ENGINE = MergeTree()
ORDER BY (tconst, ordering);

-- Bang title_ratings
CREATE TABLE bronze.title_ratings (
    tconst String,
    averageRating Float32,
    numVotes UInt32
)
ENGINE = MergeTree()
ORDER BY tconst;

-- Bang name_basics
CREATE TABLE bronze.name_basics (
    nconst String,
    primaryName String,
    birthYear Nullable(UInt16),
    deathYear Nullable(UInt16),
    primaryProfession Nullable(String),
    knownForTitles Nullable(String)
)
ENGINE = MergeTree()
ORDER BY nconst;


