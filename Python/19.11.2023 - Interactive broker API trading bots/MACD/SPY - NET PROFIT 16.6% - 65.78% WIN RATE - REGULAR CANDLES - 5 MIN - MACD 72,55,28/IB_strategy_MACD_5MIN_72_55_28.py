import logging
import numpy as np
import time
import talib
from IB_setup_MACD import InteractiveBrokersBot  # Import the IB bot setup module
from IB_telegrambot_MACD import send_telegram_message, format_order_message  # Import the Telegram bot functions

# Configure logging to display debug-level messages, including timestamps, log level, and message content
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname=s - %(message)s')

# Telegram Bot Configuration

TELEGRAM_BOT_TOKEN = 'BOT TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'

# Set error handling for NumPy operations to ignore all warnings (such as divide by zero)
np.seterr(all='ignore')

# Trading configuration
MAX_ACTIVE_POSITIONS = 1  # Maximum number of active positions allowed at any time
TRADE_AMOUNT_USDT = 40000  # The amount in USD to trade with each transaction

def execute_strategy():
    """
    Main function to execute the MACD trading strategy.
    This function connects to Interactive Brokers, fetches historical data, 
    calculates the MACD indicator, and makes trading decisions based on the MACD signals.
    """
    # Instantiate the bot with your client ID, port number, and trading symbol
    bot = InteractiveBrokersBot(clientId=5, port=7497, trading_symbol='SPY')
    
    # Connect to Interactive Brokers
    bot.connect()
    
    # Initialize flags to track if the bot is in a long or short position
    in_long_position = False
    in_short_position = False

    # MACD Configuration
    fast_length = 72  # The fast period for the MACD calculation
    slow_length = 55  # The slow period for the MACD calculation
    signal_length = 28  # The signal line period for the MACD calculation

    while True:  # Infinite loop to continuously monitor the market and execute trades
        try:
            # Fetch historical data (e.g., past prices) from Interactive Brokers
            historical_data = bot.fetch_historical_data()
            
            # If data is available, proceed with strategy execution
            if historical_data and len(historical_data) > 0:
                # Extract closing prices from the historical data
                close_prices = np.array([bar['close'] for bar in historical_data], dtype=float)

                # Calculate the MACD and signal lines using TA-Lib
                macd, signal, _ = talib.MACD(close_prices, fastperiod=fast_length, slowperiod=slow_length, signalperiod=signal_length)
                logging.info(f"MACD: {macd[-1]}")
                logging.info(f"Signal: {signal[-1]}")

                # Calculate the quantity of stock to trade based on the available trade amount in USD
                quantity = bot.calculate_quantity(TRADE_AMOUNT_USDT)

                # Check the current active positions and orders
                positions_summary = bot.check_active_positions_and_orders()
                all_positions = positions_summary['positions'] if positions_summary else []
                total_active = len(all_positions)  # Total number of active positions

                # Update the flags based on the actual positions
                in_long_position = any(pos.contract.symbol == 'SPY' and pos.position > 0 for pos in all_positions)
                in_short_position = any(pos.contract.symbol == 'SPY' and pos.position < 0 for pos in all_positions)

                # MACD Strategy Logic: Enter or exit positions based on MACD signals
                if macd[-1] > signal[-1] and not in_long_position and total_active < MAX_ACTIVE_POSITIONS:
                    # If MACD crosses above the signal line, and there are no long positions, buy
                    order = bot.place_order('BUY', quantity)
                    log_order(order)
                    in_long_position = True
                    in_short_position = False

                elif macd[-1] < signal[-1] and in_long_position:
                    # If MACD crosses below the signal line, and currently in a long position, sell
                    order = bot.place_order('SELL', quantity)
                    log_order(order)
                    in_long_position = False

                if macd[-1] < signal[-1] and not in_short_position and total_active < MAX_ACTIVE_POSITIONS:
                    # If MACD crosses below the signal line, and there are no short positions, sell
                    order = bot.place_order('SELL', quantity)
                    log_order(order)
                    in_short_position = True
                    in_long_position = False

                elif macd[-1] > signal[-1] and in_short_position:
                    # If MACD crosses above the signal line, and currently in a short position, buy
                    order = bot.place_order('BUY', quantity)
                    log_order(order)
                    in_short_position = False

        except Exception as e:
            # Log any exceptions that occur during strategy execution
            logging.error(f"An exception occurred: {e}")
            time.sleep(2)  # Pause briefly before retrying

def log_order(order):
    """
    Function to log and send details of the executed order via Telegram.
    """
    if order:
        # Format the order message for readability
        formatted_message = format_order_message(order)
        # Send the formatted order message to Telegram
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, formatted_message)
        logging.info(f"Order executed: {formatted_message}")

if __name__ == "__main__":
    # Start executing the trading strategy when the script is run
    execute_strategy()
