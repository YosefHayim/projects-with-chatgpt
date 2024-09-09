import logging
from ib_insync import IB, Stock, Order, util
import numpy as np

# Configure logging to output information with a timestamp, severity level, and message.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InteractiveBrokersBot:
    def __init__(self, clientId, port, trading_symbol):
        # Initialize the bot with client ID, port number, and trading symbol.
        self.clientId = 1  # Default client ID; you should replace it with your actual client ID.
        self.clientId = clientId  # Assign the provided client ID.
        self.port = 1111  # Default port number; you should replace it with your actual port number.
        self.ib = IB()  # Create an IB (Interactive Brokers) instance to interact with the API.
        self.trading_symbol = trading_symbol  # Define the trading symbol (e.g., 'AAPL').

    def connect(self):
        """Connect to Interactive Brokers TWS or Gateway."""
        try:
            # Attempt to establish a connection to the Interactive Brokers API using the given IP, port, and client ID.
            self.ib.connect('127.0.0.1', self.port, clientId=self.clientId)
            logging.info("Connected to Interactive Brokers.")
        except Exception as e:
            # Log an error if the connection fails.
            logging.error(f'Connection error: {e}')

    def get_account_info(self):
        """Retrieve account information."""
        try:
            # Fetch account information from Interactive Brokers.
            account_info = self.ib.accountValues()
            logging.info('Account information retrieved successfully.')
            return account_info
        except Exception as e:
            # Log an error if retrieving account info fails.
            logging.error(f'Error getting account info: {e}')
            return None

    def get_balance(self):
        """Retrieve USD balance."""
        try:
            # Extract the USD balance from the account information.
            usd_balance = next(
                val for val in self.ib.accountValues() if val.tag == 'CashBalance' and val.currency == 'USD')
            logging.info(f"USD balance: {usd_balance.value}")
            return usd_balance.value
        except Exception as e:
            # Log an error if retrieving the USD balance fails.
            logging.error(f'Error getting USD balance: {e}')
            return None

    def get_stock_info(self):
        """Retrieve stock information."""
        try:
            # Create a contract object for the specified trading symbol.
            contract = Stock(self.trading_symbol, 'SMART', 'USD')
            # Request market data for the contract.
            self.ib.reqMktData(contract, '', False, False)
            data = self.ib.reqMktData(contract)
            logging.info(f'Stock information retrieved successfully for {self.trading_symbol}.')
            return data
        except Exception as e:
            # Log an error if retrieving stock info fails.
            logging.error(f'Error getting stock info: {e}')
            return None

    def place_order(self, order_type, quantity):
        """Place a market order."""
        # Define the stock contract.
        self.contract = Stock(self.trading_symbol, 'SMART', 'USD')

        # Create a market order with the specified action (buy or sell) and quantity.
        market_order = Order()
        market_order.action = order_type  # Order action: 'BUY' or 'SELL'.
        market_order.totalQuantity = quantity  # Number of shares to buy or sell.
        market_order.orderType = 'MKT'  # Market order type.

        # Place the market order.
        trade = self.ib.placeOrder(self.contract, market_order)

        # Log the order details if the trade object contains an order ID.
        if hasattr(trade, 'order') and hasattr(trade.order, 'orderId'):
            order_id = trade.order.orderId
            logging.info(f'Market order placed: {trade}. Order ID: {order_id}')
        else:
            logging.error('Failed to place market order: Order details not found in trade object.')

        return trade

    def place_order_limit_tp_stp_trailing_stop(self, order_type, quantity):
        """Place a limit order with take profit, stop loss, and trailing stop orders."""
        # Define the stock contract.
        self.contract = Stock(self.trading_symbol, 'SMART', 'USD')

        # Fetch the last market price to use as a reference.
        market_data = self.ib.reqMktData(self.contract, '', False, False)
        reference_price = market_data.last if market_data.last else market_data.close

        # Adjust the reference price slightly for the limit order.
        limit_price = reference_price + 0.00001 if order_type == 'BUY' else reference_price - 0.00001

        # Create the limit order.
        limit_order = Order()
        limit_order.action = order_type  # Order action: 'BUY' or 'SELL'.
        limit_order.totalQuantity = quantity  # Number of shares to buy or sell.
        limit_order.lmtPrice = limit_price  # Limit price.
        limit_order.outsideRth = True  # Allow order execution outside regular trading hours.

        # Place the limit order.
        trade = self.ib.placeOrder(self.contract, limit_order)

        # Place auxiliary orders (take profit, stop loss, trailing stop) using the reference price.
        self.place_auxiliary_orders(reference_price, quantity, order_type)

        # Log the order details if the trade object contains an order ID.
        if hasattr(trade, 'order') and hasattr(trade.order, 'orderId'):
            order_id = trade.order.orderId
            logging.info(f'Order placed for session: {trade}. Order ID: {order_id}, Limit Price: {limit_price}')
        else:
            logging.error(f'Failed to place order for session: Order details not found in trade object.')

        return trade

    def place_auxiliary_orders(self, fill_price, quantity, order_type):
        """Place take profit, stop loss, and trailing stop orders."""
        # Define the tick size (e.g., 0.01 for stocks) for price calculations.
        tick_size = 0.01

        # Calculate take profit and stop loss prices, rounded to the nearest tick size.
        take_profit_price = round(
            (fill_price * 1.02 if order_type == 'BUY' else fill_price * 0.98) / tick_size) * tick_size
        stop_loss_price = round(
            (fill_price * 0.98 if order_type == 'BUY' else fill_price * 1.02) / tick_size) * tick_size

        # Create and place the take profit order.
        tp_order = Order()
        tp_order.action = 'SELL' if order_type == 'BUY' else 'BUY'
        tp_order.totalQuantity = quantity
        tp_order.orderType = 'LMT'  # Limit order type.
        tp_order.lmtPrice = take_profit_price
        self.ib.placeOrder(self.contract, tp_order)

        # Create and place the stop loss order.
        sl_order = Order()
        sl_order.action = 'SELL' if order_type == 'BUY' else 'BUY'
        sl_order.totalQuantity = quantity
        sl_order.orderType = 'STP'  # Stop order type.
        sl_order.auxPrice = stop_loss_price
        self.ib.placeOrder(self.contract, sl_order)

        # Create and place the trailing stop order.
        trailing_stop_order = Order()
        trailing_stop_order.action = 'SELL' if order_type == 'BUY' else 'BUY'
        trailing_stop_order.totalQuantity = quantity
        trailing_stop_order.orderType = 'TRAIL'  # Trailing stop order type.
        trailing_stop_order.trailingPercent = 0.1  # 0.1% trailing stop.
        trailing_stop_order.trailStopPrice = fill_price
        self.ib.placeOrder(self.contract, trailing_stop_order)

    def check_active_positions_and_orders(self):
        """Retrieve all positions without filtering for active positions."""
        try:
            # Force a refresh of position data.
            self.ib.reqPositions()

            # Fetch all positions.
            positions = self.ib.positions()

            # Validate that the fetched data is a list.
            if not isinstance(positions, list):
                logging.error("Expected a list for positions")
                return None

            # Create a summary of all positions.
            positions_summary = {'positions': positions}

            # Log the positions summary for debugging purposes.
            logging.debug(f"Positions summary: {positions_summary}")
            return positions_summary

        except Exception as e:
            # Log any errors encountered while checking positions.
            logging.error(f"An error occurred: {e}")
            return None

    def fetch_historical_data(self, use_heikin_ashi=False):
        """Fetch historical data and optionally convert it to Heikin Ashi format."""
        try:
            # Define the stock contract.
            contract = Stock(self.trading_symbol, 'SMART', 'USD')

            # Request historical data (e.g., for the last 3 days, 5-minute bars).
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr='3 D',  # Last 3 days of data.
                barSizeSetting='5 mins',  # 5-minute bars.
                whatToShow='TRADES',  # Show trade data.
                useRTH=False,  # Include data outside regular trading hours.
                formatDate=1,
                keepUpToDate=True
            )
            logging.info(f'Historical data for {self.trading_symbol} retrieved. Total bars: {len(bars)}')

            # Format the data into a list of dictionaries.
            formatted_data = [
                {'date': util.formatIBDatetime(bar.date), 'open': bar.open, 'high': bar.high, 'low': bar.low,
                 'close': bar.close, 'volume': bar.volume} for bar in bars]

            # Optionally calculate and integrate Heikin Ashi candles.
            if use_heikin_ashi:
                heikin_ashi_data = self.calculate_heikin_ashi(formatted_data)
                for data in heikin_ashi_data:
                    logging.info(f"Heikin Ashi Bar Data: {data}")

                return heikin_ashi_data

            return formatted_data

        except Exception as e:
            # Log any errors encountered while fetching historical data.
            logging.error(f'An error occurred while fetching historical data: {e}')
            return None

    def calculate_heikin_ashi(self, ohlcv_data):
        """Calculate Heikin Ashi candles from OHLCV data."""
        heikin_ashi_data = []
        for i, row in enumerate(ohlcv_data):
            if i == 0:  # For the first candle, HA values are the same as the regular values.
                ha_open = row['open']
                ha_close = row['close']
                ha_high = row['high']
                ha_low = row['low']
            else:
                # Heikin Ashi Open is the average of the previous HA Open and HA Close.
                ha_open = (heikin_ashi_data[i - 1]['open'] + heikin_ashi_data[i - 1]['close']) / 2
                # Heikin Ashi Close is the average of the current Open, High, Low, Close.
                ha_close = (row['open'] + row['high'] + row['low'] + row['close']) / 4
                # Heikin Ashi High is the maximum of the current High, HA Open, HA Close.
                ha_high = max(row['high'], ha_open, ha_close)
                # Heikin Ashi Low is the minimum of the current Low, HA Open, HA Close.
                ha_low = min(row['low'], ha_open, ha_close)

            # Append the calculated Heikin Ashi values to the list.
            heikin_ashi_data.append({
                'date': row['date'],
                'open': ha_open,
                'high': ha_high,
                'low': ha_low,
                'close': ha_close,
            })

        return heikin_ashi_data

    def clean_open_orders(self):
        """Check and clean open orders if necessary."""
        try:
            # Fetch all open orders.
            open_trades = self.ib.reqOpenOrders()
            open_orders_count = len(open_trades)

            # Fetch all positions.
            positions = self.ib.positions()
            active_positions = [pos for pos in positions if pos.position != 0]
            active_positions_count = len(active_positions)

            # If there are open orders but no active positions, cancel the open orders.
            if open_orders_count >= 1 and (active_positions_count == 0):
                logging.info(f"{open_orders_count} And {active_positions_count} Cancelling Order.")
                for trade in open_trades:
                    self.ib.cancelOrder(trade.order)
            else:
                logging.info(f"Open Orders: {open_orders_count}, Active Positions: {active_positions_count}")
        except Exception as e:
            # Log any errors encountered while cleaning open orders.
            logging.error(f"Error in cleaning open orders: {e}")

    def calculate_quantity(self, trade_amount_usdt):
        """Calculate the quantity of shares to trade based on the available USD amount."""
        try:
            # Fetch the last price of the stock.
            latest_price = self.get_last_price()
            if latest_price is not None and latest_price > 0:
                # Calculate the quantity to buy or sell.
                quantity = trade_amount_usdt / latest_price
                rounded_quantity = round(quantity)

                # Check for zero or negative quantity and log an error if found.
                if rounded_quantity <= 0:
                    logging.error(f"Calculated quantity is zero or negative: {rounded_quantity}")
                    return None

                return rounded_quantity
            else:
                logging.error("Unable to calculate quantity, latest price is unavailable or invalid.")
                return None
        except Exception as e:
            # Log any errors encountered while calculating quantity.
            logging.error(f'An unexpected error occurred while calculating quantity: {e}')
            return None

    def get_last_price(self):
        """Retrieve the last market price of the stock."""
        try:
            # Define the stock contract.
            contract = Stock(self.trading_symbol, 'SMART', 'USD')
            # Request market data for the contract.
            market_data = self.ib.reqMktData(contract, '', False, False)

            # Wait for the market data to be updated.
            self.ib.sleep(0.9)  # Sleep for a short period to allow data update.

            # Get the last price or close price from the market data.
            last_price = market_data.last if market_data.last else market_data.close

            # Check if the last price is valid, log an error if not.
            if last_price is None or last_price <= 0:
                logging.error(f'Invalid last price received: {last_price}')
                return None

            logging.info(f'Last price: {last_price}')
            return last_price
        except Exception as e:
            # Log any errors encountered while fetching the last price.
            logging.error(f'An error occurred while fetching the last price: {e}')
            return None


def main():
    # Instantiate the bot with the client ID, port number, and trading symbol.
    bot = InteractiveBrokersBot(clientId=5, port=7497, trading_symbol='SPY')

    # Connect to Interactive Brokers.
    bot.connect()

    # Fetch account information.
    bot.get_account_info()

    # Get USD balance.
    bot.get_balance()

    # Fetch stock information.
    bot.get_stock_info()

    # Get the last price of the stock.
    bot.get_last_price()

    # Fetch historical data with Heikin Ashi calculation if needed.
    use_heikin_ashi = False  # Set to True if you want to use Heikin Ashi.
    bot.fetch_historical_data(use_heikin_ashi)

    # Check active positions and orders.
    bot.check_active_positions_and_orders()

    # Clean open orders if necessary.
    bot.clean_open_orders()


if __name__ == "__main__":
    main()
