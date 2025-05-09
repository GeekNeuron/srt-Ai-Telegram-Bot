import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from core.translate import translate_srt_file
from core.user import is_valid_user
from utils.logger import setup_logger
from config import Settings
import os

load_dotenv()
logger = setup_logger()

settings = Settings()
bot = Bot(token=settings.telegram_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(msg: Message):
    await msg.answer("Send me a .srt subtitle file and I'll translate it for you.")

@dp.message()
async def handle_docs(msg: Message):
    if not msg.document or not msg.document.file_name.endswith(".srt"):
        await msg.reply("Please upload a valid .srt file.")
        return

    user_id = msg.from_user.id
    if not is_valid_user(user_id):
        await msg.reply("Access denied.")
        return

    try:
        file_info = await bot.get_file(msg.document.file_id)
        input_path = "temp/input.srt"
        await bot.download_file(file_info.file_path, input_path)

        if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
            await msg.reply("Uploaded file is empty or invalid.")
            return

        translated_path = await translate_srt_file(input_path)
        await msg.reply_document(FSInputFile(translated_path))

    except Exception as e:
        logger.exception("Translation error")
        await msg.reply("An unexpected error occurred while translating the subtitle.")

async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Failed to start polling")

if __name__ == '__main__':
    asyncio.run(main())
