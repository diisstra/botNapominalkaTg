import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class TimerBotClass():
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Отправляет объяснение, как пользоваться ботом."""
        await update.message.reply_text("Hi! Use /set <seconds> to set a timer")


    async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
        """Отправьте сообщение о конце таймера"""
        job = context.job
        await context.bot.send_message(job.chat_id, text="Бип! Время вышло!")


    def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Удалить задание с указанным именем. Возвращает, было ли удалено задание."""
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True


    @classmethod
    async def set_timer(cls, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Добавьте задание в очередь."""
        chat_id = update.effective_message.chat_id
        try:
            # args[0] должно содержать время таймера в секундах
            due = float(context.args[0])
            print(context.args)
            if due < 0:
                await update.effective_message.reply_text("Извините, мы не можем вернуться в будущее!")
                return

            job_removed = cls.remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_once(cls.alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

            text = "Таймер успешно установлен!"
            if job_removed:
                text += " Старый был удален."
            await update.effective_message.reply_text(text)

        except (IndexError, ValueError):
            await update.effective_message.reply_text("Использование: /set <секунды>")


    @classmethod
    async def unset(cls, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Удалить задание, если пользователь передумал."""
        chat_id = update.message.chat_id
        job_removed = cls.remove_job_if_exists(str(chat_id), context)
        text = "Таймер успешно отменен!" if job_removed else "У вас нет активного таймера."
        await update.message.reply_text(text)


    @classmethod
    async def set_reminder(cls, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
                    [
                        InlineKeyboardButton("Option 1", callback_data="1"),
                        InlineKeyboardButton("Option 2", callback_data="2"),
                    ],
                    [InlineKeyboardButton("Option 3", callback_data="3")],
                    ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Please choose:", reply_markup=reply_markup)


    def date_transform(context_args):
        for item in context_args:
            print(item)
        now = datetime.now().strftime("%d %m %Y %H:%M:%S")
        return now
    
    async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        await query.edit_message_text(text=f"Selected option: {query.data}")