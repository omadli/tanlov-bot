import json
import datetime
from aiogram import types
from bot.loader import dp
from bot.async_orm import *
from bot.aio.states import Form
from aiogram.dispatcher import FSMContext

from src.settings import ADMIN

def valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d.%m.%Y')
        return True
    except ValueError:
        return False



# _______________________ Handlers _____________________________


@dp.message_handler(state=Form.full_name)
async def enter_name(message: types.Message, state: FSMContext):

    await message.answer(
        "Tug'ilgan kun oy yilingizni dd.mm.yyyy formatda kiriting.\n"
        "Masalan 31.12.1999"
    )

    await state.update_data(
        {"full_name": message.text}
    )

    await Form.next()


@dp.message_handler(state=Form.birth_date)
async def enter_birth_date(message: types.Message, state: FSMContext):
    if valid_date(message.text):
        # To'g'ri formatda kiritildi

        await state.update_data(
            {"birth_date": message.text}
        )
        
        await message.answer(
            "Yashash manzilingizni kiriting.\n"
            "Viloyat, mahalla, ko'cha, xonadon"
        )

        await Form.next()

    else:
        await message.answer(
            "Noto'g'ri format!\n"
            "Iltimos qayta tekshirib dd.mm.yyyy formatda kiriting.\n"
            "Masalan 31.12.1999"
        )


@dp.message_handler(state=Form.adress)
async def enter_adress(message: types.Message, state: FSMContext):

    await state.update_data(
        {"adress": message.text}
    )

    await message.answer(
        "<b>O‘qish</b> (ta’lim muassasasi nomi, yo‘nalishi, bosqichi) "
        "yoki <b>ish joyingiz</b> (tashkilot nomi va lavozimi)ni to‘liq kiriting."
    )

    await Form.next()


@dp.message_handler(state=Form.work_or_study)
async def enter_work_or_study(message: types.Message, state: FSMContext):
    await state.update_data(
        {"work_or_study": message.text}
    )

    await message.answer(
        text="Siz bilan bog‘lanish uchun telefon raqamingizni kiriting",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="📞Raqamni yuborish", request_contact=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    await Form.next()



@dp.message_handler(content_types="contact", is_sender_contact=True, state=Form.tel)
async def enter_tel(message: types.Message, state: FSMContext):
    await state.update_data(
        {"tel": message.contact.phone_number}
    )

    await message.answer(
        text = "Tanlovga taqdim etilayotgan materiallar (elektron fayllar)ni kiriting",
        reply_markup = types.ReplyKeyboardRemove()
    )

    await Form.next()



@dp.message_handler(state=Form.tel)
async def error_tel(message: types.Message, state: FSMContext):
    await message.answer("Iltimos pastdagi tugmani bosib faqat o'zingizning raqamingizni kiriting.")



@dp.message_handler(content_types=["video", "document"], state=Form.files)
async def entering_files(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    files = datas.get("files")
    if files:
        files = json.loads(files)  
    else:
        await message.answer(
            text="Yana fayllar yubormoqchi bo'lsangiz yuboring.\n"
                "Yuboradigan fayllaringiz tugagach pastdagi \"Yakunlash\" tugmasini bosing.",
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text="Yakunlash")]
                ],
                resize_keyboard=True,
                one_time_keyboard=False
            )
        )
        files = {"video":[], "document":[]}
    ctype = str(message.content_type)
    if ctype == "video":
        files["video"].append(message.video.file_id)
    elif ctype == "document":
        files["document"].append(message.document.file_id)
    

    datas.update(files = json.dumps(files))
    await state.update_data(datas)



@dp.message_handler(text="Yakunlash", state=Form.files)
async def finish_sending_files(message: types.Message, state: FSMContext):
    datas = await state.get_data()
    files = json.loads(datas.get("files"))
    txt = "FISH: " + datas.get("full_name") + "\n"
    txt += "Tug'ilgan sana: " + datas["birth_date"] + "\n"
    txt += "Manzil: " + datas["adress"] + "\n"
    txt += "Ish yoki o'qish joyi: " + datas["work_or_study"] + "\n"
    txt += "Tel: " + datas["tel"] + "\n"
    # txt += "Fayllar: " + datas["files"]
    m1 = await message.answer(txt, reply_markup=types.ReplyKeyboardRemove())
    await m1.reply(
        text = "Barcha ma'lumotlar to'g'riligini tasdiqlaysizmi?",
        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Tasdiqlash", callback_data="ok")],
            [types.InlineKeyboardButton(text="Bekor qilish", callback_data="no")]
        ])
    )
    await Form.next()



@dp.message_handler(content_types="any", state=Form.files)
async def error_sending_files(message: types.Message, state: FSMContext):
    await message.answer(
        text="Faqat videolar yoki videolar faylini yuboring.\n"
            "Barchasi yuborib bo'lgach pastdagi \"Yakunlash\" tugmasini bosing.",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Yakunlash")]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
    )


@dp.callback_query_handler(text="ok", state=Form.ok)
async def submit_form(query: types.CallbackQuery, state: FSMContext):
    datas = await state.get_data()
    files = json.loads(datas.get("files"))
    n_video = len(files.get("video"))
    n_doc = len(files.get("document"))
    txt = "FISH: " + datas.get("full_name") + "\n"
    txt += "Tug'ilgan sana: " + datas["birth_date"] + "\n"
    txt += "Manzil: " + datas["adress"] + "\n"
    txt += "Ish yoki o'qish joyi: " + datas["work_or_study"] + "\n"
    txt += "Tel: " + datas["tel"] + "\n"
    # txt += "Fayllar: " + datas["files"]
    try:
        contestant = await Contestant_create(
            tg_user = await TgUser_get(tg_id=query.from_user.id),
            fish = datas["full_name"],
            birth_date = datas["birth_date"],
            adress = datas["adress"],
            work_or_study = datas["work_or_study"],
            tel = int(datas["tel"]),
            files = datas["files"]
        )
        c_id = contestant.pk
        txt2 =  f"#N{c_id} raqamli ishtirokchi\n"
        txt2 += f"Ishtirokchi <a href='tg://user?id={query.from_user.id}'>{query.from_user.full_name}</a> "
        txt2 += f"{'@' + query.from_user.username}" if query.from_user.username else ""
        txt2 += "\n" + txt
        await dp.bot.send_message(ADMIN, txt2)
        for i in range(n_video):
            await dp.bot.send_video(
                chat_id = ADMIN,
                video = files.get("video")[i],
                caption = f"#N{c_id} raqamli ishtirokchi"
            )
        for i in range(n_doc):
            await dp.bot.send_document(
                chat_id = ADMIN,
                document = files.get("document")[i],
                caption = f"#N{c_id} raqamli ishtirokchi "
            )

        await query.message.edit_text("Tayyor!\nSizning ma'lumotlaringiz yuborildi")
    except Exception as e:
        print(e)
        await query.message.edit_text("Xatolik!")
        print(datas)
    

    await state.finish()


@dp.callback_query_handler(text="no", state=Form.ok)
async def no_submit_form(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Bekor qilindi. Boshqatdan /start bosing")
    await state.finish()

