from aiogram import types
from bot.loader import dp
from bot.async_orm import *
from bot.aio.states import Form
from django.db.models import Model


@dp.message_handler(commands="start", state='*')
async def cmd_start(message: types.Message):
    try:
        user:Model =  await TgUser_get(tg_id=message.from_user.id)
        # bazada mavjud
        await message.answer(f"Xush kelibsiz {message.from_user.get_mention(as_html=True)}")
        try:
            contestant = await Contestant_get(tg_user=user)
            await message.answer("Siz tanlovda ishtirok etyapsiz!")
        except Contestant.DoesNotExist:
            await message.answer("Familiyangiz, ismingiz, sharifingiz to'liq kiriting.")
            await Form.full_name.set()


    except TgUser.DoesNotExist:
        # bazada mavjud bo'lmasa

        # bazaga qo'shib qo'yamiz
        await TgUser_create(
            tg_id = message.from_user.id,
            full_name = message.from_user.full_name,
            username = message.from_user.username
        )

        await message.answer(
            f"Assalomu alaykum {message.from_user.get_mention(as_html=True)}\n"
            f"<b>“XALQPARVAR DAVLAT XIZMATCHISI”</b> ijtimoiy videoroliklar "
            f"tanlovida ishtirok etish uchun ariza topshirish botiga xush kelibsiz!"
        )
        
        await message.answer("Familiyangiz, ismingiz, sharifingiz to'liq kiriting.")
        await Form.full_name.set()
        