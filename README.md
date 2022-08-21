<h1 align="center">MarketTelegramBot1.0v-release</h1>
<h3 align="center">Бот для автопродаж в телеграме</h3>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

Бот для автопродаж в телеграме с удобной навигацией и админ-панелью, для оплаты используется API YooMoney и идентифицированный кошелёк YooMoney, можно принимать оплату без ИП. 
Покупка делится на 4 этапа:
1. Выбор категории (в виде inline кнопок высвечиваются доступные категории).
2. Выбор раздела в категории (в виде inline кнопок высвечиваются доступные разделы в этой категории).
3. Если товар в наличии:
  i. Высвечивается описание раздела и стоимость, inline кнопка на получение ссылки для оплаты.
  ii. Меню оплаты с тремя кнопками: отменить оплату, проверить оплату и перейти на форму оплаты.
  iii. Выдача товара.
  
4. Если товар отсутствует - выводится сообщение, что товара нет в ассортименте.

Также присутствует удобная админ-панель с меню в виде inline кнопок