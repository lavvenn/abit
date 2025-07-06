from aiogram.fsm.state import State, StatesGroup

class adding(StatesGroup):
    last_name = State()
    email = State()
    phone_number = State()
    parent_phone_number = State()
    level = State()
    direction = State()
    photo = State()
    passport = State()
    snils = State()
    education = State()

class chek(StatesGroup):
    last_name = State()