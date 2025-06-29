from aiogram import Router
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Hello! I'm your bot. How can I assist you today?")