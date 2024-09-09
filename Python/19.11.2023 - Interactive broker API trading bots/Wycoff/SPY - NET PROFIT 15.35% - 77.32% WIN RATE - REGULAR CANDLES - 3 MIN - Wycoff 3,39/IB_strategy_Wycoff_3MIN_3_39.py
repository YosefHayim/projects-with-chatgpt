import logging
import numpy as np
import time
from IB_setup_WYCOFF import InteractiveBrokersBot
from IB_telegrambot_WYCOFF import send_telegram_message, format_order_message


TELEGRAM_BOT_TOKEN = 'BOT TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set error handling for NumPy operations
np.seterr(all='ignore')

# Trading configuration
MAX_ACTIVE_POSITIONS = 1
TRADE_AMOUNT_USDT = 42000

# Wyckoff Configuration
ACCUMULATION_LENGTH = 3
DISTRIBUTION_LENGTH = 39

def is_accumulation(bars):
    if len(bars) < ACCUMULATION_LENGTH:
        return False
    lows = [bar['low'] for bar in bars]
    volumes = [bar['volume'] for bar in bars]
    return lows[-1] == min(lows[-ACCUMULATION_LENGTH:]) and volumes[-1] < np.mean(volumes[-ACCUMULATION_LENGTH:])

def is_distribution(bars):
    if len(bars) < DISTRIBUTION_LENGTH:
        return False
    highs = [bar['high'] for bar in bars]
    volumes = [bar['volume'] for bar in bars]
    return highs[-1] == max(highs[-DISTRIBUTION_LENGTH:]) and volumes[-1] < np.mean(volumes[-DISTRIBUTION_LENGTH:])

def execute_strategy():
    bot = InteractiveBrokersBot(clientId=5, port=7497, trading_symbol='SPY')
    bot.connect()
    last_action = 'sell'  # Assuming the last action was a sell

    while True:
        try:
            historical_data = bot.fetch_historical_data()
            if historical_data and len(historical_data) >= max(ACCUMULATION_LENGTH, DISTRIBUTION_LENGTH):

                quantity = bot.calculate_quantity(TRADE_AMOUNT_USDT)

                # Check active positions and orders
                positions_summary = bot.check_active_positions_and_orders()
                all_positions = positions_summary['positions'] if positions_summary else []
                total_active = len(all_positions)

                in_long_position = any(pos.contract.symbol == 'SPY' and pos.position > 0 for pos in all_positions)
                in_short_position = any(pos.contract.symbol == 'SPY' and pos.position < 0 for pos in all_positions)

                # Wyckoff Strategy Logic
                if is_accumulation(historical_data) and last_action != 'buy' and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_order('BUY', quantity)
                    log_order(order)
                    last_action = 'buy'
                    in_long_position = True
                    in_short_position = False


                elif is_distribution(historical_data) and last_action != 'sell':
                    order = bot.place_order('SELL', quantity)
                    log_order(order)
                    last_action = 'sell'
                    in_long_position = False
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
