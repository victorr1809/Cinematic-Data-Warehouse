import json
import time
import config
import tmdb_function
import sys

def run_crawler():

    media_type = config.MEDIA_TYPE
    start_date = config.START_DATE
    end_date = config.END_DATE
    filter = config.FILTER

    file_name = f'{media_type}_data_{start_date}_{end_date}.jsonl'
    output_file = f'{config.OUTPUT_FILE}/{media_type}/{file_name}'

    print(f"BẮT ĐẦU CRAWL: {media_type.upper()}")
    print(f"Thời gian: {start_date} đến {end_date}")
    print(f"File lưu: {output_file}")

    # --- DISCOVER (QUÉT ID) ---
    print("\nĐang quét ID...")
    
    try:
        id_list = tmdb_function.discover_ids(media_type,start_date,end_date, filter)
    except Exception as e:
        sys.exit(f"Lỗi nghiêm trọng khi Discover: {e}")

    total_ids = len(id_list)
    if total_ids == 0:
        print("Không tìm thấy phim nào trong khoảng thời gian này. Kết thúc.")
        return

    print(f"Đã tìm thấy {total_ids} bộ phim/TV show cần xử lý.")
    print("-" * 60)

    # --- GET MOVIE DETAILS ---
    print("Bắt đầu lấy chi tiết và làm sạch dữ liệu...\n")
   
    success_count = 0
    error_count = 0
    data_batch = []
    BATCH_SIZE = 400

    for index, item_id in enumerate(id_list, 1):
        try:
            raw_data = tmdb_function.get_movie_details(media_type, item_id)
            if raw_data:
                if (media_type == 'movie'):
                    clean_data = tmdb_function.parser_movie(raw_data, media_type)
                else:
                    clean_data = tmdb_function.parser_series(raw_data, media_type)

                data_batch.append(clean_data)
                success_count += 1

                # Ghi file JSON lines
                if(len(data_batch) >= BATCH_SIZE or index == total_ids):
                    with open(output_file, "a", encoding="utf-8") as f:
                        for item in data_batch:
                            json_record = json.dumps(item, ensure_ascii=False)
                            f.write(json_record + "\n")
                    
                    print(f"✅ Đã ghi {len(data_batch)} movie vào {file_name}")
                    data_batch = []
                    
            else:
                print(f"[{index}/{total_ids}] Bỏ qua ID {item_id} (Data rỗng)")
                error_count += 1

        except Exception as e:
            print(f"-- Lỗi tại {item_id}")
            error_count += 1
            
        if index % 50 == 0 or index == len(id_list):
            print(f"✅ Crawl [{index}/{len(id_list)}] movie")

        time.sleep(0.7)

    if (len(data_batch) > 0):
        with open(output_file, "a", encoding="utf-8") as f:
            for item in data_batch:
                json_record = json.dumps(item, ensure_ascii=False)
                f.write(json_record + "\n")  
        print(f"✅ Ghi nốt {len(data_batch)} movie vào {file_name}")
        data_batch = [] 

    # --- TỔNG KẾT ---
    print("="*60)
    print("HOÀN TẤT QUÁ TRÌNH CRAWL!")
    print(f"Tổng: {total_ids}")
    print(f"Thành công: {success_count}")
    print(f"Thất bại: {error_count}")
    print("="*60)

if __name__ == "__main__":

    # Cú pháp: python main.py [type] [filter] [start] [end] 
    if len(sys.argv) == 5:
        # Lấy tham số từ dòng lệnh gán đè vào config
        config.MEDIA_TYPE = sys.argv[1]
        config.FILTER = sys.argv[2]         # Bộ lọc
        config.START_DATE = sys.argv[3]
        config.END_DATE = sys.argv[4]

    elif len(sys.argv) > 1:
        print("Sai cú pháp! Hãy nhập đủ: python main.py [movie/tv] [filter] [start_date] [end_date]")
        sys.exit()

    run_crawler()