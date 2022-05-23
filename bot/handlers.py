from aiogram import types, Dispatcher
from .loader import dp
from .models import TgUser, Contestant
from django.db.models import Model

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    try:
        user:Model = TgUser.objects.get(tg_id=message.from_user.id)
        # bazada mavjud

        await message.answer(f"Xush kelibsiz {message.from_user.get_mention(as_html=True)}")

        if user.full_name != message.from_user.full_name or user.username != message.from_user.username:
            # bazadagi ma'lumotlar (nom yoki username) o'zgargan bo'lsa
            user.update(
                full_name = message.from_user.full_name,
                username = message.from_user.username
            )

    except TgUser.DoesNotExist:
        # bazada mavjud bo'lmasa

        # bazaga qo'shib qo'yamiz
        TgUser.objects.create(
            tg_id = message.from_user.id,
            full_name = message.from_user.full_name,
            username = message.from_user.username
        )

        await message.answer(
            f"Assalomu alaykum {message.from_user.get_mention(as_html=True)}\n"
            f"<b>“XALQPARVAR DAVLAT XIZMATCHISI”</b> ijtimoiy videoroliklar "
            f"tanlovida ishtirok etish uchun ariza topshirish botiga xush kelibsiz!"
        )



    


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)