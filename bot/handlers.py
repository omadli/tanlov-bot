from aiogram import types, Dispatcher
from .loader import dp


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer(
        f"Assalomu alaykum {message.from_user.get_mention(as_html=True)}\n"
        f"<b>“XALQPARVAR DAVLAT XIZMATCHISI”</b> ijtimoiy videoroliklar "
        f"tanlovida ishtirok etish uchun ariza topshirish botiga xush kelibsiz!"
    )


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)