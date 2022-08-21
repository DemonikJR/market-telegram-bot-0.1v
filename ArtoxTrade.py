import telebot, time
from Task import Task
import markups as m
import staff as s
import shelve
import yoomoney_for_bot as ym
import rand_label as rl
import admin_profile as p

task = Task()
bot = task.bot

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    if not task.isRunning:
        chat_id = message.chat.id
        text = message.text
        task.isRunning = True
        msg = bot.send_message(chat_id, task.bot_start_message, reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, menu_handler)
  
@bot.message_handler(content_types=['text'])
def menu_handler(message):
    if task.isRunning:
        if task.isStaffOpen:
            staff_open_msg = bot.send_message(message.chat.id, 'Закройте предыдущее меню товаров!')
            time.sleep(1.1)
            bot.delete_message(message.chat.id, message.message_id)         
            bot.delete_message(staff_open_msg.chat.id, staff_open_msg.message_id)  
        else:
            global msg, user_msg
            text = message.text.lower()
            chat_id = message.chat.id
            if text == 'правила':
                msg = bot.send_message(chat_id, task.rules_message)
            elif text == 'поддержка':
                msg = bot.send_message(chat_id, task.support_message)
            elif text == '/adm':
                if message.from_user.username in task.admins:
                    with shelve.open('adm_prof') as db:
                        user_msg = message
                        msg = bot.send_message(chat_id, '⭐️Админ панель⭐️\n' + f'💵Профит: {db["profit"]} руб.\n' + f'🛄Совершено покупок: {db["pay_amount"]}', reply_markup=m.admin_buttons())
                else:
                    msg = bot.send_message(chat_id, '❌Ошибка: У вас недостаточно прав!❌')
            elif text == 'товары':
                user_msg = message
                task.isStaffOpen = True
                msg = bot.send_message(chat_id, '📃Категории📃', reply_markup=m.cat_buttons())                
            else:
                msg = bot.send_message(chat_id, 'Извините, я вас не понял :(')
    else:
        bot.send_message(message.chat.id, 'Перезапустите бота командой /start!')
        
@bot.callback_query_handler(func=lambda call:True)
def staff_handler(call):
    if task.isRunning:
        global msg, user_msg
        text = call.data
        chat_id = call.message.chat.id
        message_id = msg.message_id         
        if not task.isPay:
            if text in s.viewCategores():
                bot.edit_message_text('📃Доступные разделы📃', chat_id, message_id, reply_markup=m.type_buttons(text))
            elif '∑' in text and text.split('∑')[0] in s.viewTypes(text.split('∑')[1]) and len(text.split('∑')) == 2:
                if s.availableType(text.split('∑')[1], text.split('∑')[0]) == True:
                    with shelve.open('staff/' + text.split('∑')[1]) as db:
                        bot.edit_message_text(f'📃Описание товара: {db[text.split("∑")[0]+"_desc"]}\n💵Стоимость: {db[text.split("∑")[0]+"_cost"]}', chat_id, message_id, reply_markup=m.item_buttons(text.split("∑")[1], text.split("∑")[0]))
                else:
                    bot.edit_message_text('❌Товар отсутствует в ассортименте!❌', chat_id, message_id, reply_markup=m.back_buttons())
            elif '∑' in text and text.split('∑')[0] == 'buy' and len(text.split('∑')) == 3:
                task.isPay = True
                global pay_desc
                pay_desc = ym.payment(text.split('∑')[1], text.split('∑')[2], rl.rand_label())
                bot.edit_message_reply_markup(chat_id,  message_id, reply_markup=m.payment_buttons(text.split('∑')[1], text.split('∑')[2], chat_id, pay_desc[0]))
            elif text == 'menu':
                bot.delete_message(chat_id, call.message.message_id)
                bot.delete_message(chat_id, user_msg.message_id)
                task.isStaffOpen = False
            elif text == 'staff':
                bot.edit_message_text('Список товаров:', chat_id, message_id, reply_markup=m.cat_buttons())
            elif text == 'addcategory':
                msg = bot.send_message(chat_id, 'Введите название категории: ')
                bot.register_next_step_handler(msg, s.addCategory)
            elif text == 'addtype':
                msg = bot.send_message(chat_id, 'Введите название категории: ')
                bot.register_next_step_handler(msg, s.addTypeToCategory)
            elif text == 'additem':
                msg = bot.send_message(chat_id, 'Введите название категории: ')
                bot.register_next_step_handler(msg, s.addItemToType)
            elif text == 'viewcategory':
                msg = bot.send_message(chat_id, 'Доступные категории: ' + ', '.join(s.viewCategores()))
            elif text == 'viewtypes':
                msg = bot.send_message(chat_id, 'Введите название категории: ')
                bot.register_next_step_handler(msg, p.viewTypes)
            elif text == 'changedesc':
                msg = bot.send_message(chat_id, 'Введите название категории: ')
                bot.register_next_step_handler(msg, s.changeTypeDesc)
            elif text == 'changecost':
                msg = bot.send_message(chat_id, 'Введите название категории: ')
                bot.register_next_step_handler(msg, s.changeTypeCost)
            elif text == 'delcategory':
                msg = bot.send_message(chat_id, 'Введите название категории: ')
                bot.register_next_step_handler(msg, s.delCategory)
            elif text == 'deltype':
                msg = bot.send_message(chat_id, 'Введите название категории: ')
                bot.register_next_step_handler(msg, s.delType)
            elif text == 'adm_close':
                bot.delete_message(chat_id, call.message.message_id)
                bot.delete_message(chat_id, user_msg.message_id)                
            else:
                msg = bot.send_message(chat_id, 'Я вас не понял! Используйте кнопки!')
        else:       
            if text == 'cancelpay':
                task.isPay = False
                bot.delete_message(chat_id, call.message.message_id)
                bot.delete_message(chat_id, user_msg.message_id)
                task.isStaffOpen = False
            elif text == 'checkpay':
                isPayAccepted = ym.checkPayment(pay_desc[1], pay_desc[2])
                if isPayAccepted:
                    bot.send_message(chat_id, 'Спасибо за покупку!\nВаш товар: ' + s.giveItem(pay_desc[3], pay_desc[4]))
                    bot.delete_message(chat_id, call.message.message_id)
                    bot.delete_message(chat_id, user_msg.message_id)
                    task.isPay = False
                    task.isStaffOpen = False
                else:
                    checkpay_msg = bot.send_message(chat_id, 'Совершите оплату!\nЕсли вы совершили оплату, а бот так и не находит её, обратитесь в поддержку.')
                    time.sleep(1)
                    bot.delete_message(chat_id, checkpay_msg.message_id)
            else:
                pay_open_msg = bot.send_message(call.message.chat.id, 'Завершите предыдущую покупку или отмените её командой /cancelpay!')
                time.sleep(1.1)
                bot.delete_message(chat_id, call.message.message_id)
                bot.delete_message(pay_open_msg.chat.id, pay_open_msg.message_id)                
    else:
        bot.send_message(call.message.chat.id, 'Перезапустите бота командой /start!')
bot.polling(non_stop=True)
