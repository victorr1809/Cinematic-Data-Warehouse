# Cinematic Data Warehouse 🎥
Kho dữ liệu phim điện ảnh đa quốc gia từ năm 1990 tới hiện tại và Dashboard phân tích doanh thu, điểm số, thể loại phim được yêu thích, những tác phẩm điện ảnh hay nhất từng được sản xuất.
> "An idea, resilient, highly contagious. Once an idea takes hold of the brain, it is almost impossible to eradicate. An idea that is fully formed and fully understood, it sticks."     (Inception - Christopher Nolan)

## Description 📖
### Objective
Dự án xây dựng một Data Warehouse hiện đại (Modern Data Stack) được thiết kế để xử lý, làm sạch và lưu trữ dữ liệu phim điện ảnh từ API TMDB (The Movie Database). Hệ thống áp dụng kiến trúc Medallion (Bronze - Silver - Gold) để phân lớp dữ liệu, xây dựng data model tối ưu cho việc truy vấn phân tích OLAP. Dữ liệu khi được thu thập về có dạng `JSONLINES` và được đẩy vào data lake để lưu trữ tạm.

Dự án áp dụng pipeline **ELT (Extract - Load - Transform)** thay vì ETL truyền thống nhằm phục vụ các mục tiêu sau:
* Bảo toàn dữ liệu thô: việc tách biệt bước Extract/Load khỏi Transform giúp hệ thống không bao giờ bị mất dữ liệu gốc, dễ dàng khôi phục hoặc tính toán lại nếu nghiệp vụ phía sau thay đổi.
* Linh hoạt: Nhiều hệ thống khác nhau có thể tiếp cận dữ liệu thô và xử lý để sử dụng với mục đích khác nhau.
* Đẩy gánh nặng Transform vào trong ClickHouse giúp tận dụng SQL làm ngôn ngữ xử lý chính. Toàn bộ logic xử lý và xây dựng data model được quản lý bằng dbt.
  
### Tech Stack 🛠️
- Data lake: **MinIO (S3)**
- Data warehouse: **ClickHouse**
- Data Transformation & Orchestration: **dbt (data build tool)**
- Language: **Python**

**Lý do sử dụng các công cụ:**
- **MinIO S3:** đóng vai trò như một data lake, lưu trữ tạm dữ liệu, phù hợp với dữ liệu phi cấu trúc như phim điện ảnh.
- **ClickHouse:** raw data là JSONL nên có nhiều trường thông tin lồng vào nhau (`nested`) và có những trường dạng danh sách (`list`). RDBMS truyền thống xử lý kiểu dữ liệu này có phần phức tạp, ClickHouse hỗ trợ lưu trữ với kiểu dữ liệu `Array()` điều này giúp xử lý dạng dữ liệu này đơn giản hoá đi đáng kể. ClickHouse kết hợp rất tốt với S3, khi nó có thể đọc trực tiếp data dưới dạng `JSONL` lưu trên S3 và load thẳng vào bảng.
- **DBT:** cho phép module hóa code SQL, quản lý phiên bản, tự động nhận diện thứ tự chạy các bảng qua hàm `{{ ref() }}`.

## Data Architecture 🏗️
<img width="2400" height="1350" alt="architecture" src="https://github.com/user-attachments/assets/b73f1687-be91-4317-850a-180a482a2739" />

