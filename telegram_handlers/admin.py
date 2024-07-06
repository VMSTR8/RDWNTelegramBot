from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

from database.telegram_bot.db_handlers import UsersHandler


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.id
    admin = await UsersHandler.is_user_admin(telegram_id=user)
    if admin:
        text = 'Заглушка'

        buttons = [
            [
                InlineKeyboardButton(
                    text='События', callback_data=str('СОБЫТИЯ-ЗАГЛУШКА')),
                InlineKeyboardButton(
                    text='Участники', callback_data=str('УЧАСТНИКИ-ЗАГЛУШКА')),

            ]
        ]

        keyboard = InlineKeyboardMarkup(buttons)

        save_data = await update.message.reply_text(
            text=text,
            reply_markup=keyboard
        )

        context.user_data['admin_message_id'] = int(save_data.message_id)

        return 'МЕНЮ-ЗАГЛУШКА'

    not_admin = 'Команда недоступна, у тебя нет прав администратора.'
    await update.message.reply_text(
        text=not_admin
    )

    return 'END-ЗАГЛУШКА'
