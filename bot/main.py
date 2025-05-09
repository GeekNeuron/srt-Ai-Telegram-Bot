import asyncio
import logging
import schedule
import time
from telebot import TeleBot
from .config import BotSettings
from .handlers import command_handlers, message_handlers, callback_handlers
from .utils import data_utils

# -------------------------- تنظیمات Logging --------------------------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------- بارگیری تنظیمات --------------------------
settings = BotSettings()

# -------------------------- ایجاد شیء ربات --------------------------
bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)

# -------------------------- ثبت Handler ها --------------------------
command_handlers.register_handlers(bot, settings)
message_handlers.register_handlers(bot, settings)
callback_handlers.register_handlers(bot, settings)

# -------------------------- وظایف زمان‌بندی شده --------------------------
def reset_coupons_job(bot_settings: BotSettings = settings) -> None:
    """
    وظیفه بازنشانی کوپن ها.
    """
    logging.info("شروع بازنشانی کوپن ها...")
    data_utils.reset_all_daily_coupons(bot_settings)
    logging.info("بازنشانی کوپن ها با موفقیت انجام شد.")

# زمان‌بندی اجرای وظیفه بازنشانی کوپن ها (هر روز ساعت 00:00)
schedule.every().day.at("00:00").do(reset_coupons_job)

async def main(bot_settings: BotSettings = settings) -> None:
    # بازنشانی کوپن‌ها در هنگام شروع ربات
    data_utils.reset_all_daily_coupons(bot_settings)

    # شروع ذخیره دوره ای اطلاعات
    asyncio.create_task(data_utils.periodic_data_save())

    # ایجاد یک حلقه بی نهایت برای اجرای زمان‌بندی
    async def run_scheduler():
        while True:
            schedule.run_pending()
            await asyncio.sleep(60)  # بررسی هر 60 ثانیه

    # اجرای ربات به صورت ناهمزمان
    bot_task = asyncio.create_task(bot.infinity_polling())
    scheduler_task = asyncio.create_task(run_scheduler())

    await asyncio.gather(bot_task, scheduler_task)

if __name__ == "__main__":
    asyncio.run(main())
