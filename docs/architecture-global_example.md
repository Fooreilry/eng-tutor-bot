````
alex_bot/
│
├── core/                        # всё общее для всего проекта
│   ├── config.py                # настройки, .env
│   ├── database.py              # engine, Base, init_db
│   └── middleware.py            # DatabaseMiddleware для бота
│
│
│
│
├── gemini/                          # всё про Gemini
│   ├── __init__.py
│   ├── client.py                # инициализация клиента — один раз
│   ├── base.py                  # базовый класс с общими методами
│   ├── prompts/                     # все промпты отдельно
│   │   ├── __init__.py
│   │   ├── alex.py                  # системный промпт Alex
│   │   ├── vocabulary.py            # промпт карточки слова
│   │   ├── quiz.py                  # промпты для упражнений
│   ├── agents/                  # отдельный агент для каждой фичи
│      ├── chat_agent.py        # агент разговора с Alex
│      ├── vocabulary_agent.py  # агент генерации карточек
│      └── quiz_agent.py        # агент проверки ответов
│
├── models/                      # SQLAlchemy модели — отдельный слой
│   ├── __init__.py
│   ├── user.py                  # User
│   ├── vocabulary.py            # VocabularyItem
│   └── chat_memory.py           # ChatMemory
│
├── repositories/                # только работа с БД
│   ├── __init__.py
│   ├── base.py                  # базовый репозиторий с общими методами
│   ├── user_repository.py
│   └── vocabulary_repository.py
│
├── services/                    # бизнес-логика — используется и ботом и API
│   ├── __init__.py
│   ├── vocabulary_service.py
│   ├── quiz_service.py
│   └── chat_service.py
│
├── bot/                         # всё про Telegram бота
│   ├── __init__.py
│   ├── main.py                  # запуск бота
│   ├── middleware.py            # bot-specific middleware
│   └── modules/                 # фичи бота
│       ├── start/
│       │   ├── handler.py
│       │   └── keyboard.py
│       ├── quiz/
│       │   ├── handler.py
│       │   ├── keyboard.py
│       │   └── states.py
│       ├── vocabulary/
│       │   ├── handler.py
│       │   ├── keyboard.py
│       │   └── states.py
│       └── chat/
│           ├── handler.py
│           └── states.py
│
├── api/                         # FastAPI для Mini App
│   ├── __init__.py
│   ├── main.py                  # запуск API
│   ├── dependencies.py          # get_session, verify_auth — общие зависимости
│   ├── middleware.py            # CORS и прочее
│   └── routes/                  # эндпоинты
│       ├── __init__.py
│       ├── vocabulary.py
│       ├── profile.py
│       └── stats.py
│
├── schemas/                     # Pydantic схемы для API запросов/ответов
│   ├── __init__.py
│   ├── vocabulary.py
│   └── user.py
│
├── miniapp/                     # React приложение
│   ├── src/
│   └── package.json
│
├── tests/
│   ├── test_services/
│   └── test_api/
│
├── main.py                      # главная точка входа — запускает и бот и API
├── .env
└── requirements.txt
````