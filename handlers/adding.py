from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import adding

from keyboards.reply import education_kb, level_kb, in_process_kb
from keyboards.builder import direction_college_kb 

router = Router()

@router.message(adding.last_name)
async def process_last_name(message: Message, state: FSMContext):
    last_name = message.text
    print(f"Received last name: {last_name}")
    await state.update_data(last_name=last_name)
    await message.answer("Отлично! выбирите уровень образования.", reply_markup=level_kb)
    await state.set_state(adding.level)


@router.message(adding.level)
async def process_level(message: Message, state: FSMContext):
    level = message.text
    await state.update_data(level=level)
    await message.answer("Отлично! Выбирете направление.", reply_markup=direction_college_kb(["Направление 1", "Направление 2", "Направление 3", "Направление 4", "Направление 5"]))
    await state.set_state(adding.direction)


@router.callback_query(adding.direction)
async def process_direction(query: CallbackQuery, state: FSMContext):
    direction = query.data
    await state.update_data(direction=direction)
    await query.message.answer("Отлично! Теперь отправьте фотографию абитуриента.", reply_markup=in_process_kb)
    await state.set_state(adding.photo)


@router.message(adding.photo)
async def process_photo(message: Message, state: FSMContext):
    photo = message.photo[-1] if message.photo else None
    if photo:
        await state.update_data(photo=photo.file_id)
        await message.answer("Спасибо! Теперь отправьте фотографию паспорта.")
        await state.set_state(adding.passport)
    else:
        await message.answer("Пожалуйста, отправьте фотографию абитуриента.")


@router.message(adding.passport)
async def process_passport(message: Message, state: FSMContext):
    passport = message.photo[-1] if message.photo else None
    if passport:
        await state.update_data(passport=passport.file_id)
        await message.answer("Спасибо! Теперь отправьте СНИЛС.")
        await state.set_state(adding.snils)
    else:
        await message.answer("Пожалуйста, отправьте фотографию паспорта.")


@router.message(adding.snils)
async def process_snils(message: Message, state: FSMContext):
    snils = message.photo[-1] if message.photo else None
    if snils:
        await state.update_data(snils=snils.file_id)
        await message.answer("Отлично! Теперь отправьте фотографии диплома об образовании. Вниматьельно!! Если у вас несколько фото, отправьте их все по очереди.")
        await state.set_state(adding.education)
    else:
        await message.answer("Пожалуйста, отправьте фотографию СНИЛСа.")


@router.message(adding.education)
async def process_education(message: Message, state: FSMContext):
    education = message.photo[-1] if message.photo else None
    if education:
        await state.update_data(education=[education.file_id])
        await message.answer("отправьте седующюю фотографию документа об образовании или завершите заполнение", reply_markup=education_kb)
    else:
        await message.answer("Пожалуйста, отправьте фотографию диплома об образовании.")


@router.message(adding.education, F.text == "✅завершить")
async def finish_education(message: Message, state: FSMContext):
    data = await state.get_data()
    last_name = data.get("last_name")
    passport = data.get("passport")
    snils = data.get("snils")
    education = data.get("education")

    # Здесь можно добавить логику для сохранения данных в базу данных или другую обработку

    await message.answer(f"Спасибо, данные {last_name} успешно сохранены.")
    await state.clear()
        
