# Binance Futures Slippage Analysis

This project collects real-time market data from Binance Futures and analyzes trade slippage for BTC/USDT.

## Project Overview
The project consists of two main components:
1. **Data Collection Component**
2. **Analysis Component**

---
## 1. Data Collection Component
The data collection system connects to Binance Futures WebSockets API and retrieves real-time market data.

### Collected Data:
- **Book Ticker (best bid/ask prices):**
  - Streamed from `wss://fstream.binance.com/ws/btcusdt@bookTicker`
  - Stored in CSV format with timestamps
- **Aggregate Trade Data (executed trades):**
  - Streamed from `wss://fstream.binance.com/ws/btcusdt@aggTrade`
  - Stored in CSV format with timestamps

### Files:
- `book_ticker_collector.py`: Collects book ticker data.
- `trade_collector.py`: Collects aggregated trade data.
- `file_handler.py`: Handles CSV file storage.
- `websocket_manager.py`: Manages WebSocket connections.
- `main.py`: Main entry point to start data collection.
  

### How to Run Data Collection:
```sh
python main.py
```
Press `CTRL+C` to stop the data collection process.

---
## 2. Analysis Component
This component calculates trade slippage and identifies patterns under different market conditions.

### Slippage Calculation:
Slippage is calculated as the difference between the mid-price (mean of best bid/ask) and trade price.

#### Formula:
- **For Buy trades:**
  ```
  slippage_bps = (mid_price - trade_price) / trade_price * 10000
  ```
- **For Sell trades:**
  ```
  slippage_bps = (trade_price - mid_price) / trade_price * 10000
  ```

### Files:
- `slippage_calculator.py`: Merges trade and book ticker data to compute slippage.
- `Analyze.ipynb`: Jupyter Notebook for slippage pattern analysis.

### How to Run Slippage Calculation:
```sh
python slippage_calculator.py
```

---
## Folder Structure
```
/binance_slippage_analysis
├── data
│   ├── raw
│   │   ├── book_ticker/       # Raw book ticker data
│   │   ├── trades/            # Raw trade data
│   ├── processed
│   │   ├── slippage/          # Processed slippage data
│
├── src
│   ├── collectors
│   │   ├── book_ticker_collector.py
│   │   ├── trade_collector.py
│   │   ├── websocket_manager.py
│   ├── utils
│   │   ├── file_handler.py
│   ├── analysis
│   │   ├── slippage_calculator.py
│
├── main.py                    # Starts data collection
├── Analyze.ipynb               # Jupyter Notebook for analysis
├── README.md                   # Project documentation
```

---
## Requirements
Make sure you have Python and basic libraries installed along with the required dependencies.

### Install Dependencies:
```sh
pip install websocket-client pandas numpy plotlib
```

---
