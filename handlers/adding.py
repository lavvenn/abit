import os

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from PIL import Image

from states import adding

from db.requests import add_applicant

from keyboards.reply import education_kb, in_process_kb, main_kb
from keyboards.builder import direction_kb, by_buttons_kb 
from keyboards.inline import level_kb

from config import DIRECTIONS, MAIN_PATH

def create_info_txt(file_name: str, last_name: str, email: str,level: str, direction: str, phone_number: str = None, parent_phone_number: str = None):
    with open(f"{file_name}", "w", encoding="UTF-8") as file:
        file.write(f"почта--> {email}\nномер абитуриента--> {phone_number} \nномер родителя--> {parent_phone_number} \nнаправление--> {direction} \nуровень образования --> {level}")

router = Router()

@router.message(adding.last_name)
async def process_last_name(message: Message, state: FSMContext):
    last_name = message.text
    print(f"Received last name: {last_name}")
    await state.update_data(last_name=last_name)
    await message.answer("Отлично! Теперь введите email абитуриента.",reply_markup=by_buttons_kb(["❌отмена регистрации"]))
    await state.set_state(adding.email)


@router.message(adding.email)
async def process_email(message: Message, state: FSMContext):
    email = message.text
    print(f"Received email: {email}")
    await state.update_data(email=email)
    await message.answer("Отлично! Теперь введите номер телефона абитуриента. или пропустите этот шаг, нажав 'пропустить'.", reply_markup=by_buttons_kb(["⏭️пропустить", "❌отмена регистрации"]))
    await state.set_state(adding.phone_number)


