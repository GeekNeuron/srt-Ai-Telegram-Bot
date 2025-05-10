# Telegram Subtitle Translator Bot

A fully async, AI-powered Telegram bot that translates `.srt` subtitle files using Gemini API. Built with performance, security, and scalability in mind.

## Features

- Upload `.srt` files via Telegram and receive fully translated subtitles
- Powered by Gemini AI for fast and intelligent translation
- Asynchronous architecture using `aiogram`
- Auto validation for subtitle file structure and input size
- Error logging with `loguru`
- Configurable via `.env` file with secure variable loading via `pydantic`
- In-memory translation cache to avoid redundant API calls and reduce cost
- Modular, clean codebase for future extensibility

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Telegram-Sub-Translate-Ai
cd Telegram-Sub-Translate-Ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
MANAGER_ID=your_numeric_telegram_id
BOT_USERNAME=your_bot_username
```

### 4. Run the bot
```bash
python bot.py
```

## File Structure
```
Telegram-Sub-Translate-Ai/
├── bot.py
├── config.py
├── requirements.txt
├── README.md
├── .env
├── core/
│   └── translate.py
├── utils/
│   └── logger.py (optional)
├── temp/
```

## License
MIT License © 2025 GeekNeuron
