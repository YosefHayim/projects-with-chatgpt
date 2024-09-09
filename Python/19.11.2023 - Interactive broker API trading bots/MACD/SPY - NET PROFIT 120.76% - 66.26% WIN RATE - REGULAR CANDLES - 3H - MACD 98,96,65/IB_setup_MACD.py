import logging
from ib_insync import IB, Stock, Order, util

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InteractiveBrokersBot:
    def __init__(self, clientId, port, trading_symbol):
        self.clientId = 1 # your client id from interactive brokers app
        self.clientId = clientId
        self.port = 1111 # port number from interactive brokers app
        self.ib = IB()
        self.trading_symbol = trading_symbol  # Trading symbol, e.g., 'AAPL'

    def connect(self):
        """Connect to Interactive Brokers TWS or Gateway."""
        try:
            self.ib.connect('127.0.0.1', self.port, clientId=self.clientId)
            logging.info("Connected to Interactive Brokers.")
        except Exception as e:
            logging.error(f'Connection error: {e}')

    def get_account_info(self):
        """Retrieve account information."""
        try:
            account_info = self.ib.accountValues()
            logging.info('Account information retrieved successfully.')
            return account_info
        except Exception as e:
            logging.error(f'Error getting account info: {e}')
            return None

    def get_balance(self):
        """Retrieve USD balance."""
        try:
            usd_balance = next(
                val for val in self.ib.accountValues() if val.tag == 'CashBalance' and val.currency == 'USD')
            logging.info(f"USD balance: {usd_balance.value}")
            return usd_balance.value
        except Exception as e:
            logging.error(f'Error getting USD balance: {e}')
            return None

    def get_stock_info(self):
        """Retrieve stock information."""
        try:
            contract = Stock(self.trading_symbol, 'SMART', 'USD')
            self.ib.reqMktData(contract, '', False, False)
            data = self.ib.reqMktData(contract)
            self.ib.sleep(1)  # Adding a 1-second delay
            logging.info(f'Stock information retrieved successfully for {self.trading_symbol}.')
            return data
        except Exception as e:
            logging.error(f'Error getting stock info: {e}')
            return None

    def place_order(self, order_type, quantity):
        # Define the contract
        self.contract = Stock(self.trading_symbol, 'SMART', 'USD')

        # Market Order
        market_order = Order()
        market_order.action = order_type
        market_order.totalQuantity = quantity
        market_order.orderType = 'MKT'  # Market order type
        trade = self.ib.placeOrder(self.contract, market_order)
        self.ib.sleep(0.5)  # Adding a 0.5-second delay

        # Logging
        if hasattr(trade, 'order') and hasattr(trade.order, 'orderId'):
            order_id = trade.order.orderId
            logging.info(f'Market order placed: {trade}. Order ID: {order_id}')
        else:
            logging.error('Failed to place market order: Order details not found in trade object.')

        return trade


    def place_order_limit_tp_stp_trailing_stop(self, order_type, quantity):
        # Define the contract
        self.contract = Stock(self.trading_symbol, 'SMART', 'USD')

        # Fetch the last market price as a reference
        market_data = self.ib.reqMktData(self.contract, '', False, False)
        reference_price = market_data.last if market_data.last else market_data.close

        # Adjust the reference price for limit order
        limit_price = reference_price + 0.00001 if order_type == 'BUY' else reference_price - 0.00001

        # Limit Order
        limit_order = Order()
        limit_order.action = order_type
        limit_order.totalQuantity = quantity
        limit_order.orderType = 'LMT'
        limit_order.lmtPrice = limit_price  # Set the limit price
        trade = self.ib.placeOrder(self.contract, limit_order)

        # Place auxiliary orders using the reference price
        self.place_auxiliary_orders(reference_price, quantity, order_type)

        # Logging
        if hasattr(trade, 'order') and hasattr(trade.order, 'orderId'):
            order_id = trade.order.orderId
            logging.info(f'Limit order placed: {trade}. Order ID: {order_id}, Limit Price: {limit_price}')
        else:
            logging.error('Failed to place limit order: Order details not found in trade object.')

        return trade

    def place_auxiliary_orders(self, fill_price, quantity, order_type):
        # Adjusting the tick size for price calculation (e.g., 0.01 for stocks)
        tick_size = 0.01

        # Calculate prices for take profit and stop loss, rounded to the nearest tick size
        take_profit_price = round(
            (fill_price * 1.02 if order_type == 'BUY' else fill_price * 0.98) / tick_size) * tick_size
        stop_loss_price = round(
            (fill_price * 0.98 if order_type == 'BUY' else fill_price * 1.02) / tick_size) * tick_size

        # Take Profit Order
        tp_order = Order()
        tp_order.action = 'SELL' if order_type == 'BUY' else 'BUY'
        tp_order.totalQuantity = quantity
        tp_order.orderType = 'LMT'
        tp_order.lmtPrice = take_profit_price
        self.ib.placeOrder(self.contract, tp_order)

        # Stop Loss Order
        sl_order = Order()
        sl_order.action = 'SELL' if order_type == 'BUY' else 'BUY'
        sl_order.totalQuantity = quantity
        sl_order.orderType = 'STP'
        sl_order.auxPrice = stop_loss_price
        self.ib.placeOrder(self.contract, sl_order)

        # Trailing Stop Order
        trailing_stop_order = Order()
        trailing_stop_order.action = 'SELL' if order_type == 'BUY' else 'BUY'
        trailing_stop_order.totalQuantity = quantity
        trailing_stop_order.orderType = 'TRAIL'
        trailing_stop_order.trailingPercent = 0.1  # 0.1% trailing stop
        trailing_stop_order.trailStopPrice = fill_price
        self.ib.placeOrder(self.contract, trailing_stop_order)

    def check_active_positions_and_orders(self):
        """Retrieve all positions without filtering for active positions."""
        try:
            # Force a refresh of data
            self.ib.reqPositions()

            # Fetch positions
            positions = self.ib.positions()
            self.ib.sleep(1)  # Adding a 1-second delay

            # Validate fetched data
            if not isinstance(positions, list):
                logging.error("Expected a list for positions")
                return None

            # Create a summary of all positions
            positions_summary = {
                'positions': positions
            }

            # Debug log for summary
            logging.debug(f"Positions summary: {positions_summary}")
            return positions_summary

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    def fetch_historical_data(self, use_heikin_ashi=False):
        """Fetch historical data and optionally convert it to Heikin Ashi format."""
        try:
            contract = Stock(self.trading_symbol, 'SMART', 'USD')
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr='3 D',
                barSizeSetting='3 hours',
                whatToShow='TRADES',
                useRTH=False,
                formatDate=1,
                keepUpToDate=True
            )
            self.ib.sleep(1)
            logging.info(f'Historical data for {self.trading_symbol} retrieved. Total bars: {len(bars)}')

            # Convert the data to the desired format
            formatted_data = [
                {'date': util.formatIBDatetime(bar.date), 'open': bar.open, 'high': bar.high, 'low': bar.low,
                 'close': bar.close, 'volume': bar.volume} for bar in bars]

            # If Heikin Ashi candles are to be used, calculate and integrate them
            if use_heikin_ashi:
                heikin_ashi_data = self.calculate_heikin_ashi(formatted_data)
                # Commenting out the following line will stop logging the aggregated Heikin Ashi data
                # logging.info(f'Heikin Ashi Data: {heikin_ashi_data}')
                for data in heikin_ashi_data:
                    logging.info(f"Heikin Ashi Bar Data: {data}")

                return heikin_ashi_data

            return formatted_data

        except Exception as e:
            logging.error(f'An error occurred while fetching historical data: {e}')
            return None

    def calculate_heikin_ashi(self, ohlcv_data):
        """Calculate Heikin Ashi candles from OHLCV data."""
        heikin_ashi_data = []
        for i, row in enumerate(ohlcv_data):
            if i == 0:  # For the first candle, HA values are the same as the regular values
                ha_open = row['open']
                ha_close = row['close']
                ha_high = row['high']
                ha_low = row['low']
            else:
                # Heikin Ashi Open is the average of the previous HA Open and HA Close
                ha_open = (heikin_ashi_data[i - 1]['open'] + heikin_ashi_data[i - 1]['close']) / 2
                # Heikin Ashi Close is the average of the current Open, High, Low, Close
                ha_close = (row['open'] + row['high'] + row['low'] + row['close']) / 4
                # Heikin Ashi High is the maximum of the current High, HA Open, HA Close
                ha_high = max(row['high'], ha_open, ha_close)
                # Heikin Ashi Low is the minimum of the current Low, HA Open, HA Close
                ha_low = min(row['low'], ha_open, ha_close)

            heikin_ashi_data.append({
                'date': row['date'],
                'open': ha_open,
                'high': ha_high,
                'low': ha_low,
                'close': ha_close,
            })

        return heikin_ashi_data

    def clean_open_orders(self):
        try:
            open_trades = self.ib.reqOpenOrders()
            open_orders_count = len(open_trades)

            # Fetch positions
            positions = self.ib.positions()
            active_positions = [pos for pos in positions if pos.position != 0]
            active_positions_count = len(active_positions)

            # Logic for cancelling order
            if open_orders_count >= 1 and (active_positions_count == 0):
                logging.info(f"{open_orders_count} And {active_positions_count} Cancelling Order.")
                for trade in open_trades:
                    self.ib.cancelOrder(trade.order)

            else:
                logging.info(f"Open Orders: {open_orders_count}, Active Positions: {active_positions_count}")
        except Exception as e:
            logging.error(f"Error in cleaning open orders: {e}")

    def calculate_quantity(self, trade_amount_usdt):
        try:
            latest_price = self.get_last_price()
            if latest_price is not None and latest_price > 0:
                quantity = trade_amount_usdt / latest_price
                rounded_quantity = round(quantity)

                # Adding an additional check for zero quantity
                if rounded_quantity <= 0:
                    logging.error(f"Calculated quantity is zero or negative: {rounded_quantity}")
                    return None

                return rounded_quantity
            else:
                logging.error("Unable to calculate quantity, latest price is unavailable or invalid.")
                return None
        except Exception as e:
            logging.error(f'An unexpected error occurred while calculating quantity: {e}')
            return None

    def get_last_price(self):
        try:
            contract = Stock(self.trading_symbol, 'SMART', 'USD')
            market_data = self.ib.reqMktData(contract, '', False, False)

            # Wait for the market data to be updated
            self.ib.sleep(0.9)  # Sleep for a short period to allow data update

            last_price = market_data.last if market_data.last else market_data.close

            if last_price is None or last_price <= 0:
                logging.error(f'Invalid last price received: {last_price}')
                return None

            logging.info(f'Last price: {last_price}')
            return last_price
        except Exception as e:
            logging.error(f'An error occurred while fetching the last price: {e}')
            return None


def main():
    # Instantiate the bot
    bot = InteractiveBrokersBot(clientId=5, port=7497, trading_symbol='SPY')

    # Connect to Interactive Brokers
    bot.connect()

    # Fetch account information
    bot.get_account_info()

    # Get USD balance
    bot.get_balance()

    # Fetch stock information
    bot.get_stock_info()

    bot.get_last_price()

    # Fetch historical data with Heikin Ashi calculation
    use_heikin_ashi = False  # Set to False if you don't want to use Heikin Ashi
    bot.fetch_historical_data(use_heikin_ashi)

    bot.check_active_positions_and_orders()

    # Check and clean active positions and orders
    bot.clean_open_orders()


if __name__ == "__main__":
    main()

