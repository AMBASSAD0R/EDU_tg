from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import WorkDB
from config import TOKEN, greet_kb, greet_kb1
from datetime import datetime
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = WorkDB('../database.db')


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    if not db.check_user(msg.from_user.id):
        db.create_user(msg.from_user.id, datetime.now(), datetime.now())
    await msg.reply("Привет!\nЭто бот по подготовке к ЕГЭ по информатике!\n", reply_markup=greet_kb)


@dp.message_handler(commands=['description'])
async def process_help_command(message: types.Message):
    await message.reply("Этот бот поможет тебе подготовится к ЕГЭ по информатике.\nВыполняя задания каждый день, ты ГАРАНТИРОВАНО получишь высокий балл!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    db.update_date_use(msg.from_user.id, datetime.now())
    try:
        task = db.get_task(msg.text)
        lst = [j for i in task for j in i]
        print(lst)
    except:
        await message.reply("Приносим извинения, такого задания нет.")
    try:
        if lst[-1] != None:  # Если в задание есть фото - отправляем
            await bot.send_photo(msg.from_user.id, lst[-1])
        if lst[-2] != None:  # Если в задание есть файл - отправляем
            await bot.send_file(msg.from_user.id, lst[-2])
    except:  
        pass
    try:
        await bot.send_message(msg.from_user.id, lst[3])
    except:
        pass
    
    # Обработка клавиатуры
    
    if msg.text == 'Каталог заданий':
        await bot.send_message(msg.from_user.id, text='Вы попали в каталог задач', reply_markup=greet_kb1)
    if msg.text == 'В начало':
        await bot.send_message(msg.from_user.id, text='Вы вернулись в меню', reply_markup=greet_kb)
    if msg.text in [i for i in range(1, 28)]:
        pass
    if msg.text == 'Статистика':
        pass


if __name__ == '__main__':
    executor.start_polling(dp)
