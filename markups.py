from telebot import types
import staff as s

source_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
item1 = types.KeyboardButton('Правила')
item2 = types.KeyboardButton('Поддержка')
item3 = types.KeyboardButton('Товары')
source_markup.add(item1, item2, item3)

def cat_buttons():
    cat_markup = types.InlineKeyboardMarkup(row_width=3)
    categores = s.viewCategores()
    for cat in categores:
        cat_markup.add(types.InlineKeyboardButton(text=cat, callback_data=cat))
    cat_back = types.InlineKeyboardButton(text='◀️Назад', callback_data='menu')
    cat_markup.add(cat_back)
    return cat_markup

def type_buttons(category):
    type_markup = types.InlineKeyboardMarkup(row_width=3)
    staff_types = s.viewTypes(category)
    for t in staff_types:
        type_markup.add(types.InlineKeyboardButton(text=t, callback_data=t+'∑'+category))
    type_back1 = types.InlineKeyboardButton(text='⏪ В меню', callback_data='menu')
    type_back2 = types.InlineKeyboardButton(text='◀️ К категориям', callback_data='staff')
    type_markup.add(type_back1, type_back2)
    return type_markup

def item_buttons(category, staff_type):
    item_markup = types.InlineKeyboardMarkup(row_width=3)
    item_buy = types.InlineKeyboardButton(text='Купить', callback_data='buy'+'∑'+category+'∑'+staff_type)
    item_back1 = types.InlineKeyboardButton(text='<< В меню', callback_data='menu')
    item_back2 = types.InlineKeyboardButton(text='< К категориям', callback_data='staff')
    item_markup.add(item_buy)
    item_markup.add(item_back1, item_back2)
    return item_markup
    
def back_buttons():
    back_markup = types.InlineKeyboardMarkup(row_width=3)
    back1 = types.InlineKeyboardButton(text='<< В меню', callback_data='menu')
    back2 = types.InlineKeyboardButton(text='< К категориям', callback_data='staff')
    back_markup.add(back1, back2)
    return back_markup

def payment_buttons(category, staff_type, chat_id, payment_url):
    payment_markup = types.InlineKeyboardMarkup(row_width=3)
    payment_check = types.InlineKeyboardButton(text='Проверить статус оплаты', callback_data='checkpay')
    payment_butt = types.InlineKeyboardButton(text='Ссылка на оплату', url=payment_url)
    payment_back = types.InlineKeyboardButton(text='Отменить покупку', callback_data='cancelpay')
    payment_markup.add(payment_check)
    payment_markup.add(payment_butt, payment_back)
    return payment_markup

def admin_buttons():
    admin_markup = types.InlineKeyboardMarkup(row_width=3)
    admin_add_cat = types.InlineKeyboardButton(text='➕Добавить категорию', callback_data='addcategory')
    admin_add_type = types.InlineKeyboardButton(text='➕Добавить раздел', callback_data='addtype')
    admin_add_item = types.InlineKeyboardButton(text='➕Пополнить ассортимент', callback_data='additem')
    admin_change_desc = types.InlineKeyboardButton(text='🔄Изменить описание раздела', callback_data='changedesc')
    admin_change_cost = types.InlineKeyboardButton(text='🔄Изменить цену товаров раздела', callback_data='changecost')
    admin_view_cat = types.InlineKeyboardButton(text='🗒Доступные категории', callback_data='viewcategory')
    admin_view_types = types.InlineKeyboardButton(text='🗒Доступные разделы', callback_data='viewtypes')
    admin_del_cat = types.InlineKeyboardButton(text='🗑Удалить категорию', callback_data='delcategory')
    admin_del_type = types.InlineKeyboardButton(text='🗑Удалить раздел', callback_data='deltype')
    admin_close = types.InlineKeyboardButton(text='Закрыть это меню', callback_data='adm_close')
    admin_markup.add(admin_add_cat, admin_add_type, admin_add_item,
                     admin_change_desc, admin_change_cost, admin_view_cat,
                     admin_view_types, admin_del_cat, admin_del_type,
                     admin_close)
    return admin_markup
