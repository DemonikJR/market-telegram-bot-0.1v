from yoomoney import Quickpay
from Task import Task
import staff as s
from yoomoney import Client
import shelve

task = Task()
bot = task.bot
yootoken = task.yootoken
yooacc_number = task.yooacc_number
client = Client(yootoken)


def payment(category, staff_type, chat_id):
    quickpay = Quickpay(
        receiver=yooacc_number,
        quickpay_form="shop",
        targets="Оплата товара в ArtoxShop",
        paymentType="SB",
        sum=s.checkCost(staff_type, category),
        label=chat_id
    )
    return [quickpay.redirected_url, chat_id, s.checkCost(staff_type, category), staff_type, category]
    
def checkPayment(chat_id, cost):
    history = client.operation_history(label=chat_id)
    history.next_record
    success_status = False
    for operation in history.operations:
        print(operation.amount, '\n', operation.status)
        #if operation.amount == float(cost)-float(cost)*3/100:
            #success_amount = True
        #else:
            #success_amount = False
        if operation.status == 'success':
            success_status = True
            with shelve.open('adm_prof', writeback=True) as db:
                db['profit'] += operation.amount
            with shelve.open('adm_prof', writeback=True) as db:
                db['pay_amount'] += 1
        break
    if success_status == True:
        return True
    else:
        return False