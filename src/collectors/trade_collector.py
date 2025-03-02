from src.utils.file_handler import save_to_csv, initialize_csv
from src.collectors.websocket_manager import start_websocket

# Binance WebSocket URL for aggregated trades
TRADE_URL = "wss://fstream.binance.com/ws/btcusdt@aggTrade"

# Directory for storing trade data
TRADE_FOLDER = "data/raw/trades"
TRADE_PREFIX = "trades"

# Initialize CSV storage
initialize_csv(TRADE_FOLDER, TRADE_PREFIX)

def on_trade_message(ws, message):
    """Handle incoming trade messages and store them."""
    save_to_csv(TRADE_FOLDER, TRADE_PREFIX, message)

def start_trade_collector():
    """Start the WebSocket for trade data collection."""
    start_websocket(TRADE_URL, on_trade_message)
