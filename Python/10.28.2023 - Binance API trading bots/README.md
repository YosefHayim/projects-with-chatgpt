# Binance Trading Bot: Binance API Trading Bots

## Overview

This project includes several trading bots using the Binance API, each implementing a different strategy (MACD, RSI Long/Short, SMA, and Wyckoff). All bots share common modules for setup, account management, and real-time data handling, but differ in the specific strategy modules.

## Project Structure

### 1. **Binance_config**
Contains API keys and configuration settings used across all bots.

- `api_key`: Your Binance API key.
- `api_secret`: Your Binance API secret.

**Note**: Keep your API keys secure and private.

### 2. **Binance_setup**
Handles the general setup for all bots, including account information retrieval and order placement.

- **Functions**:
  - `get_account_info()`: Retrieves account details.
  - `get_usdt_balance()`: Retrieves your USDT balance.
  - `fetch_real_time_data()`: Collects real-time market data.
  - `place_market_order()`: Executes buy/sell orders.

### 3. **Strategy Modules**
Each bot has its own strategy module that defines the trading logic:

- **MACD Strategy**: (e.g., `Binance_strategy_AUDIOUSDT_MACD_15MIN_68_53_30.py`) 
  - Implements a MACD-based strategy for trading.
  - Monitors the market using the MACD indicator and executes trades accordingly.

- **RSI Long/Short Strategy**: (e.g., `Binance_strategy_RSI.py`)
  - Trades based on the Relative Strength Index (RSI), executing long positions on oversold conditions and short positions on overbought conditions.

- **SMA Strategy**: (e.g., `Binance_strategy_SMA.py`)
  - Trades based on Simple Moving Average (SMA) crossovers, such as buying when the price crosses above the 50-day SMA and selling when it crosses below.

- **Wyckoff Strategy**: (e.g., `Binance_strategy_Wyckoff.py`)
  - Uses the Wyckoff Method to identify accumulation and distribution phases for trading.

### 4. **Binance_telegram**
Handles Telegram notifications for all strategies.

- **Functions**:
  - `send_telegram_message()`: Sends updates to your Telegram chat.
  - `format_order_message()`: Formats trade details for easy readability.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/binance-trading-bot.git
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys** in `Binance_config`.

4. **Run a bot**:
   ```bash
   python Binance_strategy_<strategy_name>.py
   ```

   Replace `<strategy_name>` with the specific strategy you want to use (e.g., `AUDIOUSDT_MACD_15MIN_68_53_30`, `RSI`, `SMA`, `Wyckoff`).

## Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

This bot is for educational purposes only. Cryptocurrency trading is highly risky. The developers are not responsible for any financial losses.