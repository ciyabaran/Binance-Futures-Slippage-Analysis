import time
import signal
from src.collectors.book_ticker_collector import start_book_ticker_collector
from src.collectors.trade_collector import start_trade_collector
from src.collectors.websocket_manager import stop_websockets

# Flag to track program running state
running = True

def signal_handler(sig, frame):
    """Handle keyboard interrupt (CTRL+C) to stop WebSockets."""
    global running
    print("\nStopping data collection...")
    running = False
    stop_websockets()  # Close all WebSocket connections

# Capture CTRL+C (SIGINT) to stop cleanly
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print("Starting data collection... Press CTRL+C to stop.")

    # Start WebSocket connections
    start_book_ticker_collector()
    start_trade_collector()

    # Keep running until interrupted
    while running:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break  # Just in case

    print("Data collection stopped successfully.")
