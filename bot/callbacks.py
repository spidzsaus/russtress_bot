from telegram import Update
from telegram.ext import ContextTypes
from bot.config import logger, stress_data


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(stress_data.generate_task())


async def wildcard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    word = update.message.text.strip()
    if stress_data.is_correct(word):
        await update.message.reply_text("Мегахорош.\n\n" + stress_data.generate_task())
    else:
        await update.message.reply_text(
            f"skill issue, правильный ответ {stress_data.stress(word)}."
            + "\n\n"
            + stress_data.generate_task()
        )
