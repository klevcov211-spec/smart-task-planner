# Smart Task Planner

Планировщик задач с локальным AI (Ollama). AI определяет категорию (работа, личное, здоровье, обучение) и время выполнения.

## Технологии
Python + FastAPI, SQLite, Ollama (llama3.2)

## Установка и запуск

1. Установите Ollama: https://ollama.com/download
2. Скачайте модель: `ollama pull llama3.2`
3. Запустите сервер: `ollama serve`
4. Установите зависимости: `pip install -r requirements.txt`
5. Запустите приложение: `uvicorn app.main:app --reload`
6. Откройте браузер: http://localhost:8000

## Пример
Задача "Сдать отчет начальнику" → категория "работа", время "70 минут"

## Ссылка на репозиторий
https://github.com/klevcov211-spec/smart-task-planner
