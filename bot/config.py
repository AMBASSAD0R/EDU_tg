from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '2104313952:AAFb6dtxWE8d2vFdEi1k2ZYg81xwNCMz_gA'
button_hi = KeyboardButton('Каталог заданий')
greet_kb1 = ReplyKeyboardMarkup()
greet_kb2 = ReplyKeyboardMarkup()
greet_kb2.add(ReplyKeyboardMarkup('Интенсив'))
greet_kb2.add(ReplyKeyboardMarkup('Задача дня'))
for i in range(1, 28):
    but = KeyboardButton(str(i))
    greet_kb1.add(but)
greet_kb1.add(ReplyKeyboardMarkup('В начало'))
greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)
greet_kb.add(KeyboardButton('Тренировка'))
greet_kb.add(KeyboardButton('Статистика'))
greet_kb2.add(ReplyKeyboardMarkup('В начало'))
