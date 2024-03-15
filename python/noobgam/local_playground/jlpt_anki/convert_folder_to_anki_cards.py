from noobgam.local_playground.jlpt_anki.file_to_anki import convert_file_to_anki

if __name__ == "__main__":
    file_path = input('File path: ')
    print(
        convert_file_to_anki(file_path)
    )