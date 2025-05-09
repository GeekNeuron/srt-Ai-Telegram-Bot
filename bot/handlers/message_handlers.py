import telebot
from ..utils import translation_utils, data_utils, security_utils
from ..config import BotSettings
from ..models.translation_request import TranslationRequest
from ..utils.data_utils import user_data, can_use_coupon, use_coupon, load_user_data

def register_handlers(bot: telebot.TeleBot, settings: BotSettings):
     @bot.message_handler(content_types=["document"])
     def handle_document(message: telebot.types.Message, bot_settings: BotSettings = settings) -> None:
        """
        دریافت فایل SRT و ترجمه آن و اضافه کردن به صف.
        """
        chat_id = str(message.chat.id)

        # بررسی تعداد کوپن (ترکیبی از کوپن های روزانه و جایزه)
        can_use, reason = can_use_coupon(chat_id)
        if not can_use:
            # نمایش اطلاعات پلن پولی
            user_info = user_data[chat_id]
            text = "متاسفم، شما کوپن کافی برای استفاده ندارید.\n\n"
            text += f"برای دریافت {bot_settings.PAID_PLAN_DAILY_COUPON_COUNT} کوپن روزانه، پلن پولی را به قیمت {bot_settings.PAID_PLAN_PRICE} تومان خریداری کنید. (/buy_plan)\n"
            bot.reply_to(message, text)
            return

        # استفاده از کوپن (ابتدا کوپن های روزانه، سپس جایزه)
        use_coupon(chat_id)
        load_user_data()

        file_info = bot.get_file(message.document.file_id)
         from ..utils.security_utils import decrypt_api_key,ENCRYPTION_KEY

        # ---------------- ایجاد شیء درخواست ترجمه ----------------
        user_setting = user_data[chat_id]
        source_language = user_setting.get("language", bot_settings.DEFAULT_LANGUAGE)
        target_language = user_setting.get("translation_language", bot_settings.DEFAULT_LANGUAGE)
        translation_style = user_setting.get("translation_style", "formal")
        # رمزگشایی API Key
        gemini_api_key = ""
        encrypted_api_key = user_setting.get("gemini_api_key")
        if encrypted_api_key:
            gemini_api_key = decrypt_api_key(encrypted_api_key, ENCRYPTION_KEY)

        # بررسی وجود API Key
        if not gemini_api_key:
            bot.reply_to(message, "API Key شما یافت نشد. لطفا /start را دوباره امتحان کنید.")
            return

        translation_request = TranslationRequest(
            chat_id, file_info, source_language, target_language, translation_style, gemini_api_key
        )

        # ---------------- محدودیت نوبت در صف ----------------
        from ..utils.data_utils import MAX_QUEUE_SIZE_PAID, is_paid_plan_active, MAX_QUEUE_SIZE_FREE
        from queue import Queue
        translation_queue = Queue()
        max_queue_size = MAX_QUEUE_SIZE_PAID if is_paid_plan_active(chat_id) else MAX_QUEUE_SIZE_FREE
        if translation_queue.qsize() >= max_queue_size:
            bot.reply_to(message, "متاسفم، صف ترجمه پر است. لطفا بعدا دوباره تلاش کنید.")
            return

        # ---------------- اضافه کردن به صف ----------------
        translation_queue.put(translation_request)

        # ---------------- اطلاع رسانی به کاربر ----------------
        bot.send_message(chat_id, f"فایل شما با موفقیت به صف ترجمه اضافه شد. نوبت شما: {translation_queue.qsize()}")
