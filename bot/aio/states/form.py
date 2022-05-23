from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    full_name = State()
    birth_date = State()
    adress = State()
    work_or_study = State()
    tel = State()
    files = State()
    ok = State()