from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


level_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎓Бакалавриат", callback_data="Бакалавриат"),
            InlineKeyboardButton(text="🎓Магистратура", callback_data="Магистратура"),
        ],
        [
            InlineKeyboardButton(text="🎓Колледж", callback_data="Колледж"),
        ],
    ]
)