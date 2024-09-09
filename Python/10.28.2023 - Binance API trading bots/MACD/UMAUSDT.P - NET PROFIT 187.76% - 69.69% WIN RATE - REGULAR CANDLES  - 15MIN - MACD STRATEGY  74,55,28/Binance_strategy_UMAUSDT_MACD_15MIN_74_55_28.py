from Binance_telegram_MACD import send_telegram_message, format_order_message
import logging
import talib
import numpy as np
import time
from Binance_setup_UMAUSDT_MACD import BinanceBot
from Binance_config_UMAUSDT_MACD import api_key, api_secret

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Telegram Config
TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'TELEGRAM_CHAT_ID'

np.seterr(all='ignore')

# MACD Strategy Parameters
TRADE_AMOUNT_USDT = 2
MAX_ACTIVE_POSITIONS = 1


# MACD Parameters
MACD_FAST = 74
MACD_SLOW = 55
MACD_SIGNAL = 28

def calculate_macd(closes):
    macd, signal, _ = talib.MACD(closes, fastperiod=MACD_FAST, slowperiod=MACD_SLOW, signalperiod=MACD_SIGNAL)
    return macd, signal

def execute_strategy():
    bot = BinanceBot(api_key, api_secret)
    in_long_position = False
    in_short_position = False

    while True:
        try:
            real_time_data = bot.fetch_real_time_data()

            if real_time_data and len(real_time_data) > 0:
                close_prices = np.array([candle['close'] for candle in real_time_data], dtype=float)
                macd, signal = calculate_macd(close_prices)

                quantity = bot.calculate_quantity(TRADE_AMOUNT_USDT)

                macd_gap = macd[-1] - signal[-1]

                logging.info(f"Current MACD: {macd[-1]:.5f}, Signal: {signal[-1]:.5f}, Gap: {macd_gap:.5f}")

                total_active, _ = bot.get_active_order_count()

                # Define Long and Short Conditions
                long_condition = macd[-1] > signal[-1] and macd[-2] <= signal[-2]
                short_condition = macd[-1] < signal[-1] and macd[-2] >= signal[-2]

                # MACD Strategy Logic for Binance
                if macd[-1] > signal[-1] and not in_long_position and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_market_order('BUY', quantity)
                    log_order(order)
                    in_long_position = True
                    in_short_position = False

                elif macd[-1] < signal[-1] and in_long_position:
                    order = bot.clean_open_orders()
                    log_order(order)
                    in_long_position = False

                if macd[-1] < signal[-1] and not in_short_position and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_market_order('SELL', quantity)
                    log_order(order)
                    in_short_position = True
                    in_long_position = False

                elif macd[-1] > signal[-1] and in_short_position:
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
