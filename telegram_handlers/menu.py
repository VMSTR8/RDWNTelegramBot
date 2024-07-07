from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

from telegram_handlers.decorators import private_chat_only


@private_chat_only
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
