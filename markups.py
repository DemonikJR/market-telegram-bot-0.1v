from telebot import types

source_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
item1 = types.KeyboardButton('Правила')
item2 = types.KeyboardButton('Поддержка')
item3 = types.KeyboardButton('Товары')
source_markup.add(item1, item2, item3)

staff_markup = types.InlineKeyboardMarkup(row_width=2)
staff1 = types.InlineKeyboardButton(text='VPN', callback_data='vpn')
staff2 = types.InlineKeyboardButton(text='BrawlStars Gems', callback_data='bs')
staff3 = types.InlineKeyboardButton(text='Назад', callback_data='menu')
staff_markup.add(staff1, staff2, staff3)

item_back_markup = types.InlineKeyboardMarkup()
item_back1 = types.InlineKeyboardButton(text='<< В меню', callback_data='menu')
item_back2 = types.InlineKeyboardButton(text='< К товарам', callback_data='staff')
item_back_markup.add(item_back1, item_back2)
