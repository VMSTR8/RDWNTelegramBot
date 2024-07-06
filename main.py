import os
import logging
from datetime import datetime

from telegrambot import TelegramBot

from settings.settings import BOT_TOKEN


def main():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_file_name = datetime.now().strftime('log_%Y_%m_%d_%H_%M.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
                logging.FileHandler(os.path.join('logs', log_file_name)),
                logging.StreamHandler()
        ]
    )

    token = str(BOT_TOKEN)

    bot = TelegramBot(token=token)
    bot.run()


if __name__ == '__main__':
    main()
