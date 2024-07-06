from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes


async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f'Проверка {user.mention_html()}'
    )


async def about():
    pass
