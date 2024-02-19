from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram import flags
from aiogram.fsm.context import FSMContext
import utils
import db
from datetime import datetime
from states import Gen

from aiogram import Bot
import config
from aiogram.enums.parse_mode import ParseMode

import kb
import text

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await db.add_user(msg.from_user.id)
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "menu")
async def menu(clbck: CallbackQuery):
    await clbck.message.edit_text(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "balance")
async def menu(clbck: CallbackQuery):
    balance = await db.get_balance(clbck.message.chat.id)
    last_date = datetime.strptime(await db.get_lastdate(clbck.message.chat.id), '%Y-%m-%d %H:%M:%S.%f')
    current_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    print(last_date)
    print(current_date)
    if clbck.message.chat.id == 382767498 or clbck.message.chat.id == 1487868467 or clbck.message.chat.id == 6023561041:
        await db.change_balance('+100', clbck.message.chat.id)
    if int(balance) == 0 and last_date < current_date:
        await db.change_balance('+3', clbck.message.chat.id)
        balance = '3'
    await clbck.message.edit_text(text.balance + str(balance), reply_markup=kb.iexit_kb)

@router.callback_query(F.data == "kb")
async def menu(clbck: CallbackQuery):
    await clbck.message.edit_text(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    balance = await db.get_balance(clbck.message.chat.id)
    last_date = datetime.strptime(await db.get_lastdate(clbck.message.chat.id), '%Y-%m-%d %H:%M:%S.%f')
    current_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    if int(balance) > 0:
        await state.set_state(Gen.room_type)
        await clbck.message.edit_text(text.gen_image, reply_markup=kb.iexit_kb)
    else:
        if last_date < current_date:
            await db.change_balance('+3', clbck.message.chat.id)
            await state.set_state(Gen.room_type)
            await clbck.message.edit_text(text.gen_image, reply_markup=kb.iexit_kb)
        else:
            await clbck.message.edit_text(text.low_balance, reply_markup=kb.iexit_kb)

@router.message(Gen.room_type)
@flags.chat_action("choose_room")
async def room_type(msg: Message, state: FSMContext):
    prompt = msg.photo[-1].file_id
    await state.update_data(img_prompt=prompt)
    await msg.answer(text.choose_room, reply_markup=kb.room_types)
    #await msg.answer(text.gen_exit, reply_markup=kb.exit_kb)

@router.callback_query(F.data == "bedroom")
@router.callback_query(F.data == "living room")
@router.callback_query(F.data == "kitchen")
@router.callback_query(F.data == "bathroom")
async def input_room_type(clbck: CallbackQuery, state: FSMContext):
    await state.update_data(room_type=clbck.data)
    await clbck.message.edit_text(text.choose_style, reply_markup=kb.room_styles)

@router.callback_query(F.data == "minimalism")
@router.callback_query(F.data == "modern")
@router.callback_query(F.data == "zen")
@router.callback_query(F.data == "scandinavian")
@router.callback_query(F.data == "country")
@router.callback_query(F.data == "vintage")
@router.callback_query(F.data == "tropical")
@router.callback_query(F.data == "coastal")
@router.callback_query(F.data == "japanese")
async def input_room_type(clbck: CallbackQuery, state: FSMContext):
    await state.update_data(room_style=clbck.data)
    await state.set_state(Gen.get_img)
    await clbck.message.edit_text(text.gen_wait)
    data = await state.get_data()
    file_id = data['img_prompt']
    type = data['room_type']
    style = data['room_style']
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    try:
        file = await bot.get_file(file_id)
        # mesg = await msg.answer(text.gen_wait)
        resp = await utils.generate_image(file.file_path, type, style)
        await clbck.message.delete()
        await clbck.message.answer_photo(photo=resp, caption=text.img_watermark)
        await clbck.message.answer(text.menu, reply_markup=kb.menu)
        await db.change_balance('-1', clbck.message.chat.id)
        await db.set_lastdate(clbck.message.chat.id)
    except Exception:
        await clbck.message.delete()
        await clbck.message.answer(text.gen_error, reply_markup=kb.menu)
        await clbck.message.answer(text.menu, reply_markup=kb.menu)