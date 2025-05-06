# -*- coding: utf-8 -*-
# Простая база данных для хранения состояний пользователей

import os
import json
from typing import Dict, Any, List, Optional

# Класс для работы с данными пользователей
class UserDatabase:
    def __init__(self, db_file: str = "user_data.json"):
        """Инициализация базы данных пользователей."""
        self.db_file = db_file
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Загрузка данных из файла."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_data(self) -> None:
        """Сохранение данных в файл."""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Получение данных пользователя по ID."""
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            self.data[user_id_str] = {}
        return self.data[user_id_str]

    def update_user_data(self, user_id: str, key: str, value: Any) -> None:
        """Обновление данных пользователя."""
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            self.data[user_id_str] = {}
        self.data[user_id_str][key] = value
        self._save_data()

    def clear_user_data(self, user_id: str) -> None:
        """Очистка данных пользователя."""
        user_id_str = str(user_id)
        if user_id_str in self.data:
            self.data[user_id_str] = {}
            self._save_data()

    def get_diagnostic_state(self, user_id: str) -> Dict[str, Any]:
        """Получение состояния диагностики пользователя."""
        user_data = self.get_user_data(user_id)
        if "diagnostic" not in user_data:
            user_data["diagnostic"] = {
                "answers": {},
                "current_question": 0
            }
            self._save_data()
        return user_data["diagnostic"]

    def update_diagnostic_answer(self, user_id: str, question_idx: int, answer: str) -> None:
        """Обновление ответа пользователя на вопрос диагностики."""
        diagnostic = self.get_diagnostic_state(user_id)
        diagnostic["answers"][str(question_idx)] = answer
        diagnostic["current_question"] = question_idx + 1
        self.update_user_data(user_id, "diagnostic", diagnostic)

    def reset_diagnostic(self, user_id: str) -> None:
        """Сброс диагностики пользователя."""
        self.update_user_data(user_id, "diagnostic", {
            "answers": {},
            "current_question": 0
        })

    def get_viewed_sets(self, user_id: str) -> List[str]:
        """Получение списка просмотренных наборов."""
        user_data = self.get_user_data(user_id)
        if "viewed_sets" not in user_data:
            user_data["viewed_sets"] = []
            self._save_data()
        return user_data["viewed_sets"]

    def add_viewed_set(self, user_id: str, set_id: str) -> None:
        """Добавление набора в список просмотренных."""
        viewed_sets = self.get_viewed_sets(user_id)
        if set_id not in viewed_sets:
            viewed_sets.append(set_id)
            self.update_user_data(user_id, "viewed_sets", viewed_sets)

    def get_user_orders(self, user_id: str) -> List[Dict[str, Any]]:
        """Получение списка заказов пользователя."""
        user_data = self.get_user_data(user_id)
        if "orders" not in user_data:
            user_data["orders"] = []
            self._save_data()
        return user_data["orders"]

    def add_order(self, user_id: str, set_id: str) -> None:
        """Добавление заказа пользователя."""
        orders = self.get_user_orders(user_id)
        import datetime
        orders.append({
            "set_id": set_id,
            "date": datetime.datetime.now().isoformat(),
            "status": "new"
        })
        self.update_user_data(user_id, "orders", orders)

# Создаем экземпляр базы данных
db = UserDatabase()