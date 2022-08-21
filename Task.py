import telebot

class Task():
    isRunning = False
    isStaffOpen = False
    isPay = False
    yooacc_number = '410014635035950'
    yootoken = ''
    token = ''
    support_message = 'В разработке...'
    bot_start_message = 'Привет ✌️! Я маркет-бот Name.\nДля взаимодействия со мной используй кнопочки ниже.\nПеред покупкой обязательно прочти правила!'
    rules_message = 'В разработке...'
    admins = ['DemonikJR', '']
    bot = telebot.TeleBot(token)
