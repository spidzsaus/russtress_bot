from telegram import Update
from telegram.ext import ContextTypes
from bot.config import logger, stress_data, language
from random import choice


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    task = stress_data.generate_task()
    await update.message.reply_text(choice(language.intro).format(task=task))


async def wildcard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    word = update.message.text.strip()
    case_map = list(map(str.isupper, word))
    if any(case_map[1:]) and case_map[0]:
        word = word[0].lower() + word[1:]

    def generate_task():
        task = stress_data.generate_task()
        if task.is_variable:
            context.user_data["vid"] = task.variable_id
        elif "vid" in context.user_data:
            del context.user_data["vid"]
        return task

    if stress_data.contains(word):
        variable_id = None
        if stress_data.is_variable(word):
            variable_id = context.user_data.get("vid", None)

        if stress_data.is_correct(word, variable_id):
            task = generate_task()
            praise = language.visual_praise
            await update.message.reply_text(
                choice(language.right_answer).format(task=task.text, praise=praise),
                parse_mode="Markdown",
            )

        else:
            task = generate_task()
            right_answer = stress_data.stress(word, variable_id)
            await update.message.reply_text(
                choice(language.wrong_answer).format(
                    right_answer=right_answer, task=task.text
                ),
                parse_mode="Markdown",
            )

    else:
        # task = stress_data.generate_task()
        await update.message.reply_text(
            choice(language.wildcard),  # .format(task=task),
            parse_mode="Markdown",
        )
