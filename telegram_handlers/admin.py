from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

from database.schema.db_handlers import UsersHandler

from telegram_handlers.decorators import (
    private_chat_only,
    user_is_admin,
)

from states import (
    SELECTING_ACTION,
    MANAGE_EVENTS,
    MANAGE_PARTICIPANTS,
    END
)

@private_chat_only
@user_is_admin
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = 'Заглушка'

    buttons = [
        [
            InlineKeyboardButton(
                text='События', callback_data=str(MANAGE_EVENTS)),
            InlineKeyboardButton(
                text='Участники', callback_data=str(MANAGE_PARTICIPANTS)),

        ]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    save_data = await update.message.reply_text(
        text=text,
        reply_markup=keyboard
    )

    context.user_data['admin_message_id'] = int(save_data.message_id)

    return SELECTING_ACTION
