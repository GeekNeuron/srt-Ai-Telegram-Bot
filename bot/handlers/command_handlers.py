import telebot
import uuid
from ..utils import data_utils
from ..utils.security_utils import encrypt_api_key, decrypt_api_key
from ..config import BotSettings
from ..models.translation_request import TranslationRequest

user_data: Dict[str, Dict[str, Any]] = {}  # Type Hint برای user_data

def register_handlers(bot: telebot.TeleBot, settings: BotSettings):
    @bot.message_handler(commands=["start", "help", "coupons", "buy_plan", "suggest", "contact"])
    def send_welcome(message: telebot.types.Message, bot_settings: BotSettings = settings) -> None:
        """
        نمایش پیام خوشامدگویی، راهنما، لینک معرفی، اطلاعات پلن پولی، پیشنهادات/اسپانسری و ارتباط با مدیر.
        """
        chat_id = str(message.chat.id)
        
        from ..utils.data_utils import is_paid_plan_active, reset_daily_coupons, save_user_data, load_user_data

        # اگر کاربر جدید است، ایجاد اطلاعات اولیه
        if chat_id not in user_data:
            # رمزنگاری API Key قبل از ذخیره
            encrypted_api_key = ""
            if bot_settings.GEMINI_API_KEY:
                encrypted_api_key = encrypt_api_key(bot_settings.GEMINI_API_KEY, ENCRYPTION_KEY)

            user_data[chat_id] = {
                "language": bot_settings.DEFAULT_LANGUAGE,
                "translation_language": bot_settings.DEFAULT_LANGUAGE,
                "translation_style": "formal",
                "daily_coupons": bot_settings.DEFAULT_DAILY_COUPON_COUNT,  # کوپن‌های روزانه
                "bonus_coupons": 0,  # کوپن‌های جایزه
                "referral_link": str(uuid.uuid4()), # ایجاد لینک یکتا
                "referred_by": None, # چه کسی این کاربر را معرفی کرده است
                "last_reset": None,  # آخرین زمان بازنشانی کوپن
                "plan_expiry": None,  # تاریخ انقضای پلن پولی
                "gemini_api_key": encrypted_api_key  # API Key رمزنگاری شده
            }
            save_user_data()

        # بازنشانی کوپن ها اگر روز جدیدی باشد
        reset_daily_coupons(chat_id, bot_settings)
        load_user_data() # بارگذاری مجدد برای اعمال تغییرات

        # ساخت کیبورد
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True,  one_time_keyboard=True)
        contact_button = telebot.types.KeyboardButton(text="📞 ارتباط با مدیر")
        suggestion_button = telebot.types.KeyboardButton(text="💡 پیشنهادات و اسپانسری")
        help_button = telebot.types.KeyboardButton(text="❓ راهنما")  # دکمه راهنما
        buy_button = telebot.types.KeyboardButton(text="💰 خرید پلن")

        keyboard.add(contact_button, suggestion_button, help_button, buy_button)

        # نمایش اطلاعات به کاربر
        user_info = user_data[chat_id]
        referral_link = f"https://t.me/{bot.get_me().username}?start={user_info['referral_link']}"
        text = f"👋 سلام!\nبه ربات ترجمه زیرنویس خوش آمدید.\n\n"

        from ..config import DEFAULT_DAILY_COUPON_COUNT, PAID_PLAN_DAILY_COUPON_COUNT, PAID_PLAN_PRICE

        # نمایش وضعیت پلن پولی
        if is_paid_plan_active(chat_id):
            text += f"✨ شما دارای پلن پولی هستید و {bot_settings.PAID_PLAN_DAILY_COUPON_COUNT} کوپن روزانه دارید.\n"
        else:
            text += f"شما {bot_settings.DEFAULT_DAILY_COUPON_COUNT} کوپن روزانه و {user_info['bonus_coupons']} کوپن جایزه دارید.\n"
            text += f"🔑 برای دریافت {bot_settings.PAID_PLAN_DAILY_COUPON_COUNT} کوپن روزانه، [پلن پولی]({bot_settings.PAID_PLAN_PRICE} تومان) را خریداری کنید.\n"

        text += f"🔗 لینک معرفی شما: {referral_link}\n\n"
        text += "🎬 برای ترجمه زیرنویس، یک فایل SRT ارسال کنید."

        bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="Markdown" )

    @bot.message_handler(commands=["help"])
    def show_help(message: telebot.types.Message, bot_settings: BotSettings = settings) -> None:
        """
        نمایش راهنمای کامل ربات.
        """
        chat_id = str(message.chat.id)

        help_text = """
        📝 **راهنمای ربات ترجمه زیرنویس** 🤖

        با استفاده از این ربات، می‌توانید فایل‌های زیرنویس SRT را به زبان‌های مختلف ترجمه کنید.

        ⚙️ **دستورات:**
        *   /start - شروع مجدد ربات و نمایش راهنما
        *   /help - نمایش این راهنما
        *   /coupons - نمایش تعداد کوپن‌های باقی‌مانده
        *   /buy_plan - اطلاعات پلن پولی و خرید
        *   /suggest - ارسال پیشنهادات به مدیر
        *   /contact - اطلاعات تماس با مدیر

        🚀 **نحوه استفاده:**
        1.  📤 یک فایل SRT را به ربات ارسال کنید.
        2.  等待 ربات فایل را در صف ترجمه قرار می‌دهد.
        3.  ✅ پس از ترجمه، فایل ترجمه شده به همراه اطلاعات به شما ارسال می‌شود.

        💎 **پلن پولی:**
        با خرید پلن پولی، از مزایای زیر بهره‌مند شوید:
        *   ✅ کوپن روزانه بیشتر
        *   ⚡️ اولویت در ترجمه

        🤝 **لینک معرفی:**
        با اشتراک لینک خود، کوپن رایگان دریافت کنید!

        💬 **ارتباط با مدیر:**
        ❓ سوالی دارید؟ با ما در ارتباط باشید.

        💡 **پیشنهادات و اسپانسری:**
        ✉️ پیشنهادات خود را برای بهبود ربات با ما درمیان بگذارید.
        """

        bot.send_message(chat_id, help_text, parse_mode="Markdown")
