from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton


def by_buttons_kb(buttons: list) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.add(KeyboardButton(text=button))

    builder.adjust(2)  # Adjust the number of buttons in each row
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def direction_kb(directions: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for direction in directions:
        builder.row(
            InlineKeyboardButton(text=direction, callback_data=f"{direction}")
        )

    builder.adjust(1)  # Adjust the number of buttons in each row


    return builder.as_markup()