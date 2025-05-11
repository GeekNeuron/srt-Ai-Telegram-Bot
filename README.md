# 🚀 AI-Powered Telegram Subtitle Translator Bot

This project is a production-ready, scalable, and secure Telegram bot built to translate `.srt` subtitle files using Gemini AI. Designed with microservices architecture and full support for asynchronous tasks, caching, monitoring, and more.

---

## ✨ Features

- Translate `.srt` subtitle files using Gemini AI API.
- Async architecture with `aiogram` and `aiohttp`.
- Redis caching to reduce repeated API calls.
- Task queue system powered by `Celery`.
- SQLite/PostgreSQL database for persistent user storage.
- Monitoring support with Prometheus and Grafana.
- Linted, formatted, and fully documented codebase.
- Automated unit testing using `pytest`.

---

## 🧰 Requirements

- Python >= 3.8
- Redis
- Celery
- Docker & Docker Compose (optional for full setup)

---

## 🛠 Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/YourUsername/srt-Ai-Telegram-Bot.git
cd srt-Ai-Telegram-Bot
```

### 2. Create virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create `.env` file
```env
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
REDIS_URL=redis://localhost:6379
```

### 4. Initialize database
```bash
python create_db.py
```

### 5. Run services

**Worker:**
```bash
celery -A worker.celery_app worker --loglevel=info
```

**Bot:**
```bash
python bot.py
```

**Prometheus Metrics (Optional):**
Runs on port `8000`.

---

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Lint and format:
```bash
flake8 .
black .
```

---

## 🐳 Docker Support

To run all services via Docker:
```bash
docker-compose up --build
```

---

## 📈 Monitoring

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default login: admin/admin)

---

## 📁 Project Structure
```
├── bot_service/         # Telegram interaction logic
├── core/                # Translation, utils, DB, tasks
├── tests/               # Unit tests with pytest
├── db.py                # SQLAlchemy async DB setup
├── worker.py            # Celery app instance
├── create_db.py         # Script to initialize tables
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Multi-service container config
└── .env.example         # Env var sample
```

---

## 📜 License

MIT License © 2024 GeekNeuron
