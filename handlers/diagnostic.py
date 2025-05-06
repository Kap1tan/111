# -*- coding: utf-8 -*-
# Обработчики для диагностики

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import BUTTONS, States
from models import DIAGNOSTIC_QUESTIONS, DIAGNOSTIC_LOGIC, DIAGNOSTIC_RESULTS, SHUPA_SETS
from database import db


async def diagnostic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Начинает процесс диагностики."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Сбрасываем данные диагностики пользователя
    db.reset_diagnostic(user_id)

    # Сохраняем текущее состояние пользователя
    db.update_user_data(user_id, "state", States.DIAGNOSTIC)

    # Отправляем первый вопрос
    await send_diagnostic_question(query, user_id)

    return States.DIAGNOSTIC


async def send_diagnostic_question(query, user_id):
    """Отправляет вопрос диагностики пользователю."""
    # Получаем данные диагностики
    diagnostic = db.get_diagnostic_state(user_id)
    question_index = diagnostic["current_question"]

    # Проверяем, не закончились ли вопросы
    if question_index >= len(DIAGNOSTIC_QUESTIONS):
        await show_diagnostic_result(query, user_id)
        return

    # Получаем текущий вопрос
    question = DIAGNOSTIC_QUESTIONS[question_index]

    # Создаем клавиатуру с вариантами ответов
    keyboard = []
    for option in question["options"]:
        keyboard.append([InlineKeyboardButton(
            option["text"],
            callback_data=f'answer_{question_index}_{option["value"]}'
        )])

    # Добавляем кнопку назад, если это не первый вопрос
    if question_index > 0:
        keyboard.append([InlineKeyboardButton(BUTTONS["back"], callback_data='prev_question')])
    else:
        keyboard.append([InlineKeyboardButton(BUTTONS["back"], callback_data='back_to_start')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Формируем текст сообщения
    text = f"""
✨ *Вопрос {question_index + 1} из {len(DIAGNOSTIC_QUESTIONS)}* ✨

{question["question"]}

Выбери ответ, который наиболее точно отражает твое состояние:
"""

    # Обновляем сообщение
    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def process_answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Обрабатывает ответ на вопрос диагностики."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Парсим callback_data для получения номера вопроса и ответа
    _, question_index, answer_value = query.data.split('_')
    question_index = int(question_index)

    # Сохраняем ответ
    db.update_diagnostic_answer(user_id, question_index, answer_value)

    # Получаем обновленное состояние диагностики
    diagnostic = db.get_diagnostic_state(user_id)

    # Проверяем, не был ли это последний вопрос
    if diagnostic["current_question"] >= len(DIAGNOSTIC_QUESTIONS):
        await show_diagnostic_result(query, user_id)
        return States.DIAGNOSTIC_RESULT
    else:
        await send_diagnostic_question(query, user_id)
        return States.DIAGNOSTIC


async def prev_question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Возвращает к предыдущему вопросу."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Получаем данные диагностики
    diagnostic = db.get_diagnostic_state(user_id)

    # Уменьшаем номер текущего вопроса
    if diagnostic["current_question"] > 0:
        diagnostic["current_question"] -= 1
        db.update_user_data(user_id, "diagnostic", diagnostic)

    # Отправляем предыдущий вопрос
    await send_diagnostic_question(query, user_id)

    return States.DIAGNOSTIC


async def show_diagnostic_result(query, user_id):
    """Показывает результат диагностики."""
    # Получаем ответы пользователя
    diagnostic = db.get_diagnostic_state(user_id)
    answers = diagnostic["answers"]

    # Преобразуем строковые ключи в целые числа
    int_answers = {int(k): v for k, v in answers.items()}

    # Определяем результат на основе логики диагностики
    first_answer = int_answers.get(0, "energy")  # Значение по умолчанию
    second_answer = int_answers.get(1, "warrior")  # Значение по умолчанию
    third_answer = int_answers.get(2, "confidence")  # Значение по умолчанию

    # Получаем рекомендуемый набор
    recommended_set_id = DIAGNOSTIC_LOGIC[first_answer][second_answer][third_answer]
    result = DIAGNOSTIC_RESULTS[recommended_set_id]

    # Находим набор по ID
    shupa_set = next((item for item in SHUPA_SETS if item["id"] == result["set_id"]), None)

    if not shupa_set:
        await query.edit_message_text(
            "Произошла ошибка при определении результата. Попробуйте снова.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(BUTTONS["back"], callback_data='back_to_start')
            ]])
        )
        return

    # Создаем клавиатуру для результата
    keyboard = [
        [InlineKeyboardButton(
            f"Узнать больше о наборе {shupa_set['name']}",
            callback_data=f'view_set_{shupa_set["id"]}'
        )],
        [InlineKeyboardButton(BUTTONS["back"], callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Сохраняем результат диагностики
    db.update_user_data(user_id, "diagnostic_result", recommended_set_id)

    # Показываем результат
    await query.edit_message_text(
        result["text"],
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )