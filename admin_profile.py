import shelve
from Task import Task
import telebot, time
import staff as s
import markups as m

with shelve.open('adm_prof') as db:
    if 'profit' in db:
        pass
    else:
        db['profit'] = 0.0
        
with shelve.open('adm_prof', writeback=True) as db:
    if 'pay_amount' in db:
        pass
    else:
        db['pay_amount'] = 0
    
task = Task()
bot = task.bot

def adminMenu(chat_id):
    pass

def viewTypes(message):
    text = message.text
    chat_id = message.chat.id
    staff_types = s.viewTypes(text)
    bot.send_message(chat_id, f'Доступные разделы в категории {text}: \n' + ', '.join(staff_types))