import config

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

if __name__ == '__main__':
    with TelegramClient(StringSession(), config.TELEGRAM_API_ID, config.TELEGRAM_API_HASH) as client:
        print(client.session.save())
