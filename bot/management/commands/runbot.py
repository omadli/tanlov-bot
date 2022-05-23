from django.core.management.base import BaseCommand
from aiogram import executor, Dispatcher
from bot.loader import dp
import bot.aio.middlewares, bot.aio.filters, bot.aio.handlers
from bot.aio.utils.set_bot_commands import set_default_commands
from src.settings import ADMIN


async def startup(dispatcher: Dispatcher):
    await set_default_commands(dispatcher)
    await dispatcher.bot.send_message(
        chat_id=ADMIN, 
        text="Bot ishga tushdi"
    )

async def shutdown(dispatcher: Dispatcher):
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
            on_startup=startup, 
            on_shutdown=shutdown
        )
