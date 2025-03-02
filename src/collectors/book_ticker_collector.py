from src.utils.file_handler import save_to_csv, initialize_csv
from src.collectors.websocket_manager import start_websocket

# Binance WebSocket URL for book ticker
BOOK_TICKER_URL = "wss://fstream.binance.com/ws/btcusdt@bookTicker"

# Directory for storing book ticker data
BOOK_TICKER_FOLDER = "data/raw/book_ticker"
BOOK_TICKER_PREFIX = "book_ticker"

# Initialize CSV storage
initialize_csv(BOOK_TICKER_FOLDER, BOOK_TICKER_PREFIX)

def on_book_ticker_message(ws, message):
    """Handle incoming book ticker messages and store them."""
    save_to_csv(BOOK_TICKER_FOLDER, BOOK_TICKER_PREFIX, message)

def start_book_ticker_collector():
    """Start the WebSocket for book ticker data collection."""
    start_websocket(BOOK_TICKER_URL, on_book_ticker_message)
