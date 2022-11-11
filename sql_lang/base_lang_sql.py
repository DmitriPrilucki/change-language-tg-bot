import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, types, executor
import logging
from config import TOKEN
import sql_for_lang

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)
count = 1

############################## ОНЛАЙН КНОПКИ #################################

IKB_ENG = types.InlineKeyboardMarkup()
IB_ENG = types.InlineKeyboardButton(text='PRESS ME!', callback_data='press_eng')
IKB_ENG.add(IB_ENG)

IKB_RU = types.InlineKeyboardMarkup()
IB_RU = types.InlineKeyboardButton(text='НАЖМИ НА МЕНЯ!', callback_data='press_ru')
IKB_RU.add(IB_RU)

############################## ПРИ СТАРТЕ БОТА #################################


async def on_startup(_):
    await sql_for_lang.db_conn()
    print('БД ПОДКЛЮЧЕНА!')


############################## ПРИ СТАРТЕ ОБЩЕНИЯ С БОТОМ #################################


@dp.message_handler(content_types=["new_chat_members"])
async def new_user(message: types.Message):
    global count
    await message.answer('Hi!')
    await sql_for_lang.new_user(user_id=message.from_user.id)
    await sql_for_lang.insert_eng(user_id=message.from_user.id)
    count += 1


#################### КОМАНДЫ БОТА #############################


@dp.message_handler(commands=['eng'])
async def set_eng(message: types.Message):
    await message.answer('All rith!')
    await sql_for_lang.update_eng(user_id=message.from_user.id)


@dp.message_handler(commands=['ru'])
async def set_ru(message: types.Message):
    await message.answer('Хорошо!')
    await sql_for_lang.update_ru(user_id=message.from_user.id)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "/eng - for english language,\n/ru - для русского языка!")
        await sql_for_lang.new_user(user_id=message.from_user.id)
    except sqlite3.IntegrityError:
        await bot.send_message(message.from_user.id, "^▼^")


@dp.message_handler(commands=['test'])
async def bot_not_know(message: types.Message):
    lang_sel = await sql_for_lang.sel_lang(user_id=message.from_user.id)
    print(str(lang_sel))
    if lang_sel == str(('ru',)):
        await message.answer('РУССКИЙ КОНТЕНТ!!!')
        print('ru')
    if lang_sel == str(('eng',)):
        await message.answer('ENG CONTENT!!!')
        print('eng')
    else:
        await message.answer('!error not set language!')


@dp.message_handler(commands=['press'])
async def bot_not_know(message: types.Message):
    lang_sel = await sql_for_lang.sel_lang(user_id=message.from_user.id)
    print(str(lang_sel))
    if lang_sel == str(('ru',)):
        await message.answer('НАЖМИ НА КНОПКУ ЧТО БЫ ПОЛУЧИТЬ 10000000$!!!', reply_markup=IKB_RU)
        print('ru')
    if lang_sel == str(('eng',)):
        await message.answer('CLICK ON THE BUTTON TO GET $10000000!!!', reply_markup=IKB_ENG)
        print('eng')
    if lang_sel == str(('',)):
        await message.answer('!error not set language!')


@dp.message_handler(commands=['all_users'])
async def bot_not_know(message: types.Message):
    await message.answer(str(count))


############################## КАЛЛБЭКИ #################################

@dp.callback_query_handler(text='press_ru')
async def all_call(callback: types.CallbackQuery):
    await asyncio.sleep(3)
    await callback.message.answer('ЗАПУСКАЮ БОЕГОЛОВКИ В АНГЛИЮ 0%')
    await callback.answer()
    await asyncio.sleep(1)
    await callback.message.answer('ЗАПУСКАЮ БОЕГОЛОВКИ В АНГЛИЮ 31%')
    await asyncio.sleep(0.5)
    await callback.message.answer('ЗАПУСКАЮ БОЕГОЛОВКИ В АНГЛИЮ 46%')
    await asyncio.sleep(2)
    await callback.message.answer('ЗАПУСКАЮ БОЕГОЛОВКИ В АНГЛИЮ 99%')
    await callback.message.answer('ЗАПУСКАЮ БОЕГОЛОВКИ В АНГЛИЮ 100%')
    await callback.message.reply('☢️БОЕГОЛОВКА УСПЕШНО ЗАПУЩЕНА!')
    await asyncio.sleep(1)
    await callback.message.reply("💥 О нет её подбили 😭")


@dp.callback_query_handler(text='press_eng')
async def all_call(callback: types.CallbackQuery):
    await asyncio.sleep(3)
    await callback.message.answer('THEY LAUNCH WARHEADS INTO ENGLAND 0%')
    await callback.answer()
    await asyncio.sleep(1)
    await callback.message.answer('THEY LAUNCH WARHEADS INTO ENGLAND 31%')
    await asyncio.sleep(0.5)
    await callback.message.answer('THEY LAUNCH WARHEADS INTO ENGLAND 46%')
    await asyncio.sleep(3)
    await callback.message.answer('THEY LAUNCH WARHEADS INTO ENGLAND 99%')
    await callback.message.answer('THEY LAUNCH WARHEADS INTO ENGLAND 100%')
    await callback.message.reply('☢️WARHEAD SUCCESSFULLY LAUNCHED!')
    await asyncio.sleep(9)
    await callback.message.reply("💥 Oh no she was shot down 😭")


############################## УДОЛЯТОР СЫЛОК #################################

@dp.message_handler(lambda message: message.entities != [] and message.chat.id)
async def delete_messages(message: types.Message):
    for entity in message.entities:
        if entity.type in ["url", "text_link"]:
            await bot.delete_message(message.from_user.id, message.message_id)
            break


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)