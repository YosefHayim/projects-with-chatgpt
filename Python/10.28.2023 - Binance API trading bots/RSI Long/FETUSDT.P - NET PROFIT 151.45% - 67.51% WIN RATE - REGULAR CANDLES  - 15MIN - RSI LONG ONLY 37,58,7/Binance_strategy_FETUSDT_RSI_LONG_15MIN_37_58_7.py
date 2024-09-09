from Binance_telegram_RSI_LONG import send_telegram_message, format_order_message
import logging
import talib
import numpy as np
import time
from Binance_setup_RSI_LONG import BinanceBot
from Binance_config_FETUSDT_RSI_LONG import api_key, api_secret

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TELEGRAM_BOT_TOKEN = 'BOT TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'

np.seterr(all='ignore')

TRADE_AMOUNT_USDT = 2
MAX_ACTIVE_POSITIONS = 1


RSI_LOWER_BOUND = 37
RSI_UPPER_BOUND = 58
RSI_PERIOD = 7


def calculate_rsi(closes, period=RSI_PERIOD):
    return talib.RSI(closes, timeperiod=period)

def execute_strategy():
    bot = BinanceBot(api_key, api_secret)
    in_long_position = False

    while True:
        try:
            real_time_data = bot.fetch_real_time_data()

            if real_time_data and len(real_time_data) > 0:
                close_prices = np.array([candle['close'] for candle in real_time_data], dtype=float)
                rsi_values = calculate_rsi(close_prices, RSI_PERIOD)

                quantity = bot.calculate_quantity(TRADE_AMOUNT_USDT)

                current_rsi = rsi_values[-1]
                logging.info(f"Current RSI: {current_rsi:.5f}")

                total_active, _ = bot.get_active_order_count()

                # Enter Long Position
                if current_rsi < RSI_LOWER_BOUND and not in_long_position and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_market_order('BUY', quantity)
                    log_order(order)
                    logging.info("Entering Long position")
                    in_long_position = True

                # Exit Long Position
                elif current_rsi > RSI_UPPER_BOUND and in_long_position:
                    order = bot.clean_open_orders()
                    log_order(order)
                    logging.info("Exiting Long position")
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