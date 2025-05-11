# 🎬 srt-Ai-Telegram-Bot

A fully asynchronous Telegram bot that translates `.srt` subtitle files using the Gemini AI API. Designed with performance, security, and scalability in mind.

## ✨ Features

- Upload `.srt` files via Telegram and receive translated subtitles.
- Powered by Gemini AI for intelligent and context-aware translations.
- Asynchronous architecture using `aiogram`.
- Automatic validation for subtitle file structure and input size.
- Error logging with `loguru`.
- Configurable via `.env` file with secure variable loading using `pydantic`.
- In-memory translation cache to avoid redundant API calls and reduce costs.
- Modular, clean codebase for future enhancements.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token
- Gemini AI API Key

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/GeekNeuron/srt-Ai-Telegram-Bot.git
   cd srt-Ai-Telegram-Bot
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add the following variables:

   ```env
   BOT_TOKEN=your_telegram_bot_token
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. Run the bot:

   ```bash
   python bot.py
   ```

## 🛠 Usage

1. Start the bot on Telegram.
2. Send a `.srt` subtitle file to the bot.
3. Receive the translated subtitle file in response.

## 📁 Project Structure

```
srt-Ai-Telegram-Bot/
├── bot/
│   └── handlers.py
├── core/
│   ├── translator.py
│   └── utils.py
├── .env.example
├── bot.py
├── config.py
├── requirements.txt
└── README.md
```

## 📄 License

This project is licensed under the MIT License.
