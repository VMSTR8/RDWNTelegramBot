from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from database.schema.db_handlers import UsersHandler


def private_chat_only(func):
    @wraps(func)
    async def wrapped(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.message.chat.type == 'private':
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text(
                'Вызов данной команды возможен '
                'только в личном диалоговом окне с чат-ботом.')
            return
    return wrapped


def group_chat_only(group_id):
    def decorator(func):
        @wraps(func)
        async def wrapped(
                update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            if update.message.chat.id == group_id:
                return await func(update, context, *args, **kwargs)
            else:
                await update.message.reply_text(
                    f'Вызов данной команды возможен только в группе.')
                return
        return wrapped
    return decorator


def user_is_admin(func):
    @wraps(func)
    async def wrapped(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.message.from_user.id
        admin = await UsersHandler.is_user_admin(telegram_id=user)
        if admin:
            return await func(update, context, *args, **kwargs)
        else:
            not_admin = 'Команда недоступна, у тебя нет прав администратора.'
            await update.message.reply_text(
                text=not_admin
            )
            return
    return wrapped
