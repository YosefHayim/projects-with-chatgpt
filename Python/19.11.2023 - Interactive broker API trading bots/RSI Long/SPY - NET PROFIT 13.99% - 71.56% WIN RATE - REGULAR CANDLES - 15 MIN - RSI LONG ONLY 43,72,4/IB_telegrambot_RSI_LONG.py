import requests
from datetime import datetime

# Global dictionary to hold the last order details
last_order = {'price': None, 'quantity': None}

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat via bot.
    """
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
    response = requests.post(send_message_url, data=data)
    return response.ok

def update_last_order(price, quantity):
    """
    Updates the last order details.
    """
    last_order['price'] = price
    last_order['quantity'] = quantity

def calculate_profit_or_loss(entry_price, executed_qty):
    """
    Calculates profit or loss based on the last order details.
    """
    last_price = last_order['price']
    last_quantity = last_order['quantity']

    if last_price is not None and last_quantity is not None:
        try:
            executed_qty = float(executed_qty)
            position_size = min(executed_qty, last_quantity)
            profit_per_unit = float(entry_price) - last_price
            total_profit = profit_per_unit * position_size
            return total_profit
        except (ValueError, TypeError):
            return None

def format_order_message(trade):
    contract = trade.contract
    order = trade.order
    order_status = trade.orderStatus
    trade_log = trade.log

    date_time = trade_log[-1].time.strftime("%Y-%m-%d %H:%M:%S") if trade_log else 'N/A'
    symbol = contract.symbol if contract else 'N/A'
    exchange = contract.exchange if contract else 'N/A'
    action = order.action if order else 'N/A'
    order_type = order.orderType if order else 'N/A'
    total_quantity = order.totalQuantity if order else 'N/A'
    status = order_status.status if order_status else 'N/A'
    remaining_quantity = order_status.remaining if order_status else 'N/A'
    perm_id = order_status.permId if order_status else 'N/A'
    client_id = order_status.clientId if order_status else 'N/A'

    # Include limit price only for limit orders
    limit_price = 'N/A'
    if order_type == 'LMT' and hasattr(order, 'lmtPrice'):
        limit_price = order.lmtPrice

    message = (
        f"Date: {date_time}\n"
        f"Symbol: {symbol}\n"
        f"Exchange: {exchange}\n"
        f"Action: {action}\n"
        f"Order Type: {order_type}\n"
        f"Quantity: {total_quantity}\n"
        f"Limit Price: {limit_price}\n"
        f"Status: {status}\n"
        f"Remaining Quantity: {remaining_quantity}\n"
        f"Permanent ID: {perm_id}\n"
        f"Client ID: {client_id}\n"
    )

    return message

