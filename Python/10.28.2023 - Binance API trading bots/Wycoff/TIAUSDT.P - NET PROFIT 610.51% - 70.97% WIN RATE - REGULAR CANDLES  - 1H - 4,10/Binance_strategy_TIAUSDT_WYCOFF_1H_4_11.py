from Binance_telegram_WYCOFF_ import send_telegram_message, format_order_message
import logging
import numpy as np
import time
from Binance_setup_WYCOFF_TIAUSDT import BinanceBot
from Binance_config_TIAUSDT import api_key, api_secret


TELEGRAM_BOT_TOKEN = 'BOT TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

np.seterr(all='ignore')

TRADE_AMOUNT_USDT = 5

MAX_ACTIVE_POSITIONS = 1

ACCUMULATION_LENGTH = 4

DISTRIBUTION_LENGTH = 11

def is_accumulation(candles):
    if len(candles) < ACCUMULATION_LENGTH:
        return False
    lows = [candle['low'] for candle in candles]
    volumes = [candle['volume'] for candle in candles]
    return lows[-1] == min(lows[-ACCUMULATION_LENGTH:]) and volumes[-1] < np.mean(volumes[-ACCUMULATION_LENGTH:])

def is_distribution(candles):
    if len(candles) < DISTRIBUTION_LENGTH:
        return False
    highs = [candle['high'] for candle in candles]
    volumes = [candle['volume'] for candle in candles]
    return highs[-1] == max(highs[-DISTRIBUTION_LENGTH:]) and volumes[-1] < np.mean(volumes[-DISTRIBUTION_LENGTH:])

def execute_strategy():
    bot = BinanceBot(api_key, api_secret)
    last_action = 'sell'  # Assuming the last action was a sell

    while True:
        try:
            real_time_data = bot.fetch_real_time_data()

            if real_time_data and len(real_time_data) >= max(ACCUMULATION_LENGTH, DISTRIBUTION_LENGTH):
                total_active, _ = bot.get_active_order_count()

                # Enter Long Position
                if is_accumulation(real_time_data) and last_action != 'buy' and total_active < MAX_ACTIVE_POSITIONS:
                    quantity = bot.calculate_quantity(TRADE_AMOUNT_USDT)
                    order = bot.place_market_order('BUY', quantity)
                    log_order(order)
                    logging.info("Entering Long position")
                    last_action = 'buy'

                # Exit Long Position
                elif is_distribution(real_time_data) and last_action != 'sell':
                    order = bot.clean_open_orders()
                    log_order(order)
                    logging.info("Exiting Long position")
                    last_action = 'sell'


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
