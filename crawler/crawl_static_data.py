import requests
import json
import os
from pathlib import Path
from config import API_TOKEN, OUTPUT_FILE

OUTPUT_FILE_FOR_STATIC_DATA = f'{OUTPUT_FILE}/static_data'

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}

def save_to_jsonl(data, folder, filename):
    # Tạo thư mục nếu chưa tồn tại
    Path(folder).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(folder, f"{filename}.jsonl")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for entry in data:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')
    
    print(f"Đã lưu {len(data)} bản ghi vào: {file_path}")

def crawl_static_data(endpoint, filename):
    url = f"https://api.themoviedb.org/3/configuration/{endpoint}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list):
            save_to_jsonl(data, OUTPUT_FILE_FOR_STATIC_DATA, filename)
        else:
            print(f"Dữ liệu từ {endpoint} không phải dạng danh sách.")
            
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API {endpoint}: {e}")


if __name__ == "__main__":
    crawl_static_data("countries", "countries_iso_dict")
    crawl_static_data("languages", "languages_iso_dict")