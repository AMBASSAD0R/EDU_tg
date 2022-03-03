from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import WorkDB
from config import *
from datetime import datetime
import random

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = WorkDB('database.db')


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    if not db.check_user(msg.from_user.id):
        db.create_user(msg.from_user.id, datetime.now(), datetime.now())
        db.add_user_in_user_task(msg.from_user.id, -100)
        db.create_static(msg.from_user.id, 0, 0, str(['0'] * 27))
    await msg.reply("Привет!\nЭто бот по подготовке к ЕГЭ по информатике!\n", reply_markup=greet_kb)


@dp.message_handler(commands=['description'])
async def process_help_command(message: types.Message):
    await message.reply("Этот бот поможет тебе подготовится к ЕГЭ по информатике.\nВыполняя задания каждый день, ты\
     ГАРАНТИРОВАНО получишь высокий балл!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    db.update_date_use(msg.from_user.id, datetime.now())

    # Обработка клавиатуры

    if msg.text == 'Каталог заданий':
        await bot.send_message(msg.from_user.id, text='Вы попали в каталог задач', reply_markup=greet_kb1)

    elif msg.text == 'В начало':
        await bot.send_message(msg.from_user.id, text='Вы вернулись в меню', reply_markup=greet_kb)
        db.update_task_id(msg.from_user.id, -100)

    elif msg.text in ['№' + str(i) for i in range(1, 28)]:
        task_number_ege = msg.text[1:]

        all_tasks = db.get_all_task(task_number_ege)

        index = random.choice(all_tasks)

        task_id = index[0]

        db.update_task_id(msg.from_user.id, task_id)
        task = db.get_task(task_id)

        data = [j for i in task for j in i]
        print(data)
        try:
            if data[-4]:  # Если в задание есть фото - отправляем
                await bot.send_photo(msg.from_user.id, data[-4])
            if data[-5]:  # Если в задание есть файл - отправляем
                await bot.send_document(msg.from_user.id, data[-5])
        except:
            pass
        try:
            await bot.send_message(msg.from_user.id, data[3], reply_markup=kb_task)
        except:
            pass

    elif db.get_task_id_user(msg.from_user.id) != -100 and msg.text == \
            str(db.get_task_answer(db.get_task_id_user(msg.from_user.id))[0][0]):
        await bot.send_message(msg.from_user.id, text='Правильный ответ ✅', reply_markup=greet_kb1)
        print(db.get_task_answer(db.get_task_id_user(msg.from_user.id))[0][0])
        db.update_task_id(msg.from_user.id, -100)

    elif db.get_task_id_user(msg.from_user.id) != -100 and msg.text != \
            str(db.get_task_answer(db.get_task_id_user(msg.from_user.id))[0][0]):
        await bot.send_message(msg.from_user.id, text='Неправильный ответ ❌')
        # print(db.get_task_answer(db.get_task_id_user(msg.from_user.id))[0][0])
        print(db.get_statistic(msg.from_user.id))
        # db.update_col_false(msg.from_user.id, )

    elif msg.text == 'Статистика':
        pass


if __name__ == '__main__':
    executor.start_polling(dp)
