import telebot, time
from Task import Task
import markups as m

task = Task()
TOKEN = task.token
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    if not task.isRunning:
        chat_id = message.chat.id
        text = message.text
        task.isRunning = True
        msg = bot.send_message(chat_id, 'Сап! Я маркет-бот ArtoxTrade. Для взаимодействия со мной используй кнопочки ниже. Перед покупкой обязательно прочти правила!', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, menu_handler)
  
@bot.message_handler(content_types=['text'])
def menu_handler(message):
    if task.isRunning:
        if task.isStaffOpen:
            staff_open_msg = bot.send_message(message.chat.id, 'Закройте предыдущее меню товаров!')
            bot.delete_message(message.chat.id, message.message_id)
            time.sleep(1.1)
            bot.delete_message(staff_open_msg.chat.id, staff_open_msg.message_id)  
        else:
            global msg, user_msg
            text = message.text.lower()
            chat_id = message.chat.id
            if text == 'правила':
                msg = bot.send_message(chat_id, 'В разработке...')
            elif text == 'поддержка':
                msg = bot.send_message(chat_id, 'Способы связи с создателем: \nDiscord - 悪魔(DemonikJR)#9500\nTG - @DemoniKJR')
            elif text == 'товары':
                user_msg = message
                task.isStaffOpen = True
                msg = bot.send_message(chat_id, 'Список товаров:', reply_markup=m.staff_markup)                
            else:
                msg = bot.send_message(chat_id, 'Извините, я вас не понял :(')
    else:
        bot.send_message(message.chat.id, 'Перезапустите бота командой /start!')
        
@bot.callback_query_handler(func=lambda call:True)
def staff_handler(call):
    if task.isRunning:   
        global msg
        text = call.data.lower()
        chat_id = call.message.chat.id
        message_id = msg.message_id
        if text == 'vpn':
            bot.edit_message_text('Доступные сервисы: ', chat_id, message_id, reply_markup=m.item_back_markup)
        elif text == 'bs':
            bot.edit_message_text('Доступные сервисы: ', chat_id, message_id, reply_markup=m.item_back_markup)
        elif text == 'menu':
            bot.delete_message(chat_id, call.message.message_id)
            bot.delete_message(chat_id, user_msg.message_id)
            task.isStaffOpen = False
        elif text == 'staff':
            bot.edit_message_text('Список товаров:', chat_id, message_id, reply_markup=m.staff_markup)
        else:
            msg = bot.send_message(chat_id, 'Я вас не понял! Используйте кнопки!')
    else:
        bot.send_message(call.message.chat.id, 'Перезапустите бота командой /start!')    
bot.polling(non_stop=True)
