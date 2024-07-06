import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler
)

from tortoise import run_async

from telegram_handlers.menu import start
from database.init import init


class TelegramBot:

    def __init__(self, token):
        self.token = token
        self.application = ApplicationBuilder().token(self.token).build()

        run_async(init())

    def run(self):

        start_handler = CommandHandler('start', start)

        self.application.add_handler(start_handler)

        logging.info('TelegramBot class worked properly, running polling')
        self.application.run_polling()
