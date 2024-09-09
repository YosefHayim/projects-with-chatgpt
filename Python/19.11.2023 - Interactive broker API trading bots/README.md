# Interactive Brokers Trading Bots: MACD, RSI, SMA, and Wyckoff Strategies

This repository contains several trading bots built on a consistent structure, each tailored to different trading strategies, including MACD, RSI, SMA, and Wyckoff. Each bot automates trading using Interactive Brokers.

## Project Structure

### 1. **IB_setup_MACD (or RSI, SMA, Wyckoff)**
Handles account setup with Interactive Brokers, retrieving account information and placing orders.

- **Key Functions**:
  - `connect()`: Connects to Interactive Brokers.
  - `get_account_info()`: Retrieves account details.
  - `place_order()`: Places market orders.
  - `fetch_historical_data()`: Retrieves stock data.

**Important**: Modify the `clientId` and `port` to match your Interactive Brokers setup.

### 2. **IB_strategy_MACD_5MIN_72_55_28 (or RSI, SMA, Wyckoff)**
Implements the specific trading strategy (MACD, RSI, SMA, Wyckoff).

- **How It Works**:
  - Monitors the market and executes trades based on strategy signals.
  - Ensures only one active position at a time.
  - Logs trades and sends updates via Telegram.

### 3. **IB_telegrambot_MACD (or RSI, SMA, Wyckoff)**
Sends real-time trade notifications via Telegram.

- **Key Functions**:
  - `send_telegram_message()`: Sends updates.
  - `format_order_message()`: Formats trade details.

## Available Strategies

- **RSI Long Strategy**: Buys when RSI indicates oversold conditions.
- **SMA Strategy**: Trades based on simple moving average crossovers.
- **Wyckoff Strategy**: Trades during accumulation and distribution phases.
- **MACD Strategy**: Trades based on MACD line and signal line crossovers.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/interactive-brokers-trading-bots.git
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your IB `clientId` and `port`** in the `IB_setup` module.

4. **Run the bot**:
   ```bash
   python IB_strategy_MACD_5MIN_72_55_28.py  # Or the strategy of your choice
   ```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

**These bots are for educational purposes only.** Trading involves significant risk. The developers are not responsible for financial losses.