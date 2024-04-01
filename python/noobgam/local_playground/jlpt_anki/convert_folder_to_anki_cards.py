import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from noobgam.local_playground.jlpt_anki.file_to_anki import convert_file_to_anki

MAX_ANTHROPIC_CONCURRENT_SESSIONS = 3

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_path = input("Root folder path: ")
    with open("processed.json", "r", encoding="utf-8") as file:
        cache = json.load(file)

    processed_files = cache.get(file_path, [])

    with ThreadPoolExecutor(max_workers=MAX_ANTHROPIC_CONCURRENT_SESSIONS) as executor:
        futures = []
        futures_to_filename = {}
        for dirpath, dirnames, filenames in os.walk(file_path):
            files_to_process = [
                filename for filename in filenames if filename not in processed_files
            ]
            for filename in files_to_process:
                full_file_path = os.path.join(dirpath, filename)
                future = executor.submit(convert_file_to_anki, full_file_path)
                futures.append(future)
                futures_to_filename[future] = filename
        full_res = []
        for future in as_completed(futures):
            try:
                full_res += future.result()
                processed_files.append(str(futures_to_filename[future]))
            except Exception as e:
                logging.error(f"Failed to process {filename}, {e}")
        cache[file_path] = processed_files
        with open("processed.json", "w", encoding="utf-8") as file:
            json.dump(cache, file, ensure_ascii=False)
        with open("current_response.txt", "w", encoding="utf-8") as file:
            json.dump(full_res, file, ensure_ascii=False)
        # print(json.dumps(
        #     full_res,
        #     ensure_ascii=False,
        #     indent=4,
        #     sort_keys=True,
        # ))
