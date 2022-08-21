import shelve
import os
from Task import Task
import telebot, time

task = Task()
bot = task.bot

def addCategory(message):
    text = message.text
    chat_id = message.chat.id
    if os.path.isfile('staff/' + text + '.dat'):
        bot.send_message(chat_id, f'Ошибка: категория {text} уже существует!')
    else:
        db = shelve.open('staff/' + text)
        db.close()
        bot.send_message(chat_id, f'Категория {text} успешно добавлена!')
    
def delCategory(message):
    text = message.text
    chat_id = message.chat.id
    if os.path.isfile('staff/' + text + '.dat'):
        os.remove('staff/' + text + '.dat')
        os.remove('staff/' + text + '.dir')
        os.remove('staff/' + text + '.bak')
        bot.send_message(chat_id, f'Категория {text} успешно удалена!')
    else:
        bot.send_message(chat_id, f'Ошибка: категория {text} не существует!')
        
def delType2(message, category):
    text = message.text
    chat_id = message.chat.id    
    if text in viewTypes(category):
        with shelve.open('staff/' + category, writeback=True) as db:
            del db[text]
            del db[text+'_cost']
            del db[text+'_desc']
    else:
        bot.send_message(message.chat.id, f'Ошибка: данный раздел отсутствует в категории {category}!')
        
def delType(message):
    text = message.text
    chat_id = message.chat.id
    if os.path.isfile('staff/' + text + '.dat'):
        msg = bot.send_message(chat_id, 'Введите раздел категории: ')
        bot.register_next_step_handler(msg, delType2, text)
    else:
        bot.send_message(chat_id, f'Ошибка: категория {text} не существует!')    

def changeTypeDesc2(message, staff_type, category):
    with shelve.open('staff/' + category, writeback=True) as db:
        db[staff_type+'_desc'] = message.text
    bot.send_message(message.chat.id, f'Описание для товаров в разделе {staff_type} установлено!') 
        
def changeTypeDesc1(message, category):
    if message.text not in viewTypes(category):
        bot.send_message(message.chat.id, f'Ошибка: данный раздел отсутствует в категории {category}!')
    else:
        msg = bot.send_message(message.chat.id, f'Введите описание для раздела {message.text}:')
        bot.register_next_step_handler(msg, changeTypeDesc2, message.text, category)

def changeTypeDesc(message):
    chat_id = message.chat.id
    category = message.text
    if os.path.isfile('staff/' + category + '.dat'):
        msg = bot.send_message(chat_id, 'Введите раздел категории: ')
        bot.register_next_step_handler(msg, changeTypeDesc1, category)
    else:
        bot.send_message(chat_id, f'Ошибка: {category} не является категорией!')
    
def changeTypeCost2(message, staff_type, category):
    with shelve.open('staff/' + category, writeback=True) as db:
        db[staff_type+'_cost'] = int(message.text)
    bot.send_message(message.chat.id, f'Цена для товаров в разделе {staff_type} установлена!')
        
def changeTypeCost1(message, category):
    if message.text not in viewTypes(category):
        bot.send_message(message.chat.id, f'Ошибка: данный раздел отсутствует в категории {category}!')
    else:
        msg = bot.send_message(message.chat.id, f'Введите новую цену для раздела {message.text}:')
        bot.register_next_step_handler(msg, changeTypeCost2, message.text, category)

def changeTypeCost(message):
    chat_id = message.chat.id
    category = message.text
    if os.path.isfile('staff/' + category + '.dat'):
        msg = bot.send_message(chat_id, 'Введите раздел категории: ')
        bot.register_next_step_handler(msg, changeTypeCost1, category)
    else:
        bot.send_message(chat_id, f'Ошибка: {category} не является категорией!')

def addTypeDesc(message, staff_type, category):
    with shelve.open('staff/' + category, writeback=True) as db:
        db[staff_type+'_desc'] = message.text
    bot.send_message(message.chat.id, f'Описание для товаров в разделе {staff_type} установлено!')    
        
def addTypeCost(message, staff_type, category):
    with shelve.open('staff/' + category, writeback=True) as db:
        db[staff_type+'_cost'] = int(message.text)
    msg = bot.send_message(message.chat.id, f'Цена для товаров в разделе {staff_type} установлена!\nЗадайте описание товарам этого раздела: ')
    bot.register_next_step_handler(msg, addTypeDesc, staff_type, category)
    
def addTypeToCategory2(message, category):
    chat_id = message.chat.id
    text = message.text
    with shelve.open('staff/' + category, writeback=True) as db:
        if text in db:
            bot.send_message(chat_id, f'Ошибка: раздел {text} уже существует в категории {category}!')
        else:
            db[text] = []
            msg = bot.send_message(chat_id, f'Раздел {text} успешно добавлен в категорию {category}!\nТеперь укажите цену для товара в этом разделе: ')
            bot.register_next_step_handler(msg, addTypeCost, text, category)
        
def addTypeToCategory(message):
    chat_id = message.chat.id
    category = message.text
    if os.path.isfile('staff/' + category + '.dat'):
        msg = bot.send_message(chat_id, 'Введите раздел категории: ')
        bot.register_next_step_handler(msg, addTypeToCategory2, category)
    else:
        bot.send_message(chat_id, f'Ошибка: {category} не является категорией!')
        
def addItemToType3(message, staff_type, category):
    with shelve.open('staff/' + category, writeback=True) as db:
        db[staff_type].extend(message.text.split('\n'))
    bot.send_message(message.chat.id, f'Раздел {staff_type} успешно пополнен новым товаром!')
        
def addItemToType2(message, category):
    chat_id = message.chat.id
    text = message.text    
    with shelve.open('staff/' + category, writeback=True) as db:
        if text in db:
            staff_type = text
            msg = bot.send_message(chat_id, 'Введите данные: ')
            bot.register_next_step_handler(msg, addItemToType3, staff_type, category)
        else:
            bot.send_message(chat_id, f'Ошибка: раздела {text} не существует!\nСначала добавьте его с помощью команды /addtype!')
    
def addItemToType(message):
    chat_id = message.chat.id
    category = message.text
    if os.path.isfile('staff/' + category + '.dat'):
        msg = bot.send_message(chat_id, 'Введите вид товара: ')
        bot.register_next_step_handler(msg, addItemToType2, category)
    else:
        bot.send_message(chat_id, f'Ошибка: {message} не является категорией!')
            
def viewCategores():
    categores = [i[:-4] for i in os.listdir('staff/') if '.dat' in i]
    return categores

def viewTypes(category):
    with shelve.open('staff/' + category) as db:
        staff_types = [i for i in db if '_cost' not in i and '_desc' not in i]
    return staff_types

def availableType(category, staff_type):
    with shelve.open('staff/' + category) as db:
        if len(db[staff_type]) > 0:
            return True
        else:
            return False
        
def checkCost(staff_type, category):
    with shelve.open('staff/' + category) as db:
        return db[staff_type+'_cost']
        
def giveItem(staff_type, category):
    with shelve.open('staff/' + category, writeback=True) as db:
        item = db[staff_type].pop()
        print(item)
    return item