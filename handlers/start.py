from aiogram import Router, F
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.reply import main_kb

from states import adding

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Hello! I'm your bot. How can I assist you today?", reply_markup=main_kb)

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Here are the commands you can use:\n"
                         "/start - Start the bot\n"
                         "/help - Get help information\n"
                         "Feel free to ask me anything!")

@router.message(F.text == "➕Добавить абитуриента")
async def add_applicant(message: Message, state: FSMContext):
    await state.set_state(adding.last_name)
    await message.answer(f"введите фамилию абитуриента:", reply_markup=ReplyKeyboardRemove())
    await message.answer("Вы можите нажать на кнопку ниже, чтобы вернуться в главное меню.")

    
@router.message(F.text == "👥Посмотреть абитуриентов")
async def view_applicants(message: Message):
    await message.answer("""


                            """)
    
