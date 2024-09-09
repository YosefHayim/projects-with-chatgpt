import logging
import numpy as np
import time
import talib
from IB_setup_RSI_LONG import InteractiveBrokersBot
from IB_telegrambot_RSI_LONG import send_telegram_message, format_order_message

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


TELEGRAM_BOT_TOKEN = 'BOT TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'

# Set error handling for NumPy operations
np.seterr(all='ignore')

# Trading configuration
MAX_ACTIVE_POSITIONS = 1
TRADE_AMOUNT_USDT = 100000


RSI_LOWER_BOUND = 43
RSI_UPPER_BOUND = 72
RSI_PERIOD = 4

def calculate_rsi(closes, period=14):
    return talib.RSI(closes, timeperiod=period)

def execute_strategy():
    bot = InteractiveBrokersBot(clientId=5, port=7497, trading_symbol='SPY')
    bot.connect()
    in_long_position = False

    while True:
        try:
            historical_data = bot.fetch_historical_data()
            if historical_data and len(historical_data) > 0:
                close_prices = np.array([bar['close'] for bar in historical_data], dtype=float)
                rsi_values = calculate_rsi(close_prices, RSI_PERIOD)
                logging.info(f"Current RSI: {rsi_values[-1]}")

                quantity = bot.calculate_quantity(TRADE_AMOUNT_USDT)

                # RSI Strategy Logic
                if rsi_values[-1] > RSI_LOWER_BOUND and not in_long_position and len(bot.check_active_positions()) < MAX_ACTIVE_POSITIONS:
                    order = bot.place_order('BUY', quantity)
                    log_order(order)
                    in_long_position = True

                elif rsi_values[-1] > RSI_UPPER_BOUND and in_long_position:
                    order = bot.place_order('SELL', quantity)
                    log_order(order)
                    in_long_position = False

        except Exception as e:
            logging.error(f"An exception occurred: {e}")
            time.sleep(2)

def log_order(order):
    if order:
        formatted_message = format_order_message(order)
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, formatted_message)
        logging.info(f"Order executed: {formatted_message}")

if __name__ == "__main__":
    execute_strategy()
