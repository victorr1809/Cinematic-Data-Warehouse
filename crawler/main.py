# main.py
import json
import time
import config
import tmdb_function
import sys

def run_crawler():
    # media_type = config.MEDIA_TYPE
    # start_date = config.START_DATE
    # end_date = config.END_DATE
    # api_key = config.API_KEY
    # output_file = config.OUTPUT_FILE

    # media_type = 'movie'
    # start_date = '2025-02-01'
    # end_date = '2025-03-01'

    media_type = config.MEDIA_TYPE
    start_date = config.START_DATE
    end_date = config.END_DATE

    file_name = f'{media_type}_data_{start_date}_{end_date}.jsonl'
    output_file = f'{config.OUTPUT_FILE}/{file_name}'

    print(f"BẮT ĐẦU CRAWL: {media_type.upper()}")
    print(f"Thời gian: {start_date} đến {end_date}")
    print(f"File lưu: {output_file}")

    # --- DISCOVER (QUÉT ID) ---
    print("\nĐang quét ID...")
    
    try:
        id_list = tmdb_function.discover_ids(media_type,start_date,end_date)
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

    # Mở file với mode 'a' (append) để ghi nối tiếp, buffering=1: Ghi xuống ổ cứng ngay sau mỗi dòng
    with open(output_file, "a", encoding="utf-8", buffering=1) as f:
        
        success_count = 0
        error_count = 0
        data_batch = []
        BATCH_SIZE = 500

        for index, item_id in enumerate(id_list, 1):
            try:
                raw_data = tmdb_function.get_movie_details(media_type, item_id)
                if raw_data:
                    clean_data = tmdb_function.parser(raw_data, media_type)
                    data_batch.append(clean_data)
                    success_count += 1

                    # Ghi file JSON lines

                    if(len(data_batch) >= BATCH_SIZE):
                        json_record = json.dumps(clean_data, ensure_ascii=False)
                        f.write(json_record + "\n")
                    
                else:
                    print(f"[{index}/{total_ids}] Bỏ qua ID {item_id} (Data rỗng)")
                    error_count += 1

            except Exception as e:
                print(f"-- Lỗi tại {item_id}")
                error_count += 1
            
            if index % 50 == 0 or index == len(id_list):
                 print(f"✅ [{index}/{len(id_list)}] movie")

            time.sleep(1) 

    # --- TỔNG KẾT ---
    print("="*60)
    print("HOÀN TẤT QUÁ TRÌNH CRAWL!")
    print(f"Tổng: {total_ids}")
    print(f"Thành công: {success_count}")
    print(f"Thất bại: {error_count}")
    print("="*60)

if __name__ == "__main__":

    # Cú pháp: python main.py [type] [start] [end] 
    if len(sys.argv) == 4:
        # Lấy tham số từ dòng lệnh gán đè vào config
        config.MEDIA_TYPE = sys.argv[1]
        config.START_DATE = sys.argv[2]
        config.END_DATE = sys.argv[3]

    elif len(sys.argv) > 1:
        print("Sai cú pháp! Hãy nhập đủ: python main.py [movie/tv] [start_date] [end_date]")
        sys.exit()

    run_crawler()