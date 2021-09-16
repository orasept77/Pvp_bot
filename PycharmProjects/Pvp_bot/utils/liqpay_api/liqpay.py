from data.config import LIQPAY_PUBLICKEY, LIQPAY_PRIVATEKEY, LIQPAY_CURRENCY, LIQPAY_WITHDRAWAL_MESSAGE, \
    LIQPAY_WITHDRAWAL_URL, LIQPAY_DEPOSIT_URL, LIQPAY_DEPOSIT_MESSAGE

from utils.db_api.create_asyncpg_connection import create_conn
from utils.db_api.deposit.deposit_repo import DepositRepo
from utils.db_api.liqpay.liqpay_repo import LiqPayRepo

from utils.liqpay_api.liqpay_sdk.liqpay import LiqPay

liqpay = LiqPay(LIQPAY_PUBLICKEY, LIQPAY_PRIVATEKEY)


# DEPOSITS
async def liqpay_create_deposit_payment(user_id, amount, phone):
    conn = await create_conn()
    repo = LiqPayRepo(conn=conn)
    order_id = await repo.create_deposit_order(user_id, amount, phone)

    res = liqpay.api("request", {
        "action": "invoice_bot",
        "version": "3",
        "amount": str(amount),
        "currency": str(LIQPAY_CURRENCY),
        "order_id": str(order_id),
        "phone": str(phone),
        "description": str(LIQPAY_DEPOSIT_MESSAGE),
        "server_url": str(LIQPAY_DEPOSIT_URL)
    })

    await conn.close()
    return res


async def liqpay_update_deposit_status(response, order_id):
    conn = await create_conn()
    repo = LiqPayRepo(conn=conn)
    deposit = DepositRepo(conn=conn)

    if response == 'ok':
        await repo.deposit_order_success(order_id)
        user_id = await repo.deposit_get_order_user_id(order_id)
        amount = await repo.deposit_get_order_amount(order_id)
        await deposit.liqpay_deposit(user_id['user_id'], amount['amount'])
    elif response == 'error':
        await repo.deposit_order_not_enough_money(order_id)
    else:
        await repo.deposit_order_set_state(order_id, 'UNEXPECTED_ERROR')

    await conn.close()
    return


# WITHDRAWALS
async def liqpay_create_withdrawal_payment(user_id, amount, user_card_number, first_name, last_name):
    conn = await create_conn()
    repo = LiqPayRepo(conn=conn)
    deposit = DepositRepo(conn=conn)

    order_id = await repo.create_withdrawal_order(user_id, amount)
    res = liqpay.api("request", {
        "action": "p2pcredit",
        "version": "3",
        "amount": str(amount),
        "currency": str(LIQPAY_CURRENCY),
        "order_id": str(order_id),
        "receiver_card": str(user_card_number).replace(" ", ""),
        "receiver_last_name": str(last_name).replace(" ", ""),
        "receiver_first_name": str(first_name).replace(" ", ""),
        "description": str(LIQPAY_WITHDRAWAL_MESSAGE),
        "server_url": str(LIQPAY_WITHDRAWAL_URL)
    })
    await deposit.minus_user_deposit(user_id, amount)
    await conn.close()
    return res



async def liqpay_update_withdrawal_status(response, order_id):
    conn = await create_conn()
    repo = LiqPayRepo(conn=conn)
    deposit = DepositRepo(conn=conn)

    user_id = await repo.withdrawal_get_order_user_id(order_id)
    amount = await repo.withdrawal_get_order_amount(order_id)
    if response == 'success':
        await repo.withdrawal_order_success(order_id)
    elif response == 'failure':
        await repo.withdrawal_order_failure(order_id, 'ERROR')
        await deposit.update_user_deposit(user_id['user_id'], amount['amount'])
    elif response == 'error':
        await repo.withdrawal_order_error(order_id)
        await deposit.update_user_deposit(user_id['user_id'], amount['amount'])
    else:
        await repo.withdrawal_order_set_state(order_id, 'UNEXPECTED_ERROR')

    await conn.close()
    return
