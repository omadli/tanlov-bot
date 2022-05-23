from django.core.management.base import BaseCommand
from aiogram import executor, Dispatcher
from bot.loader import dp
from src.settings import ADMIN

async def notify_admin(dispatcher: Dispatcher):
    await dispatcher.bot.send_message(
        chat_id=ADMIN, 
        text="Bot ishga tushdi"
    )


class Command(BaseCommand):

    help = "Telegram botni run qilish uchun"

    def handle(self, *args, **options):
        print("Running bot")
        executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=notify_admin)
