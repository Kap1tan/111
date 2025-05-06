# -*- coding: utf-8 -*-
# Вспомогательные функции и обработчики

from telegram import Update
from telegram.ext import ContextTypes

from config import States
from database import db
from handlers.start import start_callback_handler


async def back_to_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Обработчик для возврата в главное меню."""
    # Просто перенаправляем в обработчик начального меню
    return await start_callback_handler(update, context)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок."""
    # Выводим ошибку в консоль
    print(f"Произошла ошибка: {context.error}")

    # Сохраняем информацию об ошибке
    if update:
        if update.effective_user:
            user_id = update.effective_user.id
            db.update_user_data(user_id, "last_error", str(context.error))

        # Если обновление содержит сообщение
        if update.effective_message:
            await update.effective_message.reply_text(
                "Произошла ошибка. Пожалуйста, начните заново с команды /start."
            )


def get_shupa_set_by_id(set_id: str):
    """Получает набор Шуп по ID из модели."""
    from models import SHUPA_SETS

    # Находим набор по ID
    return next((item for item in SHUPA_SETS if item["id"] == set_id), None)


def get_shupa_type_by_id(type_id: str):
    """Получает тип Шупы по ID из модели."""
    from models import SHUPA_TYPES

    # Находим тип по ID
    return next((item for item in SHUPA_TYPES if item["id"] == type_id), None)


def get_shupa_effect_by_id(effect_id: str):
    """Получает эффект Шупы по ID из модели."""
    from models import SHUPA_EFFECTS

    # Находим эффект по ID
    return next((item for item in SHUPA_EFFECTS if item["id"] == effect_id), None)


def get_ritual_by_id(ritual_id: str):
    """Получает ритуал по ID из модели."""
    from models import RITUALS_INFO

    # Находим ритуал по ID
    return RITUALS_INFO.get(ritual_id, None)


def get_instruction_by_id(instruction_id: str):
    """Получает инструкцию по ID из модели."""
    from models import INSTRUCTIONS

    # Находим инструкцию по ID
    return INSTRUCTIONS.get(instruction_id, None)