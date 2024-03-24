import json
import logging

from noobgam.local_playground.jlpt_anki.file_to_anki import convert_file_to_anki

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_path = input("File path: ")
    res = convert_file_to_anki(file_path)
    print(json.dumps(
        res,
        ensure_ascii=False
    ))
