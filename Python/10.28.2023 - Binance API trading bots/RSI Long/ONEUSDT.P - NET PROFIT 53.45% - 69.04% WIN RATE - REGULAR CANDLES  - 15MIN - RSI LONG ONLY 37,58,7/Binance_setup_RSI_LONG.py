import requests
from requests.exceptions import HTTPError
import time
import ccxt
import hmac
import hashlib
import logging


# Configure logging to include the time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BinanceBot:
    def __init__(self, api_key, api_secret):
        """Initialize the bot with API key, secret, and default parameters."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.exchange = ccxt.binanceusdm({
            'apiKey': self.api_key,
            'secret': self.api_secret,
        })
        self.pair = 'ONEUSDT'  # Default trading pair
        self.leverage = 20  # Default leverage level
        self.data = None  # To store fetched data
        self.limit = 300  # Limit for data fetching
        self.interval = '15m'  # Interval for data fetching

    def fetch_signature(self, query_string):
        """Create HMAC SHA256 signature for authenticated API requests."""
        return hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def get_account_info(self):
        try:
            # Get the Binance server time
            server_time = self.exchange.fetch_time()

            # Now fetch the balance with the adjusted timestamp
            account_info = self.exchange.fetch_balance(
                params={"type": "future", 'recvWindow': 5000, 'timestamp': server_time})
            logging.info('Account information retrieved successfully.')
            return account_info
        except ccxt.NetworkError as network_err:
            logging.error(f'Network error occurred: {network_err}')
        except ccxt.ExchangeError as exchange_err:
            logging.error(f'Exchange error occurred: {exchange_err}')
        except Exception as err:
            logging.error(f'Other error occurred: {err}')
        return None

    def get_usdt_balance(self):
        try:
            # Fetch futures balance
            balance_info = self.exchange.fetch_balance(params={"type": "future"})
            if 'total' in balance_info and 'USDT' in balance_info['total']:
                usdt_balance = balance_info['total']['USDT']
                logging.info(f"USDT balance: {usdt_balance}")
                return usdt_balance
            else:
                logging.error('USDT balance not found in futures wallet.')
                return None
        except Exception as e:
            logging.error(f'An unexpected error occurred: {e}')
            return None

    def get_stock_info(self):
        base_url = 'https://api.binance.com'
        endpoint = f'/api/v3/ticker/24hr'
        url = base_url + endpoint

        params = {
            'symbol': self.pair,
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            stock_info = response.json()
            logging.info(f'Last price of {self.pair}: {stock_info["lastPrice"]}')
        except HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logging.error(f'An error occurred: {err}')

    def set_margin_type(self, margin_type):
        try:
            response = self.exchange.setMarginMode(margin_type, self.pair)
            logging.info(f'Successfully set margin type to {margin_type} for {self.pair}.')
        except Exception as err:
            logging.error(f'An error occurred: {err}')

    def set_leverage(self):
        try:
            response = self.exchange.fapiPrivatePostLeverage({
                'symbol': self.pair,
                'leverage': self.leverage,
            })
            logging.info(f'Successfully set leverage to {self.leverage} for {self.pair}.')
        except Exception as err:
            logging.error(f'An error occurred: {err}')

    def get_leverage_bracket(self):
        try:
            response = self.exchange.fapiPrivateGetLeverageBracket({
                'symbol': self.pair,
            })
            logging.info(f'Leverage bracket for {self.pair} has been fetched.')
        except Exception as err:
            logging.error(f'An error occurred: {err}')

    def fetch_real_time_data(self, use_heikin_ashi=False):
        base_url = 'https://api.binance.com'
        endpoint = f'/api/v3/klines'
        params = {
            'symbol': self.pair,
            'interval': self.interval,
            'limit': self.limit
        }
        try:
            # Send a GET request to Binance API
            response = requests.get(base_url + endpoint, params=params)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            klines = response.json()

            # Initialize list to store formatted data
            formatted_data = []

            # Convert raw data to dictionary format for better readability
            for row in klines:
                formatted_data.append({
                    'timestamp': row[0],
                    'open': float(row[1]),
                    'high': float(row[2]),
                    'low': float(row[3]),
                    'close': float(row[4]),
                    'volume': float(row[5])
                })

            # If Heikin Ashi candles are to be used, calculate and integrate them
            if use_heikin_ashi:
                heikin_ashi_data = self.calculate_heikin_ashi(formatted_data)
                logging.info(f'Heikin Ashi Data: {heikin_ashi_data}')  # Log the Heikin Ashi data
                for i, data in enumerate(formatted_data):
                    data['ha_open'] = heikin_ashi_data[i]['open']
                    data['ha_high'] = heikin_ashi_data[i]['high']
                    data['ha_low'] = heikin_ashi_data[i]['low']
                    data['ha_close'] = heikin_ashi_data[i]['close']
                logging.info(f'Heikin Ashi data for {self.pair} has been calculated and integrated.')
            return formatted_data

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTPError while fetching data for {self.pair}: {e}")
            return None
        except requests.exceptions.ConnectionError as e:
            logging.error(f"ConnectionError while fetching data for {self.pair}: {e}")
            return None
        except requests.exceptions.Timeout as e:
            logging.error(f"TimeoutError while fetching data for {self.pair}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"RequestException while fetching data for {self.pair}: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while fetching data for {self.pair}: {e}")
            return None

    def calculate_heikin_ashi(self, ohlcv_data):
        heikin_ashi_data = []
        for i, row in enumerate(ohlcv_data):
            if i == 0:  # For the first candle, HA values are the same as the regular values
                ha_open = row['open']
                ha_close = row['close']
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
                'timestamp': row['timestamp'],
                'open': ha_open,
                'high': ha_high,
                'low': ha_low,
                'close': ha_close,
                'volume': row['volume']  # Volume is not modified for Heikin Ashi
            })

        return heikin_ashi_data

    def place_market_order(self, side, amount):
        try:
            # Place a market order for both opening and closing positions
            order = self.exchange.create_order(
                symbol=self.pair,
                type='MARKET',
                side=side,
                amount=amount,
            )
            logging.info(f"Market order placed: {order}")

            return order
        except Exception as err:
            logging.error(f'An error occurred: {err}')
            return None

    def place_market_order_and_tp(self, side, amount):
        try:
            # Place a market order for both opening and closing positions
            order = self.exchange.create_order(
                symbol=self.pair,
                type='MARKET',
                side=side,
                amount=amount,
            )
            logging.info(f"Market order placed: {order}")

            # Calculate take profit price
            if side == 'BUY':
                # If going long, set take profit 1% above the executed price
                take_profit_price = order['price'] * 1.001
            else:
                # If going short, set take profit 1% below the executed price
                take_profit_price = order['price'] * 0.999

            # Place a take profit limit order
            self.exchange.create_order(
                symbol=self.pair,
                type='LIMIT',
                side='SELL' if side == 'BUY' else 'BUY',
                amount=amount,
                price=take_profit_price,
                params={'reduceOnly': True}  # This ensures that the order will only reduce a position, not increase it
            )
            logging.info(f"Take profit limit order placed at: {take_profit_price}")

            return order
        except Exception as err:
            logging.error(f'An error occurred: {err}')
            return None

    def place_order_limit(self, side, amount):
        try:
            # Fetch the current market price
            current_price = self.get_last_price()
            if current_price is None:
                logging.error('Failed to fetch current market price')
                return None

            # Calculate the limit order price as a slight percentage above or below the current market price
            limit_order_price = current_price * (1 + 0.0005) if side == 'BUY' else current_price * (1 - 0.0005)

            # Place the limit order
            order = self.exchange.create_order(
                symbol=self.pair,
                type='LIMIT',
                side=side,
                price=limit_order_price,
                amount=amount,
            )
            logging.info(f"Limit order placed at {limit_order_price}: {order}")

            return order
        except Exception as err:
            logging.error(f'An error occurred: {err}')
            return None


    def place_order_ta_stp_trailing_stop(self, side, amount, trailing_percentage=1.01, stop_loss_percentage=1.5,take_profit_percentage=1.061):
        try:
            # Fetch the current market price
            current_price = self.get_last_price()
            if current_price is None:
                logging.error('Failed to fetch current market price')
                return None

            # Calculate the limit order price as a slight percentage above or below the current market price
            limit_order_price = current_price * (1 + 0.0005) if side == 'BUY' else current_price * (1 - 0.0005)

            # Place the limit order
            order = self.exchange.create_order(
                symbol=self.pair,
                type='LIMIT',
                side=side,
                price=limit_order_price,
                amount=amount,
            )
            logging.info(f"Limit order placed at {limit_order_price}: {order}")

            # Adjust the execution price based on the limit order price
            execution_price = float(order['price'])

            # Determine closing side based on the order side
            closing_side = 'BUY' if side == 'SELL' else 'SELL'

            # Calculate callbackRate for trailing stop, stop loss price, and take profit price
            callback_rate = trailing_percentage
            stop_loss_price = execution_price * (
                        1 - stop_loss_percentage / 100) if side == 'BUY' else execution_price * (
                        1 + stop_loss_percentage / 100)
            take_profit_price = execution_price * (
                        1 + take_profit_percentage / 100) if side == 'BUY' else execution_price * (
                        1 - take_profit_percentage / 100)

            # Create TRAILING_STOP_MARKET order with specified callback rate and activation price
            self.exchange.create_order(
                symbol=self.pair,
                type='TRAILING_STOP_MARKET',
                side=closing_side,
                amount=amount,
                params={
                    'callbackRate': trailing_percentage,
                    'activationPrice': execution_price,
                    'reduceOnly': 'True'
                }
            )
            logging.info(
                f"Trailing stop order set for {side} position with callback rate of {trailing_percentage}% at activation price {execution_price}")

            # Create STOP_MARKET order for fixed stop loss
            self.exchange.create_order(
                symbol=self.pair,
                type='STOP_MARKET',
                side=closing_side,
                amount=amount,
                params={
                    'stopPrice': stop_loss_price,
                    'reduceOnly': 'True'
                }
            )
            logging.info(f"Fixed stop loss order set for {side} position at price {stop_loss_price}")

            # Create TAKE_PROFIT_MARKET order for take profit
            self.exchange.create_order(
                symbol=self.pair,
                type='TAKE_PROFIT_MARKET',
                side=closing_side,
                amount=amount,
                params={
                    'stopPrice': take_profit_price,
                    'reduceOnly': 'True'
                }
            )
            logging.info(f"Take profit order set for {side} position at price {take_profit_price}")

            return order
        except Exception as err:
            logging.error(f'An error occurred: {err}')
            return None

    def get_active_order_count(self):
        try:
            # Fetch open orders for the specific symbol
            orders = self.exchange.fetch_open_orders(symbol=self.pair)
            order_count = len(orders)

            detailed_positions_info = []

            # Logging details of each open order
            for order in orders:
                logging.info(f"Open Order Details: {order}")

            # Fetch position information
            params = {
                'symbol': self.pair,
                'timestamp': self.exchange.nonce()
            }
            method = 'fapiPrivateV2GetPositionRisk'
            if hasattr(self.exchange, method):
                response = getattr(self.exchange, method)(params)

                # Check if response is not None
                if response is not None:
                    active_positions = [pos for pos in response if float(pos.get('positionAmt', '0')) != 0]
                    position_count = len(active_positions)

                    for position in active_positions:
                        # Initialize TP and SL order details as None
                        tp_order_details = None
                        sl_order_details = None

                        # Check each order to find TP and SL orders for the position
                        for order in orders:
                            if order['symbol'] == position['symbol']:
                                if order['type'] in ['TAKE_PROFIT', 'TAKE_PROFIT_LIMIT', 'TAKE_PROFIT_MARKET']:
                                    tp_order_details = order
                                elif order['type'] in ['STOP_LOSS', 'STOP_LOSS_LIMIT', 'STOP_LOSS_MARKET']:
                                    sl_order_details = order

                        # Prepare position details including TP and SL orders
                        position_detail = {
                            'symbol': position.get('symbol', 'N/A'),
                            'position_amt': position.get('positionAmt', 'N/A'),
                            'entry_price': position.get('entryPrice', 'N/A'),
                            'unrealized_profit': position.get('unRealizedProfit', 'N/A'),
                            'liquidation_price': position.get('liquidationPrice', 'N/A'),
                            'mark_price': position.get('markPrice', 'N/A'),
                            'leverage': position.get('leverage', 'N/A'),
                            'position_side': position.get('positionSide', 'N/A'),
                            'notional': position.get('notional', 'N/A'),
                            'tp_order_details': tp_order_details,
                            'sl_order_details': sl_order_details
                        }
                        detailed_positions_info.append(position_detail)
                else:
                    position_count = 0

            else:
                position_count = 0

            total_active = order_count + position_count
            logging.info(
                f"Active orders: {order_count}, Active positions: {position_count}, Total: {total_active}")
            logging.info(f"Position Details: {detailed_positions_info}")

            return total_active, detailed_positions_info
        except ccxt.NetworkError as e:
            logging.error(f'Network problem occurred: {e}')
        except ccxt.ExchangeError as e:
            logging.error(f'Exchange reported an error: {e}')
        except Exception as e:
            logging.error(f'An unexpected error occurred: {e}')

        return None, None

    def clean_open_orders(self):
        try:
            # Fetch open orders directly
            open_orders = self.exchange.fetch_open_orders(symbol=self.pair)
            open_orders_count = len(open_orders)

            # Fetch position information directly
            position_info = self.exchange.fapiPrivateV2GetPositionRisk({'symbol': self.pair})
            # Filter out zero positions
            active_positions = [pos for pos in position_info if float(pos['positionAmt']) != 0]
            active_positions_count = len(active_positions)
            logging.info(
                f"Evaluated Counts - Open Orders: {open_orders_count}, Active Positions: {active_positions_count}")

            # Close all open orders if no active positions are found
            if open_orders_count >= 1 and active_positions_count == 0:
                logging.info(
                    f"{open_orders_count} open order(s) found and no active positions. Canceling the open order(s).")
                self.exchange.cancel_all_orders(symbol=self.pair)

            # Close all active positions if found
            if active_positions_count > 0:
                logging.info(f"{active_positions_count} active position(s) found. Closing active position(s).")
                for position in active_positions:
                    self.close_position(position)

            else:
                logging.info(f"No action needed as there are no active positions and no open orders.")

        except Exception as e:
            logging.error(f"Error in cleaning open orders: {e}")

    def close_position(self, position):
        side = 'BUY' if float(position['positionAmt']) < 0 else 'SELL'
        amount = abs(float(position['positionAmt']))
        order = {
            'symbol': self.pair,
            'side': side,
            'type': 'MARKET',
            'amount': amount
        }
        self.exchange.create_order(**order)

    def calculate_quantity(self, trade_amount_usdt, decimal_places=5):
        try:
            latest_price = self.get_last_price()
            if latest_price is not None:
                quantity = (trade_amount_usdt * self.leverage) / latest_price
                notional_value = round(quantity * latest_price, decimal_places)  # Rounded notional value
                return quantity
            else:
                logging.error("Unable to calculate quantity, latest price is unavailable.")
                return 0  # Return 0 if the latest price is unavailable
        except Exception as e:
            logging.error(f'An unexpected error occurred while calculating quantity: {e}')
            return 0  # Return 0 in case of any error

    def get_last_price(self):
        try:
            ticker = self.exchange.fetch_ticker(self.pair)
            return ticker['last']
        except Exception as err:
            logging.error(f'An error occurred while fetching the last price: {err}')
            return None

def main():
    from Binance_config_ONEUSDT_RSI_LONG import api_key, api_secret

    # Instantiate the bot with the API keys
    bot = BinanceBot(api_key, api_secret)

    # Step 1: Log in and get account information
    account_info = bot.get_account_info()

    # Step 2: Get USDT balance using the account information
    if account_info:
        bot.get_usdt_balance()

    # Step 3: Fetch real-time data for the default trading pair and interval
    real_time_data = bot.fetch_real_time_data()

    # Step 4: Set margin type for the selected symbol
    margin_type = 'CROSS'
    bot.set_margin_type(margin_type)

    # Step 5: Set leverage for the selected symbol
    bot.set_leverage()

    # Step 6: Get leverage bracket information for the selected symbol
    bot.get_leverage_bracket()

    # Step 7: Fetch stock information for the selected symbol
    bot.get_stock_info()

    bot.get_active_order_count()

if __name__ == "__main__":
    main()