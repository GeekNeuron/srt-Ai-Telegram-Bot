import os
import string
from dotenv import load_dotenv

# -------------------------- ثابت‌ها --------------------------
DEFAULT_LANGUAGE = "en"
DEFAULT_DAILY_COUPON_COUNT = 10
REFERRAL_COUPON_REWARD = 5
PAID_PLAN_PRICE = 100000
PAID_PLAN_DAILY_COUPON_COUNT = 100
PAID_PLAN_DURATION = 30
USER_DATA_FILE = "user_data.json"
MAX_QUEUE_SIZE_FREE = 20
MAX_QUEUE_SIZE_PAID = 60
DATA_SAVE_INTERVAL = 60  # ذخیره اطلاعات هر 60 ثانیه

# -------------------------- لیست سفید کاراکترهای مجاز برای نام فایل --------------------------
ALLOWED_CHARACTERS_FILENAME = string.ascii_letters + string.digits + "_"

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

        if not self.TELEGRAM_BOT_TOKEN or not self.GEMINI_API_KEY or not self.MANAGER_ID:
            print("خطا: متغیرهای محیطی TELEGRAM_BOT_TOKEN، GEMINI_API_KEY و MANAGER_ID باید تنظیم شوند.")
            exit()
