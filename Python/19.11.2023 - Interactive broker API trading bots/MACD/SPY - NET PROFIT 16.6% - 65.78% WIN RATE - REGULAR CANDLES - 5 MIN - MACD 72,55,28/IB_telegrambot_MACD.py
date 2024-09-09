import requests
from datetime import datetime

# Global dictionary to hold the last order details
# This dictionary is used to store the price and quantity of the last executed order.
last_order = {'price': None, 'quantity': None}

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to a Telegram chat via bot.
    
    Args:
    - bot_token (str): The Telegram bot token used for authentication.
    - chat_id (str): The chat ID where the message will be sent.
    - message (str): The message content to be sent.
    
    Returns:
    - bool: True if the message was sent successfully, False otherwise.
    """
    # URL for sending a message via Telegram API
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Data payload to be sent with the POST request
    data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
    
    # Sending a POST request to the Telegram API to send the message
    response = requests.post(send_message_url, data=data)
    
    # Return True if the request was successful, otherwise False
    return response.ok

def update_last_order(price, quantity):
    """
    Updates the last order details in the global last_order dictionary.
    
    Args:
    - price (float): The price at which the last order was executed.
    - quantity (float): The quantity of the last order executed.
    """
    # Update the global last_order dictionary with the new price and quantity
    last_order['price'] = price
    last_order['quantity'] = quantity

def calculate_profit_or_loss(entry_price, executed_qty):
    """
    Calculates the profit or loss based on the last order details.
    
    Args:
    - entry_price (float): The price at which the current position was entered.
    - executed_qty (float): The quantity of the current position.
    
    Returns:
    - float: The total profit or loss based on the last order details.
    - None: If there is an error in the calculation.
    """
    # Retrieve the price and quantity from the last order
    last_price = last_order['price']
    last_quantity = last_order['quantity']

    # Ensure that the last order details are not None
    if last_price is not None and last_quantity is not None:
        try:
            # Convert executed_qty to a float for calculation
            executed_qty = float(executed_qty)
            
            # Determine the position size based on the smaller of the executed quantity or last quantity
            position_size = min(executed_qty, last_quantity)
            
            # Calculate the profit or loss per unit
            profit_per_unit = float(entry_price) - last_price
            
            # Calculate the total profit or loss
            total_profit = profit_per_unit * position_size
            
            return total_profit
        except (ValueError, TypeError):
            # Return None if there is an error in conversion or calculation
            return None

def format_order_message(trade):
    """
    Formats an order message with details to be sent via Telegram.
    
    Args:
    - trade (object): The trade object containing all order details.
    
    Returns:
    - str: A formatted string containing the order details.
    """
    # Extract information from the trade object
    contract = trade.contract
    order = trade.order
    order_status = trade.orderStatus
    trade_log = trade.log

    # Format the date and time of the order execution
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

    # Create a formatted message string containing all relevant details
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

    # Return the formatted message
    return message
