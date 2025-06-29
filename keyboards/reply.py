from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕Добавить абитуриента"),
            KeyboardButton(text="👥Посмотреть абитуриентов"),
        ],
    ], resize_keyboard=True)

level_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎓Бакалавриат"),
            KeyboardButton(text="🎓Магистратура"),
            KeyboardButton(text="🎓Колледж"),

        ],
    ], resize_keyboard=True)

direction_college_kb = ReplyKeyboardMarkup

in_process_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌отмена"),
        ],
    ], resize_keyboard=True)

education_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅завершить"),
        ],
    ], resize_keyboard=True)