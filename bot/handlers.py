from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart
from core.translator import translate_srt_file
from core.utils import is_valid_user
import os

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Welcome! Send me a `.srt` subtitle file to translate it using AI.")

@router.message()
async def file_handler(message: types.Message):
    if not message.document or not message.document.file_name.endswith(".srt"):
        await message.reply("Please send a valid `.srt` subtitle file.")
        return

    user_id = message.from_user.id
    if not is_valid_user(user_id):
        await message.reply("You are not authorized to use this bot.")
        return

    input_path = f"temp/{message.document.file_unique_id}.srt"
    output_path = f"temp/output_{message.document.file_unique_id}.srt"

    file_info = await message.bot.get_file(message.document.file_id)
    await message.bot.download_file(file_info.file_path, input_path)

    if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
        await message.reply("The file is empty or invalid.")
        return

    await translate_srt_file(input_path, output_path)
    await message.reply_document(FSInputFile(output_path))
