# Alex Bot

Telegram-бот репетитор по английскому языку с AI-компаньоном Alex — 22-летний американец из Нью-Йорка. Целевая аудитория: молодёжь 16–28 лет, уровень A1–B2.

## Стек технологий

| Технология | Назначение |
|---|---|
| Python 3.11 | Основной язык |
| aiogram 3 | Telegram бот (async) |
| FastAPI | REST API для Mini App |
| google-genai | Gemini AI (персонаж Alex) |
| aiosqlite | Асинхронная БД SQLite |
| Docker | Контейнеризация |

## Структура проекта

```
├── main.py              # Точка входа — запуск Telegram бота
├── Bot/                 # Telegram бот
│   ├── handlers/        # Обработчики команд и сообщений
│   │   └── acquaintance.py  # /start и онбординг
│   └── states.py        # FSM состояния диалога
├── API/                 # FastAPI сервер для Mini App
│   └── server.py        # FastAPI приложение
├── Gemini/              # Интеграция с Google Gemini
│   └── client.py        # Инициализация Gemini клиента
├── DB/                  # База данных (SQLite)
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── .env                 # Переменные окружения (не в git)
```

## Быстрый старт

### Предварительные требования

- [Docker](https://docs.docker.com/get-docker/) и Docker Compose
- Telegram Bot Token ([BotFather](https://t.me/BotFather))
- Google Gemini API Key ([AI Studio](https://aistudio.google.com/))

### 1. Клонировать репозиторий

```bash
git clone <url-репозитория>
cd pythonProject
```

### 2. Создать файл `.env`

```bash
cp .env.example .env
```

Заполнить переменные:

```env
T_BOT_KEY=токен_от_BotFather
GEMINI_KEY=ключ_от_aistudio
```

### 3. Запустить контейнеры

```bash
docker compose up -d --build
```

Эта команда соберёт образы и запустит два сервиса:
- **bot** — Telegram бот (polling)
- **api** — FastAPI сервер на `http://localhost:8000`

## Управление контейнерами

```bash
# Запустить все сервисы
docker compose up -d

# Пересобрать и запустить (после изменения зависимостей)
docker compose up -d --build

# Остановить все сервисы
docker compose down

# Посмотреть логи всех сервисов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f bot
docker compose logs -f api

# Перезапустить конкретный сервис
docker compose restart bot

# Статус контейнеров
docker compose ps
```

## Локальная разработка без Docker

```bash
# Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt

# Запустить бота
python main.py

# Запустить API сервер (отдельный терминал)
uvicorn API.server:api --reload
```

## Переменные окружения

| Переменная | Описание |
|---|---|
| `T_BOT_KEY` | Токен Telegram бота от BotFather |
| `GEMINI_KEY` | API ключ Google Gemini |