### Data source 💻
Dự án sử dụng API từ [**TMDB**](https://www.themoviedb.org/) (The Movie Database) để lấy dữ liệu phim điện ảnh. TMDB là một nền tảng cơ sở dữ liệu phim điện ảnh rất phổ biến, cung cấp nhiều khía cạnh thông tin của 1 bộ phim như:
- Thông tin cơ bản
- Doanh thu, nguồn vốn
- Thông tin diễn viên
- Công ty sản xuất
- Nhiều thông tin khác
> Dữ liệu thu thập về có dạng JSONL, gồm nhiều trường dữ liệu dạng danh sách như sau:
```text
{"id": 157336, "imdb_id": "tt0816692", "title_type": "movie", "title": "Interstellar", "original_title": "Interstellar", "release_date": "2014-11-05", "runtime": 169, "status": "Released", "popularity": 46.5417, "vote_average": 8.467, "vote_count": 38846, "budget": 165000000, "revenue": 746606706, "genres_id": [12, 18, 878], "genres_name": ["Adventure", "Drama", "Science Fiction"], "production_companies_id": [923, 9996, 13769], "production_companies_name": ["Legendary Pictures", "Syncopy", "Lynda Obst Productions"], "production_countries": ["GB", "US"], "origin_country": ["US"], "original_language": "en", "cast_id": [10297, 1813, 3895, 83002, 1893, 8210, 17052, 851784, 9560, 12074, 58549, 55411, 1190668, 1892, 40039], "cast_name": ["Matthew McConaughey", "Anne Hathaway", "Michael Caine", "Jessica Chastain", "Casey Affleck", "Wes Bentley", "Topher Grace", "Mackenzie Foy", "Ellen Burstyn", "John Lithgow", "Bill Irwin", "David Gyasi", "Timothée Chalamet", "Matt Damon", "Josh Stewart"], "cast_character": ["Cooper", "Brand", "Professor Brand", "Murph", "Tom", "Doyle", "Getty", "Murph (10 Yrs.)", "Murph (older)", "Donald", "TARS (voice)", "Romilly", "Tom (15 Yrs.)", "Mann", "CASE (voice)"], "director_id": [525], "director_name": ["Christopher Nolan"], "writer_id": [527, 525], "writer_name": ["Jonathan Nolan", "Christopher Nolan"], "composer_id": [947], "composer_name": ["Hans Zimmer"]}
{"id": 27205, "imdb_id": "tt1375666", "title_type": "movie", "title": "Inception", "original_title": "Inception", "release_date": "2010-07-15", "runtime": 148, "status": "Released", "popularity": 32.9158, "vote_average": 8.37, "vote_count": 38665, "budget": 160000000, "revenue": 839030630, "genres_id": [28, 878, 12], "genres_name": ["Action", "Science Fiction", "Adventure"], "production_companies_id": [923, 9996, 174], "production_companies_name": ["Legendary Pictures", "Syncopy", "Warner Bros. Pictures"], "production_countries": ["GB", "US"], "origin_country": ["US", "GB"], "original_language": "en", "cast_id": [6193, 24045, 3899, 2524, 27578, 95697, 2037, 13022, 8293, 4935, 3895, 526, 66441, 173212, 967376], "cast_name": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ken Watanabe", "Tom Hardy", "Elliot Page", "Dileep Rao", "Cillian Murphy", "Tom Berenger", "Marion Cotillard", "Pete Postlethwaite", "Michael Caine", "Lukas Haas", "Talulah Riley", "Tohoru Masamune", "Taylor Geare"], "cast_character": ["Dom Cobb", "Arthur", "Saito", "Eames", "Ariadne", "Yusuf", "Robert Fischer, Jr.", "Peter Browning", "Mal Cobb", "Maurice Fischer", "Stephen Miles", "Nash", "Blonde", "Japanese Security Guard", "Phillipa (5 years)"], "director_id": [525], "director_name": ["Christopher Nolan"], "writer_id": [525], "writer_name": ["Christopher Nolan"], "composer_id": [947], "composer_name": ["Hans Zimmer"]}
```
## Project structure 📂
```text
├── crawled_data/             # Raw JSONL data from TMDB API
│ ├── movie/
│ ├── tv/
│ ├── person/
│ ├── static_data/
| 
├── crawler/                  # Crawl data code using API
│ ├── config.py               
│ └── crawl_media_data.py 
│ └── crawl_static_data.py
│ └── crawl_person_data.py
│ └── tmdb_function.py
│
├── dbt_cinematic_dw/         # dbt project
│ ├── macros/
│ ├── models/                 # data models (bronze, silver, gold)
│ └── dbt_project.yml
│
├── dbt-env/                  # Virtual python environment for dbt
├── docker-compose.yml
├── images/
├── sql script/               # DDL and Insert scripts for Bronze Layer
└── README.md
```

## Data flow (dbt dags) 🌊
<img width="1022" height="574" alt="dbt-dags" src="https://github.com/user-attachments/assets/cfbb89f1-e1b3-46a6-abc8-0e9d3ad049a5" />

* Flattern Array: Sử dụng `array join` trong ClickHouse để flattern các cột mảng, sau đó tách chúng thành các bảng riêng.
* Bridge table: Xây dựng các bảng cầu nối (Bridge table) để tách các bảng có mối quan hệ N-N (Many to Many) thành 1-N.

## Data model 📊
<img width="995" height="610" alt="Screenshot 2026-02-28 at 18 10 57" src="https://github.com/user-attachments/assets/5f90c3ce-d958-4edc-b873-828d2bd2dda8" />

Data model được lựa chọn là Galaxy Schema bởi vì dữ liệu gồm nhiều thực thể (phim rạp, phim bộ) và nhiều luồng sự kiện khác nhau (doanh thu, điểm số, thông tin theo từng mùa). Galaxy schema cho phép có nhiều bảng Fact (fact_score, fact_finance, fact_seasons) để xử lý từng nghiệp vụ với mức độ chi tiết nhất định.

Thông tin các bảng xem tại: [data_catalog.md](docs/data_catalog.md)
## Dashboard 
(Update)

## Key features 🎯
* Áp dụng pipeline ELT, cơ chế lưu trữ an toàn, linh hoạt, raw data có thể được sử dụng bởi nhiều mục đích khác nhau.
* Xử lý dữ liệu dạng mảng bằng SQL thông qua ClickHouse

## Setup 
Bạn có thể cài đặt dbt trong môi trường ảo (virtual env) hoặc cài thẳng vào môi trường chính.
> Tạo môi trường ảo
```text
python3.xx -m venv dbt-env
```
### Cài đặt các depedencies
```text
# Chạy dbt với ClickHouse
pip install dbt-core
pip install dbt-clickhouse

# Kết nối với ClickHouse qua python
pip install clickhouse-connect

# Kết nối với MinIO S3 qua python
pip install boto3
pip install minio
```
### Tạo dbt project
```text
dbt init dbt_cinematic_dw
```
### Chạy thử
> Để crawl dữ liệu movie/series từ [TMDB](https://www.themoviedb.org/?language=vi) sử dụng cú pháp sau
```text
python crawl_media_data.py [type] [filter] [start_date] [end_date]

Ví dụ:
python crawl_media_data.py movie 100 2026-01-01 2026-02-02
(crawl movie từ 2026-01-01 đến 2026-02-02 với điều kiện vote_count >= 100)
```

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-C72E49?style=for-the-badge&logo=minio&logoColor=white)
![ClickHouse](https://img.shields.io/badge/ClickHouse-FFCC01?style=for-the-badge&logo=clickhouse&logoColor=black)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
