# -*- coding: utf-8 -*-
# Конфигурация бота

# Токен бота
BOT_TOKEN = "8147762356:AAEOn8Z4b5IZq_f5N5yFG98YLLJkTH0Sc8g"

# Параметры для текстовых сообщений
WELCOME_MESSAGE = """
✨ *Добро пожаловать в мир Шуп* ✨

Ты не случайно оказался здесь...

Мистические силы привели тебя к порталу глубинных трансформаций. 
Шупа - это древний код земли, помогающий раскрыть скрытые возможности твоего сознания.

Выбери, куда направить свой путь:
"""

# Названия кнопок и разделов
BUTTONS = {
    "choose_set": "🔮 Выбрать набор Шуп",
    "diagnostic": "✨ Пройти диагностику",
    "instructions": "📜 Инструкция и Ритуалы",
    "marathon": "🌙 Марафон Шуп 60 дней",
    "admin": "👤 Связь с Админом",
    "about": "🧿 О Шупах и их Силе",
    "back": "◀️ Назад",
    "more_info": "📖 Подробнее",
    "want_this": "💫 Хочу этот набор",
    "next_question": "➡️ Далее",
    "show_result": "🔮 Показать результат",
    "write_admin": "✉️ Написать Админу",
    "want_consultation": "🧙‍♂️ Хочу консультацию"
}


# Состояния для FSM
class States:
    START = "start"
    CHOOSING_SET = "choosing_set"
    VIEWING_SET = "viewing_set"
    DIAGNOSTIC = "diagnostic"
    DIAGNOSTIC_RESULT = "diagnostic_result"
    INSTRUCTIONS = "instructions"
    MARATHON = "marathon"
    ADMIN = "admin"
    ABOUT = "about"


# Настройки медиа-файлов
MEDIA_PATH = "media/"
PHOTOS_PATH = f"{MEDIA_PATH}photos/"
