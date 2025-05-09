# این فایل شامل توابع مربوط به پردازش فایل SRT است

import re
import logging
import aiohttp
from typing import Optional
from .translation_utils import translate_text
from ..models.srt_file_handler import SrtFileHandler  # اضافه کردن import

async def translate_srt_file(srt_file_handler: SrtFileHandler, source_language: str, target_language: str, gemini_api_key: str, translation_style: str, chat_id: str, session: aiohttp.ClientSession) -> Optional[str]:
    """
    ترجمه فایل SRT.
    """
    srt_content = srt_file_handler.read_file_content()
    if not srt_content:
        return None

    # استفاده از regular expression برای استخراج متن زیرنویس (بهینه‌سازی شده)
    subtitle_texts = re.findall(r"^(?:\d+\n[\d:,]+\s-->\s[\d:,]+\n)(.*?)(?=\n\d+|$)", srt_content, re.MULTILINE | re.DOTALL)

    if not subtitle_texts:
        logging.warning("فایل SRT فاقد متن زیرنویس است.")
        return None

    all_text = "\n".join(subtitle_texts)
    translated_all_text = await translate_text(
        all_text, source_language, target_language, gemini_api_key, translation_style, session
    )

    if not translated_all_text:
        logging.warning("ترجمه یکپارچه متن زیرنویس با خطا مواجه شد.")
        return None

    translated_lines = translated_all_text.splitlines()

    # بازسازی فایل SRT ترجمه شده
    translated_srt = ""
    index = 0
    line_index = 0
    for match in re.finditer(r"^(\d+)\n([\d:,]+\s-->\s[\d:,]+)\n(.*?)(?=\n\d+|$)", srt_content, re.MULTILINE | re.DOTALL):
        index =+ 1
        line_number, timeline, original_text = match.groups()
        try:
            translated_text = translated_lines[line_index]
            line_index += 1
        except IndexError:
            translated_text = ""  # اگر متن ترجمه شده کافی نیست

        translated_srt += f"{line_number}\n{timeline}\n{translated_text}\n\n"

    return translated_srt

def format_srt_for_instant_view(srt_string: str) -> str:
    """
    فرمت‌بندی فایل SRT برای نمایش در Instant View تلگرام.
    """
    html_text = "<pre style='font-family: monospace;'>"
    for line in srt_string.splitlines():
        if line.isdigit():
            html_text += f"<b style='color: #007BFF;'>{line}</b>\n"
        elif "-->" in line:
            html_text += f"<code style='color: #6C757D;'>{line}</code>\n"
        elif line:
            html_text += f"<span>{line}</span>\n"
        else:
            html_text += "\n"

    html_text += "</pre>"
    return html_text

def split_text_into_chunks(text: str, chunk_size: int = 4096) -> list[str]:
    """
    تقسیم متن به قطعات کوچکتر برای ارسال در تلگرام.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
