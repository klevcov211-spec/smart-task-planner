import requests
import json
import re


class AIService:
    OLLAMA_URL = "http://localhost:11434/api/generate"

    @staticmethod
    def categorize_task(description: str) -> str:
        """Использует локальную Ollama модель для определения категории"""
        categories = ["работа", "личное", "здоровье", "обучение", "другое"]

        try:
            prompt = f"""Ты помощник для категоризации задач. Определи категорию задачи.

Задача: "{description}"

Правила определения:
- "работа" - задачи связанные с офисом, начальником, отчетом, проектом, дедлайном, клиентом, бизнесом
- "личное" - задачи про дом, семью, друзей, хобби, покупки, отдых
- "здоровье" - задачи про врача, спорт, тренировку, аптеку, больницу
- "обучение" - задачи про учебу, курсы, уроки, экзамены, универ

Ответь ТОЛЬКО одним словом из списка: работа, личное, здоровье, обучение, другое.
Никаких объяснений, только слово."""

            response = requests.post(
                AIService.OLLAMA_URL,
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.1,
                    "max_tokens": 20
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                category = result.get("response", "").strip().lower()

                print(f"AI ответ (категория): {category}")  # Отладка

                # Проверяем точное совпадение
                for cat in categories:
                    if cat == category:
                        return cat
                # Проверяем вхождение
                for cat in categories:
                    if cat in category:
                        return cat
                # Дополнительная проверка по ключевым словам
                if any(w in category for w in ['работ', 'офис', 'начальник', 'отчет', 'проект']):
                    return "работа"
                if any(w in category for w in ['здоров', 'врач', 'спорт', 'трениров']):
                    return "здоровье"
                if any(w in category for w in ['уч', 'курс', 'урок', 'экзамен']):
                    return "обучение"
                if any(w in category for w in ['личн', 'дом', 'семь', 'друг']):
                    return "личное"
                return "другое"
            else:
                print(f"Ollama ошибка: статус {response.status_code}")
                return AIService._fallback_categorize(description)

        except Exception as e:
            print(f"Ollama ошибка: {e}")
            return AIService._fallback_categorize(description)

    @staticmethod
    def estimate_time(description: str) -> int:
        """Использует Ollama для оценки времени"""
        try:
            prompt = f"""Оцени сколько минут займет задача. Учитывай сложность.

Задача: "{description}"

Правила оценки:
- Простые задачи (купить хлеб, позвонить): 5-15 минут
- Средние задачи (собраться, сходить куда-то): 30-60 минут
- Сложные задачи (отчет, проект): 60-120 минут
- Очень сложные задачи: 120-240 минут

Ответь ТОЛЬКО числом от 5 до 240. Без слов, только цифры."""

            response = requests.post(
                AIService.OLLAMA_URL,
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.1,
                    "max_tokens": 20
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                time_str = result.get("response", "").strip()

                print(f"AI ответ (время): {time_str}")  # Отладка

                # Извлекаем число из ответа
                numbers = re.findall(r'\d+', time_str)
                if numbers:
                    minutes = int(numbers[0])
                    return max(5, min(minutes, 240))
                return 30
            else:
                return AIService._fallback_time(description)

        except Exception as e:
            print(f"Ollama ошибка: {e}")
            return AIService._fallback_time(description)

    @staticmethod
    def _fallback_categorize(description: str) -> str:
        """Заглушка если Ollama не работает"""
        text = description.lower()
        if any(w in text for w in
               ['проект', 'отчет', 'работа', 'дедлайн', 'начальник', 'офис', 'клиент', 'бизнес', 'презентация']):
            return "работа"
        if any(w in text for w in
               ['врач', 'спорт', 'тренировка', 'аптека', 'здоровье', 'больница', 'лекарство', 'фитнес']):
            return "здоровье"
        if any(w in text for w in
               ['учить', 'курс', 'урок', 'лекция', 'домашка', 'экзамен', 'универ', 'школа', 'отчет']):
            return "обучение"
        if any(w in text for w in
               ['друг', 'семья', 'родители', 'позвонить', 'встреча', 'кино', 'гулять', 'магазин', 'купить']):
            return "личное"
        return "личное"

    @staticmethod
    def _fallback_time(description: str) -> int:
        """Заглушка времени если Ollama не работает"""
        text = description.lower()
        if any(w in text for w in ['срочно', 'быстро', 'минуту', 'мало']):
            return 10
        if any(w in text for w in ['долго', 'часа', 'сложно', 'много']):
            return 120
        if any(w in text for w in ['проект', 'отчет', 'презентация']):
            return 60
        return 30