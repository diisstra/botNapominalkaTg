from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import Update
from src.timerbot import TimerBotClass
from config.conf import settings



def main() -> None:
    application = Application.builder().token(settings.TOKEN).build()

    application.add_handler(CommandHandler(["start", "help"], TimerBotClass.start))
    application.add_handler(CommandHandler("set", TimerBotClass.set_timer))
    application.add_handler(CallbackQueryHandler(TimerBotClass.button))
    application.add_handler(CommandHandler("remind", TimerBotClass.set_reminder))
    application.add_handler(CommandHandler("unset", TimerBotClass.unset))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()