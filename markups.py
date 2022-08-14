from telebot import types

source_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
item1 = types.KeyboardButton('Правила')
item2 = types.KeyboardButton('Поддержка')
item3 = types.KeyboardButton('Товары')
source_markup.add(item1, item2, item3)

staff_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
staff1 = types.KeyboardButton('')
staff2 = types.KeyboardButton('')
staff_markup.add(staff1, staff2)