from aiogram.types import Update, User

def get_user_from_update(update: Update) -> User | None:
    if update.message:
        return update.message.from_user
    if update.callback_query:
        return update.callback_query.from_user
    if update.inline_query:
        return update.inline_query.from_user
    return None
