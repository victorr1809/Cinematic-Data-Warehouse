# Data Catalog for Gold Layer 🥇
Gold Layer được thiết kế theo dạng Galaxy Schema, gồm các bảng fact, dimension và bridge (để giải quyết mối quan hệ N-N)
## 1. gold.dim_person
* Lưu trữ thông tin chi tiết của diễn viên, đạo diễn, biên kịch, composer xuất hiện trong các bộ phim điện ảnh.

| Tên cột | Kiểu dữ liệu | Mô tả |
|-------------|------------|------------|
| person_id | INT | Khoá chính của bảng, mỗi dòng là thông tin của một người |
| imdb_id | STRING | ID của người đó trong cơ sở dữ liệu của IMDB |
| name | String | Tên cụ thể |
| birthYear | DATE | Ngày sinh |
| deathYear | DATE | Ngày mất (nếu có) |
| profession | STRING | Chuyên môn cụ thể |

## 2. gold.dim_company
* Lưu trữ thông tin các công ty sản xuất (Warner Bros, Paramount Picture, ...) các bộ phim điện ảnh.
  
| Tên cột | Kiểu dữ liệu | Mô tả |
|-------------|------------|------------|
| production_company_id | INT | Khoá chính - mỗi dòng là thông tin một công ty |
| production_company_name | STRING | Tên cụ thể |

## 3. gold.dim_genres
* Lưu trữ thông tin thể loại phim điện ảnh
  
| Tên cột | Kiểu dữ liệu | Mô tả |
|-------------|------------|------------|
| genres_id | INT | Khoá chính - mỗi dòng là thông tin một thể loại |
| genres_name | STRING | Tên thể loại |

## 4. gold.dim_movie
* Lưu trữ thông tin chi tiết của phim lẻ (movie). Bảng này sử dụng composite key (id, media_type)

| Tên cột | Kiểu dữ liệu | Mô tả |
|-------------|------------|------------|
| id | INT | ID của bộ phim |
| media_type | STRING | Thể loại phim (mặc định là movie) |
| title | STRING | Tiêu đề |
| original_title | STRING | Tiêu đề gốc |
| release_date | DATE | Ngày phát hành |
| status | STRING | Trạng thái |
| runtime | STRING | Thời lượng |
| original_country | STRING | Quốc gia nguồn gốc |
| original_language | STRING | Ngôn ngữ |

## 5. gold.dim_series
* Lưu trữ thông tin chi tiết của phim bộ (series). Bảng này sử dụng composite key (id, media_type)

| Tên cột | Kiểu dữ liệu | Mô tả |
|-------------|------------|------------|
| id | INT | ID của bộ phim |
| media_type | STRING | Thể loại phim (mặc định là tv series) |
| title | STRING | Tiêu đề |
| original_title | STRING | Tiêu đề gốc |
| first_air_date | DATE | Ngày phát hành |
| last_air_date | DATE | Ngày kết thúc (nếu có) |
| original_country | STRING | Quốc gia nguồn gốc |
| original_language | STRING | Ngôn ngữ |
| status | STRING | Trạng thái |
| type | STRING | Loại kịch bản |
| in_production | BOOLEAN | Trạng thái sản xuất |

## 6. gold.bridge_company
* Bảng trung gian liên kết giữa bộ phim và công ty sản xuất, xử lý quan hệ N-N

| Tên cột | Kiểu dữ liệu | Mô tả |
|----------|--------------|-------|
| production_company_id | INT | ID công ty sản xuất |
| id | INT | ID bộ phim |
| media_type | STRING | Loại phim (movie/series) |
| _updated_at | DATE | Ngày cập nhập |

## 7. gold.bridge_person
* Bảng trung gian liên kết giữa dim_movie, dim_series và dim_person, xử lý quan hệ N–N và lưu vai trò tham gia.

| Tên cột | Kiểu dữ liệu | Mô tả |
|----------|--------------|-------|
| id | INT | ID bộ phim |
| media_type | STRING | Loại phim (movie/series) |
| person_id | INT | Khoá ngoại tới bảng dim_person |
| position | STRING | Vai trò tham gia trong bộ phim |
| character | STRING | Nhân vật (nếu có) |
| _updated_at | DATE | Ngày cập nhập |

---

## 8. gold.bridge_genre
* Bảng trung gian liên kết giữa media và thể loại, xử lý quan hệ N-N giữa nội dung và thể loại.

| Tên cột | Kiểu dữ liệu | Mô tả |
|----------|--------------|-------|
| id | INT | ID bộ phim |
| media_type | STRING | Loại phim (movie/series) |
| genres_id | INT | Khoá ngoại tới dim_genres |
| _updated_at | DATE | Ngày cập nhập |

## 9. gold.fact_finance

* Bảng fact lưu trữ thông tin tài chính của phim lẻ (vì phim bộ không chiếu rạp nên không có)

| Tên cột | Kiểu dữ liệu | Mô tả |
|----------|--------------|-------|
| id | INT | ID bộ phim |
| media_type | STRING | Loại phim (movie) |
| budget | INT | Nguồn vốn |
| revenue | INT | Doanh thu |
| profit | INT | Lợi nhuận |
| roi | FLOAT | Tỉ suất trên lợi nhuận |
| _updated_at | DATE | Ngày cập nhập |

## 10. fact_score
* Bảng fact lưu trữ điểm số đánh giá và độ phổ biến của bộ phim từ các nguồn như TMDB và IMDB.

| Tên cột | Kiểu dữ liệu | Mô tả |
|----------|--------------|-------|
| id | INT | ID bộ phim |
| media_type | STRING | Loại phim (movie/series) |
| tmdb_score | FLOAT | Điểm đánh giá trên TMDB |
| tmdb_count | INT | Số lượng người đánh giá |
| imdb_score | FLOAT | Điểm đánh giá trên IMDB |
| imdb_count | INT | Số lượng người đánh giá |
| tmdb_last_ep_score | FLOAT | Điểm đánh giá tập cuối cùng của Series trên TMDB |
| tmdb_last_ep_count | INT | Số lượng người đánh giá |
| popularity | FLOAT | Độ phổ biến |
| _updated_at | DATE | Ngày cập nhập |

## 11. fact_seasons
* Bảng fact lưu trữ thông tin đánh giá theo từng season của series.

| Tên cột | Kiểu dữ liệu | Mô tả |
|----------|--------------|-------|
| id | INT | ID bộ phim |
| season_number | INT | Số mùa |
| tmdb_season_score | FLOAR | Điểm đánh giá mùa trên TMDB |
| _updated_at | DATE | Ngày cập nhập |


