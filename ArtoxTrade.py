import telebot
from Task import Task
import markups as m


TOKEN = '5332989623:AAFlZc99FM8_lFEBfyClZbkuQQqPaltsabo'
bot = telebot.TeleBot(TOKEN)
task = Task()


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    if not task.isRunning:
        chat_id = message.chat.id
        text = message.text
        msg = bot.send_message(chat_id, 'Сап! Я маркет-бот ArtoxTrade. Для взаимодействия со мной используй кнопочки ниже. Перед покупкой обязательно прочти правила!', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, menu_handler)
        task.isRunning = True
    
def menu_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    if text == 'правила':
        msg = bot.send_message(chat_id, 'В разработке...')
        bot.register_next_step_handler(msg, menu_handler)
    elif text == 'поддержка':
        msg = bot.send_message(chat_id, 'Для связи с создателем используй Discord - 悪魔(DemonikJR)#9500')
    elif text == 'товары':
        msg = bot.send_message(chat_id, 'Список товаров:')
        
    else:
        msg = bot.send_message(chat_id, 'Извините, я вас не понял :(')
        bot.register_next_step_handler(msg, menu_handler)
        return



bot.polling(non_stop=True)