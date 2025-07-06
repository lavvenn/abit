from aiogram import Router, F
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.reply import main_kb

from states import adding, chek

from keyboards.builder import by_buttons_kb

from db.requests import get_applicant_by_last_name

GREATING_MESSAGE = """
Здравствуйте! 👋🎉
Я — ваш помощник по загрузке данных 🗂️ и фотографий 📸 абитуриентов.
С моей помощью вы быстро ⚡ и удобно 🛠️ внесёте всю необходимую информацию 📋 в систему вашего вуза 🎓.
Просто следуйте инструкциям 👉, и процесс регистрации станет проще ✅ и быстрее 🚀!
Если нужна помощь ❓ — напишите мне 💬, я всегда готов помочь 🤝.
"""

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(GREATING_MESSAGE, reply_markup=main_kb)


@router.message(F.text == "➕Добавить абитуриента")
async def add_applicant(message: Message, state: FSMContext):
    await state.set_state(adding.last_name)
    await message.answer(f"введите фамилию абитуриента:", reply_markup=ReplyKeyboardRemove())
    await message.answer("Вы можите нажать на кнопку ниже, чтобы вернуться в главное меню.", reply_markup=by_buttons_kb(["❌отмена регистрации"]))

@router.message(F.text == "❌отмена регистрации")
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(GREATING_MESSAGE, reply_markup=main_kb)


    
@router.message(F.text == "👥Посмотреть абитуриентов")
async def view_applicants(message: Message, state: FSMContext):
    await message.answer("""
введите фамилию


                            """, reply_markup= by_buttons_kb(["завершить"]))
    await state.set_state(chek.last_name)

@router.message(chek.last_name)
async def view_applicants_by_id(message: Message, state :FSMContext):
    try:
        await message.answer(f"{get_applicant_by_last_name(message.text)}")
    except:
        await message.answer("вы ввели неверно ")
    if message.text == "завршить":
        await state.clear()
        await message.answer("выбирите действие", reply_markup=main_kb)



