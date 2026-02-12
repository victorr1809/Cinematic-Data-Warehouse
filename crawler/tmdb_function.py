import requests
import time
from config import API_KEY


session = requests.Session()

# --- Hàm lấy danh sách ID theo năm ---
# def discover_ids(media_type, year, page=1):
#     """Bước A: Lấy danh sách ID"""
#     url = f"https://api.themoviedb.org/3/discover/{media_type}"
#     params = {
#         "api_key": API_KEY,
#         "page": page,
#         "sort_by": "popularity.desc",
#         "primary_release_year" if media_type == "movie" else "first_air_date_year": year
#     }
#     return session.get(url, params=params).json()


# --- Hàm lấy danh sách ID theo năm ---
def discover_ids(media_type, start_date, end_date):
    url = f"https://api.themoviedb.org/3/discover/{media_type}"
    date_key = "primary_release_date" if media_type == "movie" else "first_air_date"
    
    collected_ids = []
    page = 1
    total_pages = 1
    print(f"Đang quét {media_type.upper()} từ {start_date} đến {end_date}")

    while page <= total_pages:
        try:
            params = {
                "api_key": API_KEY,
                "language": "en-US",
                "sort_by": "popularity.desc",
                "page": page,
                f"{date_key}.gte": start_date,  # Ngày bắt đầu
                f"{date_key}.lte": end_date,    # Ngày kết thúc
                "popularity.gte": 1.0
                # "vote_count.gte": 0             # Lọc bớt rác
            }    
            response = session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                # Lưu ID
                batch_ids = [item['id'] for item in results]
                collected_ids.extend(batch_ids)
                
                # Cập nhật tổng số trang từ API (chỉ cần làm ở trang 1)
                if page == 1:
                    total_pages = data.get("total_pages", 1)
                    total_results = data.get("total_results", 0)
                    print(f"Tìm thấy tổng cộng {total_results} kết quả ({total_pages} trang).")
                    
                    # Nếu quá 500 trang, TMDB sẽ không trả về dữ liệu sau trang 500
                    if total_pages > 500:
                        print("CẢNH BÁO: Số lượng quá lớn (>10k)! Bạn nên chia nhỏ ngày ngắn hơn.")
                        import sys
                        sys.exit("Dừng chương trình.")

                if (page % 50 == 0 or page == total_pages):
                    print(f"Đã lấy trang {page}/{total_pages}")
                
                page += 1
                time.sleep(0.5)
                
            else:
                print(f"❌ Lỗi API trang {page}: {response.status_code}")
                break
                
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            time.sleep(2)

    return collected_ids


# --- Hàm lấy movie details và credits ---
def get_movie_details(media_type, item_id):
    url = f"https://api.themoviedb.org/3/{media_type}/{item_id}"   
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "append_to_response": "credits" 
    }
    
    try:
        response = session.get(url, params=params, timeout=10)      
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Bị giới hạn tốc độ (Rate Limit). Cần nghỉ ngơi thêm!")
            return None
        else:
            return None
            
    except Exception as e:
        print(f"Lỗi mạng khi lấy ID {item_id}: {e}")
        return None


# --- Hàm lọc ra các trường dữ liệu quan trọng
def parser(raw_data, media_type):

    # Xử lý sự khác biệt giữa Movie và TV SHOW
    if media_type == "movie":
        title = raw_data.get("title")
        release_date = raw_data.get("release_date")
        runtime = raw_data.get("runtime")
        original_title = raw_data.get("original_title")
    else:
        title = raw_data.get("name")
        release_date = raw_data.get("first_air_date")
        runtimes = raw_data.get("episode_run_time", []) # TV show thường có mảng runtime (VD: [45, 50]), ta lấy số trung bình hoặc số đầu tiên
        runtime = runtimes[0] if runtimes else None
        original_title = raw_data.get("original_name")

    # Xử lý CREDITS (Movie thì lấy trong crew, TV thì lấy trong created_by)
    raw_cast = raw_data.get("credits", {}).get("cast", [])[:10]
    raw_crew = raw_data.get("credits", {}).get("crew", [])
    
    cast_ids = []
    cast_names = []
    cast_characters = []

    director_ids = []
    director_names = []
    
    for actor in raw_cast:
        cast_ids.append(actor.get('id'))
        cast_names.append(actor.get('name'))
        cast_characters.append(actor.get('character', '')) 
 
    # if media_type == "movie":
    for member in raw_crew:
        if member.get("job") == "Director":
            director_ids.append(member.get('id'))
            director_names.append(member.get('name'))


    # Xử lý genres, production_countries
    genres = raw_data.get("genres", [])
    genres_id = [item.get('id') for item in genres]     
    genres_name = [item.get('name') for item in genres]

    production_countries = raw_data.get("production_countries", [])
    pc_iso = [item.get('iso_3166_1') for item in production_countries]

    clean_data = {
        "id": raw_data.get("id"),
        "imdb_id": raw_data.get("imdb_id"),
        "title_type": media_type,

        # Thông tin cơ bản
        "title": title,
        "original_title": original_title,

        # Thông tin thời gian
        "release_date": release_date,
        "runtime": runtime,
        "status": raw_data.get("status"),

        # Điểm số & Độ phổ biến
        "popularity": raw_data.get("popularity"),
        "vote_average": raw_data.get("vote_average"),
        "vote_count": raw_data.get("vote_count"),

        # Thông tin doanh thu, lợi nhuận
        "budget": raw_data.get("budget", 0),
        "revenue": raw_data.get("revenue", 0),

        # Thông tin phân loại
        "genres_id": genres_id,
        "genres_id": genres_name,
        "production_countries": pc_iso,
        "origin_country": raw_data.get("origin_country"),
        "original_language": raw_data.get("original_language"),

        # Cast and Crew
        "cast_id": cast_ids,
        "cast_name": cast_names,
        "cast_character": cast_characters,
        "director_id": director_ids,
        "director_name": director_names
    }

    return clean_data

    

    
