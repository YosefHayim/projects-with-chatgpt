import logging
import numpy as np
import time
import talib
from IB_setup_SMA_ import InteractiveBrokersBot
from IB_telegrambot_SMA_2 import send_telegram_message, format_order_message

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


TELEGRAM_BOT_TOKEN = 'BOT TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'

# Set error handling for NumPy operations
np.seterr(all='ignore')

# Trading configuration
MAX_ACTIVE_POSITIONS = 1
TRADE_AMOUNT_USDT = 40000

SMA_PERIOD = 2

def execute_strategy():
    bot = InteractiveBrokersBot(clientId=5, port=7497, trading_symbol='SPY')
    bot.connect()

    while True:
        try:
            historical_data = bot.fetch_historical_data()
            if historical_data and len(historical_data) > 0:
                close_prices = np.array([bar['close'] for bar in historical_data], dtype=float)

                # Calculate SMA
                sma_value = talib.SMA(close_prices, SMA_PERIOD)

                quantity = bot.calculate_quantity(TRADE_AMOUNT_USDT)

                # Check active positions and orders
                positions_summary = bot.check_active_positions_and_orders()
                all_positions = positions_summary['positions'] if positions_summary else []
                total_active = len(all_positions)

                # Strategy Logic based only on SMA
                is_above_sma = close_prices[-1] > sma_value[-1]
                is_below_sma = close_prices[-1] < sma_value[-1]

                if is_above_sma and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_order('BUY', quantity)
                    log_order(order)

                elif is_below_sma and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_order('SELL', quantity)
                    log_order(order)


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
