from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import WorkDB
from config import *
from datetime import datetime
import random

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = WorkDB('../database.db')


def get_user_rating(user_id):
    return int(db.get_task_сol_true_answer(user_id) / (
            db.get_task_сol_true_answer(user_id) + db.get_task_col_false_answer(user_id)) * 100)


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    if not db.check_user(msg.from_user.id):
        db.create_user(msg.from_user.id, datetime.now(), datetime.now())
        db.add_user_in_user_task(msg.from_user.id, -100)
        db.create_static(msg.from_user.id, 0, 0, str(['0'] * 27))
        db.create_user_train(msg.from_user.id, '[]')
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
    elif msg.text == 'Статистика':
        username = msg.from_user.username
        col_resh1 = db.get_task_col_resh(msg.from_user.id)[3:-3].split("', '")
        col_resh2 = []
        for j, i in enumerate(col_resh1):
            col_resh2.append(f'Количевство решения №{j + 1}: {i}')
        text1 = '\n'.join(col_resh2)
        await bot.send_message(msg.from_user.id, text=f'{username}')
        await bot.send_message(msg.from_user.id, text=f'Процент решения задач: {text1}')
        try:
            await bot.send_message(msg.from_user.id,
                                   text=f'Процент решения задач: {int(db.get_task_сol_true_answer(msg.from_user.id) / (db.get_task_сol_true_answer(msg.from_user.id) + db.get_task_col_false_answer(msg.from_user.id)) * 100)}')
        except:
            await bot.send_message(msg.from_user.id,
                                   text=f'Процент решения задач: 0%')

    elif msg.text == 'Тренировка':
        user_rating = get_user_rating(msg.from_user.id)
        suitable_tasks = db.get_rating_diapason(user_rating - 20, user_rating + 20)
        id_suitable_tasks = []
        for task in suitable_tasks:
            id_suitable_tasks.append(list(task)[0])
        id_task = id_suitable_tasks[0]
        await bot.send_message(msg.from_user.id,
                               )




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
        rating = data[-1]
        print(data)
        try:
            if data[-4]:  # Если в задание есть фото - отправляем
                await bot.send_photo(msg.from_user.id, data[-4])
            if data[-5]:  # Если в задание есть файл - отправляем
                await bot.send_message(msg.from_user.id, data[-5])
        except Exception as e:
            print(e)
        try:
            await bot.send_message(msg.from_user.id, data[3], reply_markup=kb_task)
        except:
            pass
        await bot.send_message(msg.from_user.id, f'Процент решаемости задачи: {rating}%', reply_markup=kb_task)
    elif db.get_task_id_user(msg.from_user.id) != -100 and msg.text == str(
            db.get_task_answer(db.get_task_id_user(msg.from_user.id))[0][0]):
        await bot.send_message(msg.from_user.id, text='Правильный ответ ✅', reply_markup=greet_kb1)
        task_id = db.get_task_id_user(msg.from_user.id)
        db.update_task_num_attempts(task_id)
        db.update_task_rights_solves(task_id)
        db.update_task_rating(task_id)
        db.update_task_сol_true_answer(msg.from_user.id)
        print(db.get_task_answer(task_id)[0][0])
        col_resh = list(map(int, db.get_task_col_resh(msg.from_user.id)[3:-3].split("', '")))
        number_id = db.get_task_number_id(task_id)
        col_resh[number_id - 1] += 1
        print(col_resh)
        db.update_task_col_resh(msg.from_user.id, str(list(map(str, col_resh))))
        db.update_task_id(msg.from_user.id, -100)

    elif db.get_task_id_user(msg.from_user.id) != -100 and msg.text != \
            str(db.get_task_answer(db.get_task_id_user(msg.from_user.id))[0][0]):
        await bot.send_message(msg.from_user.id, text='Неправильный ответ ❌')
        # print(db.get_task_answer(db.get_task_id_user(msg.from_user.id))[0][0])
        task_id = db.get_task_id_user(msg.from_user.id)
        db.update_task_num_attempts(task_id)
        db.update_task_rating(task_id)
        db.update_task_col_false_answer(msg.from_user.id)
        print(db.get_statistic(msg.from_user.id))
        # db.update_col_false(msg.from_user.id, )


if __name__ == '__main__':
    executor.start_polling(dp)
