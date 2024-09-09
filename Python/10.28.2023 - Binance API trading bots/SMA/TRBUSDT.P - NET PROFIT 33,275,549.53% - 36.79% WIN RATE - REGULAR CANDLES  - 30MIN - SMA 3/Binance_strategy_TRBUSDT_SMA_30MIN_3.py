from Binance_telegram_SMA_ import send_telegram_message, format_order_message
import logging
import talib
import numpy as np
import time
from Binance_setup_SMA_TRBUSDT import BinanceBot
from Binance_config_TRBUSDT_SMA import api_key, api_secret

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Telegram Config

TELEGRAM_BOT_TOKEN = 'BOT TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'

np.seterr(all='ignore')

# SMA Strategy Parameters
TRADE_AMOUNT_USDT = 5

MAX_ACTIVE_POSITIONS = 1

SMA_PERIOD = 3  # Simple Moving Average period

def calculate_sma(closes):
    return talib.SMA(closes, timeperiod=SMA_PERIOD)

def execute_strategy():
    bot = BinanceBot(api_key, api_secret)
    in_long_position = False
    in_short_position = False

    while True:
        try:
            real_time_data = bot.fetch_real_time_data()

            if real_time_data and len(real_time_data) > 0:
                close_prices = np.array([candle['close'] for candle in real_time_data], dtype=float)
                sma = calculate_sma(close_prices)

                quantity = bot.calculate_quantity(TRADE_AMOUNT_USDT)

                logging.info(f"Current SMA: {sma[-1]:.5f}")

                total_active, _ = bot.get_active_order_count()

                # Define Long and Short Conditions
                long_condition = close_prices[-1] > sma[-1]
                short_condition = close_prices[-1] < sma[-1]

                # SMA Strategy Logic for Binance
                if long_condition and not in_long_position and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_market_order('BUY', quantity)
                    log_order(order)
                    in_long_position = True
                    in_short_position = False

                elif short_condition and in_long_position:
                    order = bot.clean_open_orders()
                    log_order(order)
                    in_long_position = False

                if short_condition and not in_short_position and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_market_order('SELL', quantity)
                    log_order(order)
                    in_short_position = True
                    in_long_position = False

                elif long_condition and in_short_position:
                    order = bot.clean_open_orders()
                    log_order(order)
                    in_short_position = False

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
