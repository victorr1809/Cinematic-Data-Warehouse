import clickhouse_connect
import requests
import time
import json
import config
import os
import tmdb_function
from minio import Minio
from minio.error import S3Error

def get_person_id_list(client):
    query = """
        Select distinct person_id
        From silver.silver_credits
        Limit 500
        """
    result = client.query(query)
    return [row[0] for row in result.result_rows]

def crawl_person_data():  

    file_name = f'person_batch_{int(time.time())}.jsonl'
    output_file = f'{config.OUTPUT_FILE}/person/{file_name}'
  
    try:
        client = tmdb_function.connect_clickhouse()
    except Exception as e:
        return
    
    person_ids = get_person_id_list(client)
    client.close()

    if not person_ids:
        print("Không có data cần crawl")
        return
    print("Bắt đầu crawl person details")

    data_batch = []
    BATCH_SIZE = 100

    for p_id in person_ids:
        raw_data = tmdb_function.get_person_details(p_id)
        if raw_data:
            clean_data = tmdb_function.parser_person(raw_data)
            data_batch.append(clean_data)

            # Ghi file JSONL
            if(len(data_batch) >= BATCH_SIZE):
                with open(output_file, 'a', encoding='utf-8') as f:
                    for item in data_batch:
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
                
                print(f"✅ Đã ghi {len(data_batch)} dòng vào {file_name}")
                data_batch = []
        else:
            print(f"Bỏ qua {p_id}. Tiếp tục..")
            
        time.sleep(0.01)
    
    if (len(data_batch) != 0):
        with open(output_file, 'a', encoding='utf-8') as f:
            for item in data_batch:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        print(f"✅ Đã ghi nốt {len(data_batch)} dòng vào {file_name}")

    # Day len MinIO S3
    tmdb_function.upload_jsonl_to_minio(output_file, 'person')

if __name__ == "__main__":
    crawl_person_data()