@router.message(adding.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    if message.text.lower() == "⏭️пропустить":
        await state.update_data(phone_number="0000000000")
        await message.answer("Вы пропустили ввод номера телефона абитуриента. Продолжаем.")
        await message.answer("Теперь введите номер телефона родителя абитуриента  или пропустите этот шаг.", reply_markup=by_buttons_kb(["⏭️пропустить", "❌отмена регистрации"]))
        await state.set_state(adding.parent_phone_number)
        return
    if not message.text.isdigit() or len(message.text) < 10:
        await message.answer("Пожалуйста, введите корректный номер телефона (только цифры, минимум 10 цифр).")
        return
    else:
        phone_number = message.text
        print(f"Received phone number: {phone_number}")
        await state.update_data(phone_number=phone_number)
        await message.answer("Отлично! Теперь введите номер телефона родителя абитуриента  или пропустите этот шаг.", reply_markup=by_buttons_kb(["⏭️пропустить", "❌отмена регистрации"]))
        await state.set_state(adding.parent_phone_number)


@router.message(adding.parent_phone_number)
async def process_parent_phone_number(message: Message, state: FSMContext):
    if message.text.lower() == "⏭️пропустить":
        await state.update_data(parent_phone_number="0000000000")
        await message.answer("Вы пропустили ввод номера телефона родителя. Продолжаем.", reply_markup = by_buttons_kb(["❌отмена регистрации"]))

        await message.answer("Теперь выберите уровень образования абитуриента.", reply_markup=level_kb)
        await state.set_state(adding.level)

    else:
        if not message.text.isdigit() or len(message.text) < 10:
            await message.answer("Пожалуйста, введите корректный номер телефона (только цифры, минимум 10 цифр).")
            
        else:
            parent_phone_number = message.text
            print(f"Received parent phone number: {parent_phone_number}")
            await state.update_data(parent_phone_number=parent_phone_number)
            await message.answer("Отлично! Теперь выберите уровень образования абитуриента.", reply_markup=level_kb)
            await state.set_state(adding.level)


@router.callback_query(adding.level)
async def process_level(query: CallbackQuery, state: FSMContext):
    level = query.data
    await state.update_data(level=level)
    await query.message.answer("Отлично! Выбирете направление.", reply_markup=direction_kb(DIRECTIONS[level]))
    await state.set_state(adding.direction)


@router.callback_query(adding.direction)
async def process_direction(query: CallbackQuery, state: FSMContext):
    direction = query.data
    await state.update_data(direction=direction)
    await query.message.answer("Отлично! Теперь отправьте фотографию абитуриента.", reply_markup=by_buttons_kb(["❌отмена регистрации"]))
    await state.set_state(adding.photo)


@router.message(adding.photo)
async def process_photo(message: Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1] if message.photo else None
    if photo:
        data = await state.get_data()

        file = await bot.get_file(photo.file_id)

        os.mkdir(f"{MAIN_PATH}/{data['last_name']}")

        await bot.download_file(file.file_path, destination=f"{MAIN_PATH}/{data['last_name']}/photo.jpg")
        await state.update_data(photo=photo.file_id)
        await message.answer("Спасибо! Теперь отправьте фотографию паспорта.")
        await state.set_state(adding.passport)
    else:
        await message.answer("Пожалуйста, отправьте фотографию абитуриента.")


@router.message(adding.passport)
async def process_passport(message: Message, state: FSMContext, bot: Bot):
    passport = message.photo[-1] if message.photo else None
    if passport:
        data = await state.get_data()

        file = await bot.get_file(passport.file_id)

        await bot.download_file(file.file_path, destination=f"{MAIN_PATH}/{data['last_name']}/passport.jpg")

        await state.update_data(passport=passport.file_id)
        await message.answer("Спасибо! Теперь отправьте СНИЛС.")
        await state.set_state(adding.snils)
    else:
        await message.answer("Пожалуйста, отправьте фотографию паспорта.")


@router.message(adding.snils)
async def process_snils(message: Message, state: FSMContext, bot: Bot):
    snils = message.photo[-1] if message.photo else None
    if snils:
        data = await state.get_data()
        file = await bot.get_file(snils.file_id)

        await bot.download_file(file.file_path, destination=f"{MAIN_PATH}/{data['last_name']}/snils.jpg")

        await state.update_data(snils=snils.file_id)
        await message.answer("Отлично! Теперь отправьте фотографии диплома об образовании. Вниматьельно!! Если у вас несколько фото, отправьте их все по очереди.")
        await state.set_state(adding.education)
    else:
        await message.answer("Пожалуйста, отправьте фотографию СНИЛСа.")


@router.message(adding.education)
async def process_education(message: Message, state: FSMContext, bot: Bot):
    education = message.photo[-1] if message.photo else None
    if education:
        data = await state.get_data()

        if "education" not in data:
            await state.update_data(education=[education.file_id])
            await message.answer("отправьте седующюю фотографию документа об образовании или завершите заполнение", reply_markup=education_kb)
        else:
            state.update_data(education=data["education"].append(education.file_id))
            await message.answer("отправьте седующюю фотографию документа об образовании или завершите заполнение", reply_markup=education_kb)

    else:
        if message.text == "✅завершить":
            data = await state.get_data()

            print(data)


            for photo in range(len(data["education"])):
                file = await bot.get_file(data["education"][photo])
                await bot.download_file(file.file_path, destination=f"{MAIN_PATH}/{data['last_name']}/education_{photo}.jpg")

            

            images = [
                Image.open(f"{MAIN_PATH}/{data['last_name']}/" + f)
                for f in [f"education_{i}.jpg" for i in range(len(data["education"]))]   
            ]

            pdf_path = f"{MAIN_PATH}/{data['last_name']}/education_result.pdf"

            images[0].save(pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])



            add_applicant(
                last_name=data["last_name"],
                email=data.get("email"),
                phone_number=data.get("phone_number"),
                parent_phone_number=data.get("parent_phone_number"),
                level=data["level"],
                direction=data["direction"],
            )

            create_info_txt(
                file_name=f"{MAIN_PATH}\{data['last_name']}\info.txt",
                last_name=data["last_name"],
                email=data.get("email"),
                phone_number=data.get("phone_number"),
                parent_phone_number=data.get("parent_phone_number"),
                level=data["level"],
                direction=data["direction"],
            )


            print("Applicant data:", data)
            await message.answer("Регистрация абитуриента завершена! Спасибо!", reply_markup=main_kb)
            await state.clear()
        
        else:
            await message.answer("Пожалуйста, отправьте фотографию диплома об образовании.")