from telegram.ext import ConversationHandler

(
    SELECTING_ACTION,
    MANAGE_EVENTS,
    MANAGE_PARTICIPANTS,
) = map(chr, range(3))

END = ConversationHandler.END
