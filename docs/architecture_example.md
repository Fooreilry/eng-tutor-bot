Идея — каждая фича это отдельный модуль
Вместо того чтобы делить по типу файлов (все хендлеры в одной папке, все сервисы в другой) — делишь по функциональности. Каждый модуль полностью самодостаточен.

````
modules/
├── quiz/           ← всё про тест
├── chat/           ← всё про разговор с Alex
├── vocabulary/     ← всё про словарь
└── profile/        ← всё про профиль
````

Структура каждого модуля
````
modules/
└── quiz/
    ├── __init__.py       # экспортирует router наружу
    ├── handler.py        # принимает апдейты от Telegram
    ├── keyboard.py       # кнопки и клавиатуры
    ├── service.py        # бизнес-логика
    ├── states.py         # FSM состояния
    └── repository.py     # запросы к БД (если нужны)
````
Один модуль — одна фича. Всё что нужно для теста лежит в quiz/, ничего лишнего.

Полная структура проекта
````
Bot/
│
├── main.py                  # точка входа — только запуск
│
├── core/                    # общие вещи для всего проекта
│   ├── config.py            # загрузка .env, настройки
│   ├── database.py          # подключение к БД
│   └── gemini.py            # инициализация Gemini клиента
│
├── modules/                 # фичи приложения
│   │
│   ├── quiz/                # тест на определение уровня
│   │   ├── __init__.py
│   │   ├── handler.py
│   │   ├── keyboard.py
│   │   ├── service.py
│   │   ├── states.py
│   │   └── data/
│   │       └── placement_test.json
│   │
│   ├── chat/                # разговор с Alex
│   │   ├── __init__.py
│   │   ├── handler.py
│   │   ├── service.py
│   │   └── prompts.py
│   │
│   ├── vocabulary/          # словарь и карточки
│   │   ├── __init__.py
│   │   ├── handler.py
│   │   ├── keyboard.py
│   │   ├── service.py
│   │   └── repository.py
│   │
│   └── profile/             # профиль пользователя
│       ├── __init__.py
│       ├── handler.py
│       ├── keyboard.py
│       └── repository.py
│
├── tests/
│   ├── test_quiz.py
│   └── test_vocabulary.py
│
├── .env
├── requirements.txt
└── main.py
```