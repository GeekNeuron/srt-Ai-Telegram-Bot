# این فایل شامل توابع مربوط به ترجمه و API Gemini است

import aiohttp
import logging
from limiter import RateLimiter, BucketFullException
from typing import Optional, Tuple

translation_cache: Dict[Tuple[str, str, str, str], str] = {}  # (text, source_lang, target_lang, style) -> translated_text
limiter = RateLimiter(max_calls=5, period=10)

async def validate_gemini_api_key(api_key: str, session: aiohttp.ClientSession) -> bool:
    """
    بررسی اعتبار API Key.
    """
    url = "https://generative-ai-service-endpoint/test"
    headers = {"Content-Type": "application/json"}
    data = {"api_key": api_key}
    try:
        # استفاده از HTTPS
        async with session.post(url, headers=headers, json=data, timeout=5, ssl=True) as response:
            response.raise_for_status()
            return True
    except aiohttp.ClientError as e:
        logging.error(f"خطا در اعتبارسنجی API Key: {e}")
        return False

async def translate_text(text: str, source_language: str, target_language: str, gemini_api_key: str, translation_style: str, session: aiohttp.ClientSession) -> Optional[str]:
    """
    ترجمه متن با استفاده از API Gemini و Caching.
    """
    cache_key = (text, source_language, target_language, translation_style)

    # بررسی Cache
    if cache_key in translation_cache:
        logging.info("استفاده از ترجمه موجود در Cache.")
        return translation_cache[cache_key]

    url = "https://generative-ai-service-endpoint"
    headers = {"Content-Type": "application/json"}
    data = {
        "text": text,
        "target_language": target_language,
        "api_key": gemini_api_key,
        "style": translation_style,
    }

    try:
        try:
            with limiter:
                # استفاده از HTTPS
                async with session.post(url, headers=headers, json=data, timeout=10, ssl=True) as response:
                    response.raise_for_status()
                    json_response = await response.json()  # دریافت پاسخ JSON
                    translation = json_response.get("translated_text") # استفاده از get برای جلوگیری از KeyError
                    if not translation:
                        logging.warning("پاسخ API ترجمه فاقد فیلد 'translated_text' است.")
                        return None

                    # ذخیره در Cache
                    translation_cache[cache_key] = translation
                    logging.info("ترجمه جدید در Cache ذخیره شد.")
                    return translation
        except BucketFullException:
            logging.warning("محدودیت درخواست به API Gemini رد شد (Rate Limit).")
            return None
    except aiohttp.ClientError as e:
        logging.error(f"خطا در درخواست ترجمه به Gemini: {e}")
        return None
    except (KeyError, ValueError) as e:
        logging.error(f"خطا در پردازش پاسخ Gemini: {e}")
        return None
