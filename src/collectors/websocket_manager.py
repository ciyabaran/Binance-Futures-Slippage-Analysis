import threading
import websocket

# Store WebSocket instances and threads
websockets = []
threads = []

def start_websocket(url, on_message):
    """Start a WebSocket connection and keep track of it."""
    ws = websocket.WebSocketApp(url, on_message=on_message)
    websockets.append(ws)

    def run():
        ws.run_forever()
    
    thread = threading.Thread(target=run)
    thread.daemon = False  # Change daemon=False to properly manage shutdown
    threads.append(thread)
    thread.start()

def stop_websockets():
    """Gracefully close all WebSocket connections and stop threads."""
    print("\nClosing WebSocket connections...")
    
    for ws in websockets:
        try:
            ws.close()
        except Exception as e:
            print(f"Error closing WebSocket: {e}")

    for thread in threads:
        if thread.is_alive():
            thread.join(timeout=2)  # Ensure all threads are properly stopped

    websockets.clear()
    threads.clear()
    print("All WebSocket connections closed.")
