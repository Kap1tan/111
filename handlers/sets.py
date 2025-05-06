# -*- coding: utf-8 -*-
# Обработчики для выбора и просмотра наборов Шуп

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes

from config import BUTTONS, States, PHOTOS_PATH
from models import SHUPA_SETS
from database import db


async def choose_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Показывает доступные наборы Шуп."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Сохраняем текущее состояние пользователя
    db.update_user_data(user_id, "state", States.CHOOSING_SET)

    text = """
✨ *Выбери набор Шуп, который тебя интересует* ✨

Каждый набор имеет свою уникальную энергетику и предназначение.
Раскрой свой потенциал с помощью древней силы Шуп!
"""

    # Создаем клавиатуру с доступными наборами
    keyboard = []
    for shupa_set in SHUPA_SETS:
        keyboard.append([InlineKeyboardButton(
            shupa_set["name"],
            callback_data=f'view_set_{shupa_set["id"]}'
        )])

    keyboard.append([InlineKeyboardButton(BUTTONS["back"], callback_data='back_to_start')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    return States.CHOOSING_SET


async def view_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Показывает детали выбранного набора."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Извлекаем ID набора из callback_data
    set_id = query.data.split('_')[-1]

    # Находим набор по ID
    selected_set = next((item for item in SHUPA_SETS if item["id"] == set_id), None)

    if not selected_set:
        await query.edit_message_text(
            "Набор не найден. Вернитесь в главное меню.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(BUTTONS["back"], callback_data='back_to_start')
            ]])
        )
        return States.START

    # Сохраняем текущее состояние и выбранный набор
    db.update_user_data(user_id, "state", States.VIEWING_SET)
    db.update_user_data(user_id, "selected_set", set_id)
    db.add_viewed_set(user_id, set_id)

    # Создаем клавиатуру
    keyboard = [
        [InlineKeyboardButton(BUTTONS["want_this"], callback_data=f'want_{set_id}')],
        [InlineKeyboardButton(BUTTONS["back"], callback_data='choose_set')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Получаем путь к фото
    photo_path = os.path.join(PHOTOS_PATH, selected_set["photo"])

    # Проверяем существование файла
    if not os.path.exists(photo_path):
        # Если файл не существует, используем текстовое описание
        await query.edit_message_text(
            f"{selected_set['full_description']}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return States.VIEWING_SET

    # Отправляем фото с описанием
    with open(photo_path, 'rb') as photo_file:
        await query.message.reply_photo(
            photo=photo_file,
            caption=selected_set["full_description"],
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    # Удаляем предыдущее сообщение
    await query.delete_message()

    return States.VIEWING_SET


async def want_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Обрабатывает запрос на приобретение набора."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Извлекаем ID набора из callback_data
    set_id = query.data.split('_')[-1]

    # Находим набор по ID
    selected_set = next((item for item in SHUPA_SETS if item["id"] == set_id), None)

    if not selected_set:
        await query.edit_message_text(
            "Набор не найден. Вернитесь в главное меню.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(BUTTONS["back"], callback_data='back_to_start')
            ]])
        )
        return States.START

    # Добавляем заказ в базу данных
    db.add_order(user_id, set_id)

    # Формируем сообщение
    text = f"""
✨ *Отличный выбор!* ✨

Ты выбрал набор "*{selected_set["name"]}*".

Для завершения заказа, пожалуйста, свяжись с нашим администратором.
Он ответит на все твои вопросы и поможет завершить покупку.

Твой набор уже ждет тебя! 💫
"""

    keyboard = [
        [InlineKeyboardButton(BUTTONS["write_admin"], callback_data='contact_admin')],
        [InlineKeyboardButton(BUTTONS["back"], callback_data=f'view_set_{set_id}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    return States.VIEWING_SET