# این فایل شامل هندلرهای مربوط به کال‌بک‌ها است (دکمه‌های اینلاین)
import telebot
import re
from ..utils import data_utils
from ..utils.security_utils import validate_file_name

from ..config import BotSettings
def register_handlers(bot: telebot.TeleBot, settings: BotSettings):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("output_"))
    def handle_output_type(call: telebot.types.CallbackQuery, bot_settings: BotSettings = settings) -> None:
        chat_id = str(call.message.chat.id)
        from ..utils.data_utils import user_data
        if chat_id not in user_data:
            bot.send_message(call.message.chat.id, "متاسفم، اطلاعات ترجمه شما یافت نشد. لطفا دوباره فایل SRT را ارسال کنید.")
            return

        translated_srt = user_data[chat_id]["translated_srt"]

          #محاسبه اطلاعات فایل 
        file_size = len(translated_srt.encode('utf-8'))  # حجم فایل (بایت)
        line_count = len(translated_srt.splitlines())  # تعداد خطوط
        char_count = len(re.findall(r"[a-zA-Z]", translated_srt))  # تعداد حروف
        number_count = len(re.findall(r"\d", translated_srt))  # تعداد اعداد

         #ایجاد کپشن فایل
        caption = f"""
        حجم فایل: {file_size} بایت
        تعداد خطوط: {line_count}
        تعداد حروف: {char_count}
        تعداد اعداد: {number_count}

        @{bot.get_me().username}
         """

        file_name = f"{bot.get_me().username}.srt"
        try:
            bot.send_document(call.message.chat.id, data = translated_srt.encode('utf-8') ,caption=caption ,  visible_file_name=file_name)
        except Exception as e:
             # گزارش خطا به مدیر
            from ..utils.data_utils import report_error_to_manager
            error_message = f"خطا در ارسال فایل به کاربر {chat_id}: {e}"
            report_error_to_manager(error_message, bot_settings)
            bot.send_message(chat_id, "متاسفم، در ارسال فایل مشکلی پیش آمد. لطفاً دوباره تلاش کنید.")
