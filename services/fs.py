import config


def delete_file(file_name_txt):
    print(f"Oh no, file {file_name_txt} will be deleted...")
    file_name_jpg = file_name_txt.replace(".txt", ".jpg")

    (config.RAW_TXT_PATH / file_name_txt).unlink()
    (config.RAW_IMAGES_PATH / file_name_jpg).unlink()

    print(f"File {file_name_txt} has been deleted!")
