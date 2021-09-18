from app import webhook_app

from flask import request, abort

from db.create_connection import connection, close_connection
from db.deposit_repo import DepositRepo
from db.liqpay_repo import LiqPayRepo


@webhook_app.route('/webhook_deposits', methods=['POST'])
@webhook_app.route('/webhook_deposits/', methods=['POST'])
def webhook():
    conn = connection()
    liqpay = LiqPayRepo(conn=conn)
    deposit = DepositRepo(conn=conn)
    try:
        data = request.json
        #id = data['order_id']
        id = "1"
        id = int(id)
        user_id = liqpay.deposit_get_user(id)
        amount = liqpay.deposit_get_amount(id)
        result = data['result']

        if result == 'ok':
            liqpay.deposit_set_state(id, "DONE")
            deposit.update_user_deposit(user_id=int(user_id), balance=int(amount))
        elif result == 'error':
            liqpay.deposit_set_state(id, "ERROR")

        if data['bot_channel'] is not None:
            liqpay.deposit_set_bot_channel(id=id, value=data['bot_channel'])

        if data['bot_in_contacts'] is not None:
            liqpay.deposit_set_bot_in_contacts(id=id, value=data['bot_in_contacts'])

        if data['bot_name'] is not None:
            liqpay.deposit_set_bot_name(id=id, value=data['bot_name'])

        if data['bot_url'] is not None:
            liqpay.deposit_set_bot_url(id=id, value=data['bot_url'])

        if data['href'] is not None:
            liqpay.deposit_set_href(id=id, value=data['href'])

        if data['id'] is not None:
            liqpay.deposit_set_id(id=id, value=data['id'])

        if data['result'] is not None:
            liqpay.deposit_set_result(id=id, value=data['result'])

        if data['token'] is not None:
            liqpay.deposit_set_token(id=id, value=data['token'])
    except:
        print('Cant load JSON data')
    close_connection(conn)



@webhook_app.route('/webhook_withdrawals', methods=['POST'])
@webhook_app.route('/webhook_withdrawals/', methods=['POST'])
def webhook():
    conn = connection()
    liqpay = LiqPayRepo(conn=conn)
    deposit = DepositRepo(conn=conn)
    try:
        data = request.json
        id = data['order_id']
        id = int(id)
        user_id = liqpay.withdrawal_get_user(id)
        status = data['status']
        amount = data['amount']
        if status == 'error':
            liqpay.withdrawal_set_state(id, "WRONG_DATA")
            deposit.update_user_deposit(user_id=int(user_id), balance=amount)
        elif status == 'failure':
            liqpay.withdrawal_set_state(id, "ERROR")
            deposit.update_user_deposit(user_id=int(user_id), balance=amount)
        elif status == 'success':
            pass

        if data['acq_id'] is not None:
            liqpay.withdrawal_set_acq_id(id=id, value=data['acq_id'])

        if data['action'] is not None:
            liqpay.withdrawal_set_action(id=id, value=data['action'])

        if data['agent_commission'] is not None:
            liqpay.withdrawal_set_agent_commission(id=id, value=data['agent_commission'])

        if data['amount'] is not None:
            liqpay.withdrawal_set_amount(id=id, value=data['amount'])

        if data['amount_bonus'] is not None:
            liqpay.withdrawal_set_amount_bonus(id=id, value=data['amount_bonus'])

        if data['amount_credit'] is not None:
            liqpay.withdrawal_set_amount_credit(id=id, value=data['amount_credit'])

        if data['amount_debit'] is not None:
            liqpay.withdrawal_set_amount_debit(id=id, value=data['amount_debit'])

        if data['commission_credit'] is not None:
            liqpay.withdrawal_set_commission_credit(id=id, value=data['commission_credit'])

        if data['commission_debit'] is not None:
            liqpay.withdrawal_set_commission_debit(id=id, value=data['commission_debit'])

        if data['create_date'] is not None:
            liqpay.withdrawal_set_create_date(id=id, value=data['create_date'])

        if data['currency'] is not None:
            liqpay.withdrawal_set_currency(id=id, value=data['currency'])

        if data['currency_credit'] is not None:
            liqpay.withdrawal_set_currency_credit(id=id, value=data['currency_credit'])

        if data['currency_debit'] is not None:
            liqpay.withdrawal_set_currency_debit(id=id, value=data['currency_debit'])

        if data['description'] is not None:
            liqpay.withdrawal_set_description(id=id, value=data['description'])

        if data['end_date'] is not None:
            liqpay.withdrawal_set_end_date(id=id, value=data['end_date'])

        if data['is_3ds'] is not None:
            liqpay.withdrawal_set_is_3ds(id=id, value=data['is_3ds'])

        if data['liqpay_order_id'] is not None:
            liqpay.withdrawal_set_liqpay_order_id(id=id, value=data['liqpay_order_id'])

        if data['mpi_eci'] is not None:
            liqpay.withdrawal_set_mpi_eci(id=id, value=data['mpi_eci'])

        if data['payment_id'] is not None:
            liqpay.withdrawal_set_payment_id(id=id, value=data['payment_id'])

        if data['receiver_commission'] is not None:
            liqpay.withdrawal_set_receiver_commission(id=id, value=data['receiver_commission'])

        if data['redirect_to'] is not None:
            liqpay.withdrawal_set_redirect_to(id=id, value=data['redirect_to'])

        if data['sender_bonus'] is not None:
            liqpay.withdrawal_set_sender_bonus(id=id, value=data['sender_bonus'])

        if data['sender_commission'] is not None:
            liqpay.withdrawal_set_sender_commission(id=id, value=data['sender_commission'])

        if data['status'] is not None:
            liqpay.withdrawal_set_status(id=id, value=data['status'])

        if data['transaction_id'] is not None:
            liqpay.withdrawal_set_transaction_id(id=id, value=data['transaction_id'])

        if data['type'] is not None:
            liqpay.withdrawal_set_type(id=id, value=data['type'])

    except:
        print('Cant load JSON data')
    close_connection(conn)