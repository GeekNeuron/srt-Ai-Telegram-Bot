# این فایل شامل توابع مربوط به مدیریت اطلاعات کاربر (load/save) است

import json
import logging
import uuid
import datetime
import os
from typing import Dict, Any
from telebot import TeleBot
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# -------------------------- تنظیمات Logging --------------------------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------- بارگیری تنظیمات --------------------------
load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MANAGER_ID = os.environ.get("MANAGER_ID")
DEFAULT_LANGUAGE = "en"
DEFAULT_DAILY_COUPON_COUNT = 10
REFERRAL_COUPON_REWARD = 5
PAID_PLAN_PRICE = 100000
PAID_PLAN_DAILY_COUPON_COUNT = 100
PAID_PLAN_DURATION = 30
USER_DATA_FILE = "user_data.json"
DATA_SAVE_INTERVAL = 60  # ذخیره اطلاعات هر 60 ثانیه
BOT_USERNAME = os.environ.get("BOT_USERNAME")

bot = TeleBot(TELEGRAM_BOT_TOKEN)

# -------------------------- کلاس تنظیمات --------------------------
class BotSettings:
    """
    کلاس تنظیمات ربات.
    """
    def __init__(self):
        load_dotenv()
        self.TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        self.MANAGER_ID = os.environ.get("MANAGER_ID")  # اضافه کردن ID مدیر
        self.DEFAULT_LANGUAGE = DEFAULT_LANGUAGE
        self.DEFAULT_DAILY_COUPON_COUNT = DEFAULT_DAILY_COUPON_COUNT
        self.REFERRAL_COUPON_REWARD = REFERRAL_COUPON_REWARD
        self.PAID_PLAN_PRICE = PAID_PLAN_PRICE
        self.PAID_PLAN_DAILY_COUPON_COUNT = PAID_PLAN_DAILY_COUPON_COUNT
        self.PAID_PLAN_DURATION = PAID_PLAN_DURATION
        self.LANGUAGES = {
            "en": "English",
            "ru": "Russian",
            "tr": "Turkish",
            "fa": "Persian",
            "hi": "Hindi",
            "es": "Spanish",
            "zh-CN": "Chinese (Simplified)"
        }
        self.TRANSLATION_LANGUAGES = {
            "en": "English",
            "ru": "Russian",
            "tr": "Turkish",
            "fa": "Persian",
            "hi": "Hindi",
            "es": "Spanish",
            "zh-CN": "Chinese (Simplified)"
        }
        self.TRANSLATION_STYLES = {
            "formal": "رسمی",
            "eloquent": "فصیح",
            "conversational": "محاوره ای",
            "technical": "علمی-تخصصی",
            "strict": "سخت"
        }
        self.BOT_USERNAME = BOT_USERNAME

        if not self.TELEGRAM_BOT_TOKEN or not self.GEMINI_API_KEY or not self.MANAGER_ID:
            print("خطا: متغیرهای محیطی TELEGRAM_BOT_TOKEN، GEMINI_API_KEY و MANAGER_ID باید تنظیم شوند.")
            exit()

# -------------------------- رمزنگاری API --------------------------
def generate_encryption_key() -> bytes:
    """
    تولید یک کلید رمزنگاری Fernet.
    """
    return Fernet.generate_key()

# تولید کلید رمزنگاری
ENCRYPTION_KEY = generate_encryption_key()

def encrypt_api_key(api_key: str, encryption_key: bytes) -> str:
    """
    رمزنگاری API Key با استفاده از Fernet.
    """
    f = Fernet(encryption_key)
    api_key_bytes = api_key.encode('utf-8')
    encrypted_api_key_bytes = f.encrypt(api_key_bytes)
    return encrypted_api_key_bytes.decode('utf-8')

