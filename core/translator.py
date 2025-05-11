import aiofiles
import srt
from typing import List, Dict
from aiohttp import ClientSession
from config import Settings
from loguru import logger

settings = Settings()
cache: Dict[str, str] = {}

async def translate_text(session: ClientSession, text: str) -> str:
    if text in cache:
        return cache[text]
    try:
        resp = await session.post(
            url="https://api.gemini.ai/translate",
            json={"text": text, "target_lang": "fa"},
            headers={"Authorization": f"Bearer {settings.gemini_api_key}"}
        )
        resp.raise_for_status()
        data = await resp.json()
        result = data.get("translated", text)
        cache[text] = result
        return result
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text

async def translate_srt_file(input_path: str, output_path: str) -> None:
    async with aiofiles.open(input_path, mode='r', encoding='utf-8') as f:
        data = await f.read()
    try:
        subtitles: List[srt.Subtitle] = list(srt.parse(data))
    except Exception as e:
        logger.error(f"Failed to parse SRT: {e}")
        return

    async with ClientSession() as session:
        for sub in subtitles:
            sub.content = await translate_text(session, sub.content)

    async with aiofiles.open(output_path, mode='w', encoding='utf-8') as f:
        await f.write(srt.compose(subtitles))
