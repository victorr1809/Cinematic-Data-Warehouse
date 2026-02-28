# Cinematic Data Warehouse
Kho dữ liệu phim điện ảnh đa quốc gia từ năm 1990 tới hiện tại và Dashboard phân tích doanh thu, điểm số, thể loại phim được yêu thích, những tác phẩm điện ảnh hay nhất từng được sản xuất.
> "An idea, resilient, highly contagious. Once an idea takes hold of the brain, it is almost impossible to eradicate. An idea that is fully formed and fully understood, it sticks."     (Inception - Christopher Nolan)

## Description
### Objective
Dự án xây dựng một Data Warehouse hiện đại (Modern Data Stack) được thiết kế để xử lý, làm sạch và lưu trữ dữ liệu phim ảnh, chương trình truyền hình và diễn viên từ API TMDB (The Movie Database). Hệ thống áp dụng kiến trúc Medallion (Bronze - Silver - Gold) để phân lớp dữ liệu, biến đổi dữ liệu thô thành các mô hình đa chiều (Galaxy schema) tối ưu cho việc truy vấn phân tích OLAP.

Dữ liệu khi được thu thập về có dạng `JSONLINES` và được đẩy vào data lake để lưu trữ tạm.

### Tech Stack
- Data lake: **MinIO (S3)**
- Data warehouse: **ClickHouse**
- Data Transformation & Orchestration: **dbt (data build tool)**
- Language: **Python**

**Lý do sử dụng các công cụ này:**
- **MinIO S3:** đóng vai trò như một vùng lưu trữ tạm trước khi load data vào Database, phù hợp với dữ liệu phi cấu trúc như phim điện ảnh. Hơn nữa MinIO có khả năng kết hợp rất tốt với ClickHouse, điều này làm cho việc load dữ liệu vào ClickHouse vô cùng đơn giản.
- **ClickHouse:** Dữ liệu phim điện ảnh có nhiều trường thông tin lồng vào nhau (`nested`) và có những trường có dạng danh sách (`list`). Các RDBMS truyền thống xử lý kiểu dữ liệu này có phần phức tạp và nhưng ClickHouse hỗ trợ lưu trữ với kiểu dữ liệu `Array()` điều này giúp quy trình xử lý dạng dữ liệu này đơn giản hoá đi đáng kể. Hơn nữa ClickHouse kết hợp rất tốt với S3, khi nó có thể đọc dữ liệu dưới dạng `JSONL` được lưu trên S3 và load thẳng vào bảng.
- **DBT:** cho phép module hóa code SQL, quản lý phiên bản, tự động nhận diện thứ tự chạy các bảng qua hàm `{{ ref() }}`.

### Data source: TMDB API
Dự án sử dụng API từ [**TMDB**](https://www.themoviedb.org/) (The Movie Database) để lấy dữ liệu phim điện ảnh. TMDB là một nền tảng cơ sở dữ liệu phim điện ảnh rất phổ biến, cung cấp nhiều khía cạnh thông tin của 1 bộ phim như:
- Thông tin cơ bản
- Doanh thu (revenue), budget
- Điểm đánh giá
- Thông tin diễn viên
- Công ty sản xuất
- Nhiều thông tin khác


## Data Architecture
<img width="2400" height="1350" alt="architecture" src="https://github.com/user-attachments/assets/b73f1687-be91-4317-850a-180a482a2739" />

## Data model
<img width="995" height="610" alt="Screenshot 2026-02-28 at 18 10 57" src="https://github.com/user-attachments/assets/5f90c3ce-d958-4edc-b873-828d2bd2dda8" />



## Setup
