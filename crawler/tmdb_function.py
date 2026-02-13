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
def discover_ids(media_type, start_date, end_date, filter):
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
                # "popularity.gte": 1.0,
                "vote_count.gte": filter            # Lọc bớt rác
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
        "append_to_response": "credits" if media_type == "movie" else "external_ids,credits"
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


# --- Hàm lọc ra các trường dữ liệu quan trọng cho MOVIE
def parser_movie(raw_data, media_type):
    WRITER_JOBS = ("Writer", "Screenplay", "Story", "Co-Writer")
    COMPOSER_JOBS = ("Original Music Composer", "Music", "Composer")

    title = raw_data.get("title")
    release_date = raw_data.get("release_date")
    runtime = raw_data.get("runtime")
    original_title = raw_data.get("original_title")

    # Xử lý CAST và director
    raw_cast = raw_data.get("credits", {}).get("cast", [])[:15]
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

    for member in raw_crew:
        if member.get("job") == "Director":
            director_ids.append(member.get('id'))
            director_names.append(member.get('name'))

    # Xử lý crew
    writer_map = {}
    composer_map = {}
    
    for member in raw_crew:
        job = member.get("job")
        pid = member.get("id")
        pname = member.get("name")  

        # Lọc Biên kịch
        if job in WRITER_JOBS: writer_map[pid] = pname
            
        # Lọc Nhạc sĩ
        elif job in COMPOSER_JOBS: composer_map[pid] = pname

    # Xử lý genres, production_countries, production companies
    genres = raw_data.get("genres", [])
    genres_id = [item.get('id') for item in genres]     
    genres_name = [item.get('name') for item in genres]

    production_companies = raw_data.get("production_companies", [])
    cp_id = [item.get("id") for item in production_companies]
    cp_name = [item.get("name") for item in production_companies]

    production_countries = raw_data.get("production_countries", [])
    pc_iso = [item.get("iso_3166_1") for item in production_countries]

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
        "genres_name": genres_name,
        "production_companies_id": cp_id,
        "production_companies_name": cp_name, 
        "production_countries": pc_iso,
        "origin_country": raw_data.get("origin_country"),
        "original_language": raw_data.get("original_language"),

        # Cast and Crew
        "cast_id": cast_ids,
        "cast_name": cast_names,
        "cast_character": cast_characters,

        "director_id": director_ids,
        "director_name": director_names,

        "writer_id": list(writer_map.keys()),
        "writer_name": list(writer_map.values()),
        "composer_id": list(composer_map.keys()),
        "composer_name": list(composer_map.values())
    }

    return clean_data


# --- Hàm lọc ra các trường dữ liệu quan trọng cho TV SERIES
def parser_series(raw_data, media_type):
    WRITER_JOBS = ("Screenplay", "Writer", "Story", "Author")
    COMPOSER_JOBS = ("Original Music Composer", "Music", "Composer")

    # Xử lý genres, production_countries
    genres = raw_data.get("genres", [])
    genres_id = [item.get('id') for item in genres]     
    genres_name = [item.get('name') for item in genres]

    # imdb_id
    external_ids = raw_data.get("external_ids", {})
    imdb_id = external_ids.get("imdb_id")

    # last_episode_score
    last_episode_vote_avg = raw_data.get("last_episode_to_air", {}).get("vote_average")
    last_episode_vote_count = raw_data.get("last_episode_to_air", {}).get("vote_count")

    # seasons
    season = raw_data.get("seasons", {})
    season_name = [item.get("name") for item in season]
    season_number = [item.get("season_number") for item in season]
    season_avg = [item.get("vote_average") for item in season]

    # production_companies
    production_companies = raw_data.get("production_companies", [])
    cp_id = [item.get("id") for item in production_companies]
    cp_name = [item.get("name") for item in production_companies]

    # production_countries
    production_countries = raw_data.get("production_countries", {})
    pc_iso = [item.get("iso_3166_1") for item in production_countries]

    # cast
    raw_cast = raw_data.get("credits", {}).get("cast", [])[:15]
    raw_crew = raw_data.get("credits", {}).get("crew", [])
        
    cast_ids = []
    cast_names = []
    cast_characters = []
    
    for actor in raw_cast:
        cast_ids.append(actor.get('id'))
        cast_names.append(actor.get('name'))
        cast_characters.append(actor.get('character', '')) 
    
    # director
    created_by = raw_data.get("created_by", [])
    director_id = [item.get("id") for item in created_by]
    director_name = [item.get("name") for item in created_by]

    # Xử lý crew
    writer_map = {}
    composer_map = {}
    
    for member in raw_crew:
        job = member.get("job")
        pid = member.get("id")
        pname = member.get("name")  

        # Lọc Biên kịch
        if job in WRITER_JOBS: writer_map[pid] = pname
            
        # Lọc Nhạc sĩ
        elif job in COMPOSER_JOBS: composer_map[pid] = pname

    clean_data = {
        "id": raw_data.get("id"),
        "imdb_id": imdb_id,
        "media_type": "tv series",

        # Thông tin cơ bản
        "title": raw_data.get("name"),
        "original_title": raw_data.get("original_name"),
        
        # Thông tin thời gian
        "first_air_date": raw_data.get("first_air_date"),
        "last_air_date": raw_data.get("last_air_date"),
        "status": raw_data.get("status"),

        # Thông tin series
        "in_production": raw_data.get("in_production"),
        "languages": raw_data.get("languages", []),
        "number_of_episodes": raw_data.get("number_of_episodes"),
        "number_of_seasons": raw_data.get("number_of_seasons"),

        # Thông tin các seasons
        "season_name": season_name,
        "season_number": season_number,
        "season_vote_average": season_avg,

        # Thông tin điểm số
        "popularity": raw_data.get("popularity"),
        "series_vote_average": raw_data.get("vote_average"),
        "series_vote_count": raw_data.get("vote_count"),
        "last_episode_vote_average": last_episode_vote_avg,
        "last_episode_vote_count": last_episode_vote_count,

        # Thông tin phân loại
        "type": raw_data.get("type"),
        "genres_id": genres_id,
        "genres_name": genres_name,
        "origin_country": raw_data.get("origin_country", []),
        "original_language": raw_data.get("original_language"),
        "production_companies_id": cp_id,
        "production_companies_name": cp_name,
        "production_countries": pc_iso,

        # Cast and Crew
        "cast_id": cast_ids,
        "cast_name": cast_names, 
        "cast_character": cast_characters,

        "director_id": director_id,
        "director_name": director_name,

        "writer_id": list(writer_map.keys()),
        "writer_name": list(writer_map.values()),
        "composer_id": list(composer_map.keys()),
        "composer_name": list(composer_map.values())
    }
    return clean_data
    