def decrypt_api_key(encrypted_api_key: str, encryption_key: bytes) -> str:
    """
    رمزگشایی API Key رمزنگاری شده با Fernet.
    """
    try:
        f = Fernet(encryption_key)
        encrypted_api_key_bytes = encrypted_api_key.encode('utf-8')
        api_key_bytes = f.decrypt(encrypted_api_key_bytes)
        return api_key_bytes.decode('utf-8')
    except Exception as e:
        logging.error(f"خطا در رمزگشایی API Key: {e}")
        return ""

user_data: Dict[str, Dict[str, Any]] = {}  # Type Hint برای user_data

def _load_user_data() -> Dict[str, Dict[str, Any]]:
    """
    داخلی: بارگیری اطلاعات کاربر از فایل JSON.
    """
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"خطا در بارگیری اطلاعات کاربر (JSON Decode): {e}")
        return {}
    except Exception as e:
        logging.exception(f"خطا در بارگیری اطلاعات کاربر: {e}")
        return {}

def _save_user_data(data: Dict[str, Dict[str, Any]]) -> None:
    """
    داخلی: ذخیره اطلاعات کاربر در فایل JSON.
    """
    try:
        with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.exception(f"خطا در ذخیره اطلاعات کاربر: {e}")

def load_user_data() -> None:
    """
    بارگیری اطلاعات کاربر (با رعایت محدودیت دسترسی).
    """
    global user_data
    user_data = _load_user_data()
    # رمزگشایی API Key ها بعد از بارگیری
    for user_id, data in user_data.items():
        encrypted_api_key = data.get("gemini_api_key")
        if encrypted_api_key:
            data["gemini_api_key"] = decrypt_api_key(encrypted_api_key, ENCRYPTION_KEY)

def save_user_data() -> None:
    """
    ذخیره اطلاعات کاربر (با رعایت محدودیت دسترسی).
    """
    # رمزنگاری API Key ها قبل از ذخیره
    temp_data = {}
    for user_id, data in user_data.items():
        temp_data[user_id] = data.copy()  # ایجاد کپی برای جلوگیری از تغییرات ناخواسته
        api_key = temp_data[user_id].get("gemini_api_key")
        if api_key:
            temp_data[user_id]["gemini_api_key"] = encrypt_api_key(api_key, ENCRYPTION_KEY)

    _save_user_data(temp_data)

load_user_data()

def reset_daily_coupons(chat_id: str, bot_settings: BotSettings = None) -> None:
    """
    بازنشانی تعداد کوپن روزانه کاربر (با توجه به پلن پولی).
    """
    now = datetime.datetime.now()
    if chat_id not in user_data:
        logging.warning(f"کاربر {chat_id} در user_data یافت نشد.")
        return

    user_data_record = user_data[chat_id]

    bot_settings = BotSettings()

    # بررسی پلن پولی
    if is_paid_plan_active(chat_id):
        user_data_record["daily_coupons"] = bot_settings.PAID_PLAN_DAILY_COUPON_COUNT
    else:
        user_data_record["daily_coupons"] = bot_settings.DEFAULT_DAILY_COUPON_COUNT

    user_data_record["last_reset"] = now.strftime("%Y-%m-%d")  # ذخیره تاریخ بازنشانی
    save_user_data()
    logging.info(f"تعداد کوپن روزانه کاربر {chat_id} بازنشانی شد.")

def reset_all_daily_coupons(bot_settings: BotSettings = None) -> None:
    """
    بازنشانی تعداد کوپن روزانه تمامی کاربران.
    """
    now = datetime.datetime.now()
    for user_id, user_data_record in user_data.items():
        # بررسی آخرین زمان بازنشانی
        last_reset = user_data_record.get("last_reset")
        if last_reset:
            try:
                last_reset_date = datetime.datetime.strptime(last_reset, "%Y-%m-%d")
            except ValueError:
                logging.error(f"فرمت تاریخ last_reset برای کاربر {user_id} نامعتبر است.")
                continue
            if last_reset_date.date() == now.date():
                continue  # اگر امروز بازنشانی شده، رد شود

        # بازنشانی تعداد کوپن (با توجه به پلن پولی)
        reset_daily_coupons(user_id, None)
    save_user_data()
    logging.info("تعداد کوپن روزانه تمامی کاربران بازنشانی شد.")

