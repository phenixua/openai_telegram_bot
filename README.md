.OpenAI Telegram Bot

.Бот на Python для Telegram з інтеграцією OpenAI GPT. Підтримує:

.Квізи

.GPT-чат

.Розмови з відомими особистостями

.Рекомендації (фільми, книги, музика)

.Переклад тексту


📂 Структура проекту

openai_telegram_bot/
├── src/
│   ├── bot.py
│   ├── config.py
│   ├── openapi_client.py
│   ├── utils.py
│   ├── .env.py
│   ├── bot.log
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── callback_handler.py
│   │   ├── gpt_handler.py
│   │   ├── menu_handler.py
│   │   ├── quiz_handler.py
│   │   ├── random_handler.py
│   │   ├── recommend_handler.py
│   │   ├── start_handler.py
│   │   ├── talk_handler.py
│   │   ├── text_handler.py
│   │   └── translate_handler.py
│   ├── logs/
│   │   └── bot.log
│   └── resources/
│       ├── images/
│       │   └── *.jpg
│       ├── messages/
│       │   └── *.txt
│       └── prompts/
│           └── *.txt
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md

🌱 Встановлення

1. Клонувати репозиторій:

git clone <your-repo-url>
cd openai_telegram_bot

2. Створити віртуальне середовище:

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Встановити залежності через Poetry або pip:

poetry install
або
pip install -r requirements.txt

4. Створити файл .env (можна скопіювати .env.example) і додати ключі:

TG_BOT_API_KEY=your_telegram_token
OPENAI_API_KEY=your_openai_key

5. 🚀 Запуск бота

cd src
python bot.py

Бот запуститься і почне приймати команди та повідомлення.

⚙️ Команди
Команда	Опис
/start	Головне меню бота
/random	Випадковий факт
/gpt	GPT-чат
/talk	Розмова з відомими особистостями
/quiz	Квіз
/recommend	Рекомендації фільми/книги/музика
/translate	Перекладач тексту

📝 Режими

GPT – відповіді через OpenAI GPT API

Talk – обираєте особистість, бот відповідає у її стилі

Quiz – інтерактивний квіз

Recommend – рекомендації за жанром

Translate – переклад тексту на англійську, німецьку, українську

⚠️ Примітки

.env обов’язково має містити ключі Telegram та OpenAI.

Не додавайте .env у публічні репозиторії.

Рекомендовано запускати бот у віртуальному середовищі.
