from services.exporter import export_datasets
from services.openai import recognize_all_images
from services.telegram_downloader import process as process_images

if __name__ == '__main__':
    process_images()
    recognize_all_images()
    export_datasets()
