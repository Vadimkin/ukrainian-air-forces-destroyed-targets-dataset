import hashlib
import io
import os

from PIL import Image
from telethon import types
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

import config


def is_report_like_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    top_left = img.getpixel((0, 0))
    right_bottom = img.getpixel((img.width - 1, img.height - 1))
    middle_bottom = img.getpixel((img.width // 2 - 150, img.height - 150))

    # Additional check to make sure it's a report-like image
    # because KPZSU loves to use the same color scheme for some other images
    is_kpuzsu_like_image = all([
        top_left == (31, 54, 72),
        right_bottom == (31, 54, 72),
        middle_bottom == (43, 64, 83)
    ])

    is_operational_command_like_image = all([
        top_left == (255, 255, 255),
        right_bottom == (40, 55, 86),
    ])
    return is_kpuzsu_like_image or is_operational_command_like_image


def save_image(image, path):
    with open(path, "wb") as file:
        file.write(image)


async def process_messages(client):
    last_processed_message_id = None
    if config.LAST_PROCESSED_MESSAGE_ID_PATH.exists():
        with open(config.LAST_PROCESSED_MESSAGE_ID_PATH, "r") as file:
            last_processed_message_id = int(file.read().strip())
        print("Last processed message id:", last_processed_message_id)

    async for message in client.iter_messages(config.TELEGRAM_CHANNEL_NAME, min_id=last_processed_message_id, reverse=True):
        last_processed_message_id = message.id
        print("Processing message", message.id)

        if not isinstance(message.media, types.MessageMediaPhoto):
            print(f"Skipping message {message.id} because it's not a photo")
            continue

        print(f"Downloading image {message.id}")
        image = await client.download_media(message.media, file=bytes)
        is_report_image = is_report_like_image(image)
        if not is_report_image:
            print(f"Skipping message https://t.me/{config.TELEGRAM_CHANNEL_NAME}/{message.id} because it's not a report-like image")
            continue

        image_date = message.date.strftime("%d-%m-%Y_%H-%M-%S")
        image_filename = f"photo_{message.id}@{image_date}.jpg"

        print(f"Saving image {image_filename}...")
        with open(config.RAW_IMAGES_PATH / image_filename, "wb") as file:
            file.write(image)

    print(f"Saving last processed message id {last_processed_message_id}...")
    with open(config.LAST_PROCESSED_MESSAGE_ID_PATH, "w") as file:
        file.write(str(last_processed_message_id))


def process():
    client = TelegramClient(StringSession(config.TELEGRAM_SESSION_STRING), config.TELEGRAM_API_ID, config.TELEGRAM_API_HASH)
    client.start()
    client.loop.run_until_complete(process_messages(client))
    client.disconnect()
