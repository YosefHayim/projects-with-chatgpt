import requests
from datetime import datetime

# Global dictionary to hold the last order details
last_order = {'price': None, 'quantity': None}

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat via bot.
    """
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(send_message_url, data=data)
    return response.ok

def update_last_order(price, quantity):
    """
    Updates the last order details.
    """
    last_order['price'] = price
    last_order['quantity'] = quantity

def format_order_message(order_details):
    """
    Formats a message with order details to be sent via Telegram.
    """
    symbol = order_details.get('symbol', 'N/A').replace('/USDT:USDT', '')  # Correct the symbol format
    order_id = order_details.get('id', 'N/A')
    status = order_details.get('status', 'N/A').capitalize()
    order_type = order_details.get('type', 'N/A').capitalize()
    entry_price = f"{order_details.get('average', 'N/A')}"
    signal = 'Buy' if order_details.get('side', '').lower() == 'buy' else 'Sell'
    orig_qty = f"{order_details.get('amount', 'N/A')}"
    executed_qty = f"{order_details.get('filled', 'N/A')}"
    cum_quote = f"{order_details.get('cost', 'N/A')}"
    timestamp = order_details.get('timestamp', 0)
    date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
    time = datetime.fromtimestamp(timestamp / 1000).strftime('%H:%M:%S')

    update_last_order(float(entry_price), float(executed_qty))

    message = (
        f"Date: {date}\n"
        f"Time: {time}\n"
        f"Symbol: {symbol}\n"
        f"Order ID: {order_id}\n"
        f"Status: {status}\n"
        f"Order type: {order_type}\n"
        f"Entry price: {entry_price}\n"
        f"Signal: {signal}\n"
        f"Original Quantity: {orig_qty}\n"
        f"Executed Quantity: {executed_qty}\n"
        f"Cumulative Quote Quantity: {cum_quote}\n"
        f"USDT Amount: {cum_quote}\n"
    )

    return message
