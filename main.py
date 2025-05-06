# -*- coding: utf-8 -*-
# Главный файл для запуска бота

import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

from config import BOT_TOKEN, States, PHOTOS_PATH
from database import db
from handlers import handlers

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Запуск бота."""
    # Проверяем наличие и создаем необходимые директории
    os.makedirs(PHOTOS_PATH, exist_ok=True)

    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаем ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", handlers["start"])],
        states={
            States.START: [
                CallbackQueryHandler(handlers["choose_set"], pattern='^choose_set$'),
                CallbackQueryHandler(handlers["diagnostic"], pattern='^diagnostic$'),
                # Остальные обработчики будут добавлены позже
            ],
            States.CHOOSING_SET: [
                CallbackQueryHandler(handlers["view_set"], pattern='^view_set_'),
                CallbackQueryHandler(handlers["back_to_start"], pattern='^back_to_start$'),
            ],
            States.VIEWING_SET: [
                CallbackQueryHandler(handlers["want_set"], pattern='^want_'),
                CallbackQueryHandler(handlers["choose_set"], pattern='^choose_set$'),
                CallbackQueryHandler(handlers["back_to_start"], pattern='^back_to_start$'),
            ],
            States.DIAGNOSTIC: [
                CallbackQueryHandler(handlers["process_answer"], pattern='^answer_'),
                CallbackQueryHandler(handlers["prev_question"], pattern='^prev_question$'),
                CallbackQueryHandler(handlers["back_to_start"], pattern='^back_to_start$'),
            ],
            States.DIAGNOSTIC_RESULT: [
                CallbackQueryHandler(handlers["view_set"], pattern='^view_set_'),
                CallbackQueryHandler(handlers["back_to_start"], pattern='^back_to_start$'),
            ],
            # Остальные состояния будут добавлены позже
        },
        fallbacks=[CommandHandler("start", handlers["start"])],
    )

    # Добавляем ConversationHandler в приложение
    application.add_handler(conv_handler)

    # Обработчик ошибок
    application.add_error_handler(handlers["error"])

    # Запускаем бота
    print("Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling()


if __name__ == "__main__":
    main()