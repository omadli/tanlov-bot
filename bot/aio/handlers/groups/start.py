from aiogram import types
from bot.loader import dp


@dp.message_handler(commands="start", chat_type=["group", "supergroup"])
async def cmd_start_in_group(message: types.Message):
    await message.answer("Bot ishlayapti")


@dp.message_handler(content_types="any", chat_type=["group", "supergroup"])
async def echo_in_group(message: types.Message):
    await message.reply("Menga shaxsiyda yozing.")

