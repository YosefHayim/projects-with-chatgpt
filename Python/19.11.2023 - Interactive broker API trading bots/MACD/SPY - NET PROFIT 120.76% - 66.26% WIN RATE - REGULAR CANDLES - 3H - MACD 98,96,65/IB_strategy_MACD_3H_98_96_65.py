import logging
import numpy as np
import time
import talib
from IB_setup_MACD import InteractiveBrokersBot
from IB_telegrambot_MACD import send_telegram_message, format_order_message

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Telegram Bot Configuration

TELEGRAM_BOT_TOKEN = 'BOT TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'

# Set error handling for NumPy operations
np.seterr(all='ignore')

# Trading configuration
MAX_ACTIVE_POSITIONS = 1
TRADE_AMOUNT_USDT = 100000

def execute_strategy():
    bot = InteractiveBrokersBot(clientId=5, port=7497, trading_symbol='SPY')
    bot.connect()
    in_long_position = False
    in_short_position = False

    # MACD Configuration
    fast_length = 98
    slow_length = 96
    signal_length = 65

    while True:
        try:
            historical_data = bot.fetch_historical_data()
            if historical_data and len(historical_data) > 0:
                close_prices = np.array([bar['close'] for bar in historical_data], dtype=float)

                # Calculate MACD
                macd, signal, _ = talib.MACD(close_prices, fastperiod=fast_length, slowperiod=slow_length, signalperiod=signal_length)
                logging.info(f"MACD: {macd[-1]}")
                logging.info(f"Signal: {signal[-1]}")

                quantity = bot.calculate_quantity(TRADE_AMOUNT_USDT)

                # Check active positions and orders
                positions_summary = bot.check_active_positions_and_orders()
                all_positions = positions_summary['positions'] if positions_summary else []
                total_active = len(all_positions)

                # Update position flags based on actual positions
                in_long_position = any(pos.contract.symbol == 'SPY' and pos.position > 0 for pos in all_positions)
                in_short_position = any(pos.contract.symbol == 'SPY' and pos.position < 0 for pos in all_positions)

                # MACD Strategy Logic
                if macd[-1] > signal[-1] and not in_long_position and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_order('BUY', quantity)
                    log_order(order)
                    in_long_position = True
                    in_short_position = False

                elif macd[-1] < signal[-1] and in_long_position:
                    order = bot.place_order('SELL', quantity)
                    log_order(order)
                    in_long_position = False

                if macd[-1] < signal[-1] and not in_short_position and total_active < MAX_ACTIVE_POSITIONS:
                    order = bot.place_order('SELL', quantity)
                    log_order(order)
                    in_short_position = True
                    in_long_position = False

                elif macd[-1] > signal[-1] and in_short_position:
                    order = bot.place_order('BUY', quantity)
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
