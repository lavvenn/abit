from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton

directions = [
    "Направление 1",
    "Направление 2",
    "Направление 3",
    "Направление 4",
    "Направление 5"
]

def direction_college_kb(directions: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for direction in directions:
        builder.row(
            InlineKeyboardButton(text=direction, callback_data=f"{direction}")
        )

    builder.adjust(1)  # Adjust the number of buttons in each row


    return builder.as_markup()