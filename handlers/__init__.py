# -*- coding: utf-8 -*-
# Инициализация пакета обработчиков

# Импортируем обработчики из разных модулей
from .start import start_handler, start_callback_handler
from .sets import choose_set_handler, view_set_handler, want_set_handler
from .diagnostic import diagnostic_handler, process_answer_handler, prev_question_handler
from .utils import back_to_start_handler, error_handler

# Словарь с обработчиками для удобного импорта
handlers = {
    "start": start_handler,
    "start_callback": start_callback_handler,
    "choose_set": choose_set_handler,
    "view_set": view_set_handler,
    "want_set": want_set_handler,
    "diagnostic": diagnostic_handler,
    "process_answer": process_answer_handler,
    "prev_question": prev_question_handler,
    "back_to_start": back_to_start_handler,
    "error": error_handler
}