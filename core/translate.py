import os
import aiofiles
import srt
import asyncio
from typing import List, Dict
from aiohttp import ClientSession
from config import Settings
from utils.logger import setup_logger

logger = setup_logger()
settings = Settings()

_translation_cache: Dict[str, str] = {}

async def translate_text(session: ClientSession, text: str) -> str:
    if text in _translation_cache:
        logger.debug("Cache hit for text chunk.")
        return _translation_cache[text]

    try:
        response = await session.post(
            "https://api.gemini.ai/translate",
            json={"text": text, "target_lang": "fa"},
            headers={"Authorization": f"Bearer {settings.gemini_api_key}"}
        )
        response.raise_for_status()
        data = await response.json()
        translated = data.get("translated", text)
        _translation_cache[text] = translated
        return translated
    except Exception as e:
        logger.error(f"Translation failed for chunk: {text[:30]}... | Error: {e}")
        return text

async def translate_srt_file(file_path: str) -> str:
    output_path = "temp/output.srt"
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
        srt_data = await f.read()

    try:
        subtitles: List[srt.Subtitle] = list(srt.parse(srt_data))
    except Exception as e:
        logger.error(f"Invalid SRT file structure: {e}")
        raise

    async with ClientSession() as session:
        for subtitle in subtitles:
            subtitle.content = await translate_text(session, subtitle.content)

    translated_srt = srt.compose(subtitles)
    async with aiofiles.open(output_path, mode='w', encoding='utf-8') as f:
        await f.write(translated_srt)

    return output_path
