from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import WorkDB
from config import TOKEN
from datetime import datetime

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = WorkDB('./database.db')


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    if not db.check_user(msg.from_user.id):
        db.create_user(msg.from_user.id, datetime.now(), datetime.now())
    await msg.reply("Привет!\nНапиши мне что-нибудь!")


@dp.message_handler(commands=['start', 'help'])
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    db.update_date_use(msg.from_user.id, datetime.now())
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)