def is_paid_plan_active(chat_id: str) -> bool:
    """
    بررسی می‌کند آیا کاربر پلن پولی فعال دارد یا خیر.
    """
    if chat_id not in user_data:
        return False

    user_data_record = user_data[chat_id]
    plan_expiry = user_data_record.get("plan_expiry")
    if not plan_expiry:
        return False

    try:
        expiry_date = datetime.datetime.strptime(plan_expiry, "%Y-%m-%d")
    except ValueError:
        logging.error(f"فرمت تاریخ plan_expiry برای کاربر {chat_id} نامعتبر است.")
        return False
    return expiry_date > datetime.datetime.now()

def can_use_coupon(chat_id: str) -> Tuple[bool, Optional[str]]:
    """
    بررسی می‌کند آیا کاربر می‌تواند از کوپن استفاده کند یا خیر.
    """
    # بازنشانی کوپن ها اگر روز جدیدی باشد
    bot_settings = BotSettings()
    reset_daily_coupons(chat_id, bot_settings)
    load_user_data() # بارگذاری مجدد برای اعمال تغییرات

    if chat_id not in user_data:
        return False, "متاسفم، کاربر یافت نشد."

    user_coupons = user_data[chat_id]
    total_coupons = user_coupons.get("daily_coupons", 0) + user_coupons.get("bonus_coupons", 0)
    if total_coupons <= 0:
        return False, "متاسفم، شما کوپن کافی برای استفاده ندارید.\n\n" + f"برای دریافت {PAID_PLAN_DAILY_COUPON_COUNT} کوپن روزانه، [پلن پولی]({PAID_PLAN_PRICE} تومان) را خریداری کنید."

    return True, None

def use_coupon(chat_id: str) -> None:
    """
    یک کوپن از کاربر کم می‌کند (ابتدا کوپن‌های روزانه، سپس کوپن‌های جایزه).
    """
    if chat_id not in user_data:
        logging.warning(f"کاربر {chat_id} در user_data یافت نشد.")
        return

    user_coupons = user_data[chat_id]
    if user_coupons["daily_coupons"] > 0:
        user_coupons["daily_coupons"] -= 1
    elif user_coupons["bonus_coupons"] > 0:
        user_coupons["bonus_coupons"] -= 1
    save_user_data()

def load_user_data_sync() -> Dict[str, Any]:
    """
    بارگیری اطلاعات کاربر به صورت همزمان (Synchronous) - برای جلوگیری از مشکلات Async.
    """
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"خطا در بارگیری اطلاعات کاربر (همزمان - JSON Decode): {e}")
        return {}
    except Exception as e:
        logging.exception(f"خطا در بارگیری اطلاعات کاربر (همزمان): {e}")
        return {}

def report_error_to_manager(error_message: str, bot_settings: BotSettings = None) -> None:
    """
    ارسال گزارش خطا به مدیر ربات.
    """
    bot_settings = BotSettings()
    manager_id = bot_settings.MANAGER_ID
    try:
        bot.send_message(manager_id, f"**گزارش خطا:**\n{error_message}", parse_mode="Markdown")
        logging.info(f"گزارش خطا به مدیر {manager_id} ارسال شد.")
    except Exception as e:
        logging.error(f"خطا در ارسال گزارش خطا به مدیر: {e}")

import asyncio
async def periodic_data_save():
    """
    ذخیره دوره ای اطلاعات کاربر.
    """
    while True:
        from .data_utils import DATA_SAVE_INTERVAL
        await asyncio.sleep(DATA_SAVE_INTERVAL)
        logging.info("ذخیره دوره ای اطلاعات کاربر...")
        save_user_data()
        logging.info("ذخیره دوره ای اطلاعات کاربر با موفقیت انجام شد.")
