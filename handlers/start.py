# -*- coding: utf-8 -*-
# Обработчики для команды старт и главного меню

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from config import WELCOME_MESSAGE, BUTTONS, States
from database import db


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Обработчик команды /start."""
    # Получаем ID пользователя
    user_id = update.effective_user.id

    # Создаем клавиатуру главного меню
    keyboard = [
        [InlineKeyboardButton(BUTTONS["choose_set"], callback_data='choose_set')],
        [InlineKeyboardButton(BUTTONS["diagnostic"], callback_data='diagnostic')],
        [InlineKeyboardButton(BUTTONS["instructions"], callback_data='instructions')],
        [InlineKeyboardButton(BUTTONS["marathon"], callback_data='marathon')],
        [InlineKeyboardButton(BUTTONS["admin"], callback_data='admin')],
        [InlineKeyboardButton(BUTTONS["about"], callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Сохраняем текущее состояние пользователя
    db.update_user_data(user_id, "state", States.START)

    # Отправляем приветственное сообщение
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    return States.START


async def start_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Обработчик колбэка для возврата в главное меню."""
    query = update.callback_query
    await query.answer()

    # Получаем ID пользователя
    user_id = query.from_user.id

    # Создаем клавиатуру главного меню
    keyboard = [
        [InlineKeyboardButton(BUTTONS["choose_set"], callback_data='choose_set')],
        [InlineKeyboardButton(BUTTONS["diagnostic"], callback_data='diagnostic')],
        [InlineKeyboardButton(BUTTONS["instructions"], callback_data='instructions')],
        [InlineKeyboardButton(BUTTONS["marathon"], callback_data='marathon')],
        [InlineKeyboardButton(BUTTONS["admin"], callback_data='admin')],
        [InlineKeyboardButton(BUTTONS["about"], callback_data='about')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Сохраняем текущее состояние пользователя
    db.update_user_data(user_id, "state", States.START)

    # Обновляем сообщение
    await query.edit_message_text(
        WELCOME_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    return States.START