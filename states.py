from aiogram.fsm.state import State, StatesGroup

class adding(StatesGroup):
    last_name = State()
    level = State()
    direction = State()
    photo = State()
    passport = State()
    snils = State()
    education = State()