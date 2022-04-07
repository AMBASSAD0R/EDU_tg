import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import *
from db import WorkDB
from datetime import datetime
import random
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import matplotlib.pyplot as plt

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = WorkDB('../database.db')


def get_user_rating(user_id):
    try:
        return int(db.get_task_сol_true_answer(user_id) / (
                db.get_task_сol_true_answer(user_id) + db.get_task_col_false_answer(user_id)) * 100)
    except:
        return 0


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    if not db.check_user(msg.from_user.id):
        db.create_user(msg.from_user.id, msg.from_user.username)
        db.add_user_in_user_task(msg.from_user.id, -100)
        db.create_static(msg.from_user.id, 0, 0, str(['0'] * 27), 0)
        suitable_tasks = db.get_rating_diapason(0, 20)
        id_suitable_tasks = []
        for task in suitable_tasks:
            id_suitable_tasks.append(list(task)[0])
        random.shuffle(id_suitable_tasks)
        db.create_user_train(msg.from_user.id, f'{id_suitable_tasks[:5]}')
    await msg.reply("Привет!\nЭто бот по подготовке к ЕГЭ по информатике!\n", reply_markup=greet_kb)


@dp.message_handler(commands=['description'])
async def process_help_command(message: types.Message):
    await message.reply("Этот бот поможет тебе подготовится к ЕГЭ по информатике.\nВыполняя задания каждый день, ты\
     ГАРАНТИРОВАНО получишь высокий балл!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    # db.update_date_use(msg.from_user.id, datetime.now())
    try:
        if len(list(map(int, db.get_users_train(msg.from_user.id)[2:-2].split(', ')))) == 0:
            user_rating = get_user_rating(msg.from_user.id)
            suitable_tasks = db.get_rating_diapason(100 - user_rating - 20, 100 - user_rating + 20)
            id_suitable_tasks = []
            for task in suitable_tasks:
                id_suitable_tasks.append(list(task)[0])
            random.shuffle(id_suitable_tasks)
            db.update_tasks_id(msg.from_user.id, f'{id_suitable_tasks[:5]}')
    except:
        user_rating = get_user_rating(msg.from_user.id)
        suitable_tasks = db.get_rating_diapason(100 - user_rating - 20, 100 - user_rating + 20)
        id_suitable_tasks = []
        for task in suitable_tasks:
            id_suitable_tasks.append(list(task)[0])
        random.shuffle(id_suitable_tasks)
        db.update_tasks_id(msg.from_user.id, f'{id_suitable_tasks[:5]}')
    # Обработка клавиатуры

    if msg.text == 'Каталог заданий':
        await bot.send_message(msg.from_user.id, text='Вы попали в каталог задач', reply_markup=greet_kb1)
    elif msg.text == 'Рейтинг пользователей':
        users_raiting = db.get_top_rating()
        users_raiting.sort(key=lambda x: x[1])
        users_raiting = users_raiting[::-1]
        print(users_raiting)
        user_id = [x for x in users_raiting if x[0] == msg.from_user.id]
        user_place = users_raiting.index(user_id[0])
        sp = []
        print()
        for j, i in enumerate(users_raiting[:11]):
            if j == 0:
                sp.append(f'🥇 {j + 1}. {db.get_username(i[0])[1:-1]} : {i[1]}')
            elif j == 1:
                sp.append(f'🥈 {j + 1}. {db.get_username(i[0])[1:-1]} : {i[1]}')
            elif j == 2:
                sp.append(f'🥉 {j + 1}. {db.get_username(i[0])[1:-1]} : {i[1]}')
            else:
                sp.append(f'🔥 {j + 1}. {db.get_username(i[0])[1:-1]} : {i[1]}')
        sp.append('\t .')
        sp.append('\t .')
        sp.append('\t .')
        if user_place == 0:
            sp.append(f'🥇 {user_place + 1}. {db.get_username(user_id[0][0])[1:-1]}: {user_id[0][1]}')
        elif user_place == 1:
            sp.append(f'🥈 {user_place + 1}. {db.get_username(user_id[0][0])[1:-1]}: {user_id[0][1]}')
        elif user_place == 2:
            sp.append(f'🥉 {user_place + 1}. {db.get_username(user_id[0][0])[1:-1]}: {user_id[0][1]}')
        elif 10 <= user_place < 2:
            sp.append(f'🔥 {user_place + 1}. {db.get_username(user_id[0][0])[1:-1]} : {user_id[0][1]}')
        else:
            sp.append(f'💡 {user_place + 1}. {db.get_username(user_id[0][0])[1:-1]} : {user_id[0][1]}')
        t = "\n".join(sp)
        await bot.send_message(msg.from_user.id, text=f'{t}', reply_markup=kb_task)

    elif msg.text == 'Статистика':
        username = msg.from_user.username
        col_resh1 = list(map(int, db.get_task_col_resh(msg.from_user.id)[3:-3].split("', '")))
        col_resh2 = []
        for i in range(len(col_resh1)):
            col_resh2.append(f' {int(i) + 1} ')
        # await bot.send_message(msg.from_user.id, text=f'{username}')
        # await bot.send_message(msg.from_user.id, text=f'Процент решения задач: {text1}')
        plt.bar(col_resh2, col_resh1)
        print(col_resh1)
        print(col_resh2)
        plt.savefig(f'graphics/{msg.from_user.id}.jpg')
        await bot.send_photo(msg.from_user.id, open(f'graphics/{msg.from_user.id}.jpg', 'rb'))
        os.remove(f'graphics/{msg.from_user.id}.jpg')
        try:
            percent = int(db.get_task_сol_true_answer(msg.from_user.id) / (
                    db.get_task_сol_true_answer(msg.from_user.id) + db.get_task_col_false_answer(
                msg.from_user.id)) * 100)
            if percent < 50:
                await bot.send_message(msg.from_user.id,
                                       text=f'Процент решения задач: {percent}% 🆘‼')
            elif 50 <= percent < 80:
                await bot.send_message(msg.from_user.id,
                                       text=f'Процент решения задач: {percent}% ☣')
            elif 80 <= percent:
                await bot.send_message(msg.from_user.id,
                                       text=f'Процент решения задач: {percent}% 💯')
        except:
            await bot.send_message(msg.from_user.id,
                                   text=f'Процент решения задач: 0% 🆘‼')

    elif msg.text == 'Тренировка':
        # user_rating = get_user_rating(msg.from_user.id)
        # suitable_tasks = db.get_rating_diapason(user_rating - 20, user_rating + 20)
        # id_suitable_tasks = []
        # for task in suitable_tasks:
        #    id_suitable_tasks.append(list(task)[0])
        # task_id = id_suitable_tasks[0]
        # print(db.get_users_train(msg.from_user.id))
        sp = list(map(int, db.get_users_train(msg.from_user.id)[2:-2].split(', ')))
        print(sp)
        task_id = random.choice(sp)
        db.update_task_id(msg.from_user.id, task_id)
        task = db.get_task(task_id)
        data = [j for i in task for j in i]
        print(data)
        rating = data[-1]
        print('s')
        print(data)
        if data[2] == 10 or data[2] == 9 or data[2] == 26 or data[2] == 27:
            try:
                if data[-4]:  # Если в задание есть фото - отправляем
                    await bot.send_document(msg.from_user.id, data[-4])
            except Exception as e:
                print(e)
        else:
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
        if data[2] == 10 or data[2] == 9 or data[2] == 26 or data[2] == 27:
            try:
                if data[-4]:  # Если в задание есть фото - отправляем
                    await bot.send_document(msg.from_user.id, data[-4], caption='')
            except Exception as e:
                print(e)
        else:
            try:
                if data[-4]:  # Если в задание есть фото - отправляем
                    await bot.send_photo(msg.from_user.id, data[-4])
                if data[-5]:  # Если в задание есть файл - отправляем
                    await bot.send_document(msg.from_user.id, data[-5])
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
        db.update_user_rating(msg.from_user.id, db.get_task_rating(db.get_task_id_user(msg.from_user.id)))
        task_id = db.get_task_id_user(msg.from_user.id)
        sp = list(map(int, db.get_users_train(msg.from_user.id)[2:-2].split(', ')))
        if int(task_id) in sp:
            sp.remove(int(task_id))
        db.update_tasks_id(msg.from_user.id, str(sp))
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
