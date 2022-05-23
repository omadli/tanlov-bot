from django.core.management.base import BaseCommand
from aiogram import executor, Dispatcher
from bot.loader import dp
from src.settings import ADMIN

async def startup_notify_admin(dispatcher: Dispatcher):
    await dispatcher.bot.send_message(
        chat_id=ADMIN, 
        text="Bot ishga tushdi"
    )

async def shutdown_notify_admin(dispatcher: Dispatcher):
    await dispatcher.bot.send_message(
        chat_id=ADMIN, 
        text="Bot to'xtadi"
    )

class Command(BaseCommand):

    help = "Telegram botni run qilish uchun"

    def handle(self, *args, **options):
        print("Running bot")
        executor.start_polling(
            dispatcher=dp, 
            skip_updates=True, 
            on_startup=startup_notify_admin, 
            on_shutdown=shutdown_notify_admin
        )
