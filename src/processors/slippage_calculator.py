import json
import os
import pandas as pd

# Define file paths dynamically based on date
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))  # Get base directory
BOOK_TICKER_FOLDER = os.path.join(BASE_DIR, "data", "raw", "book_ticker")
TRADE_FOLDER = os.path.join(BASE_DIR, "data", "raw", "trades")
SLIPPAGE_FOLDER = os.path.join(BASE_DIR, "data", "processed")

# Ensure processed folder exists
os.makedirs(SLIPPAGE_FOLDER, exist_ok=True)

def get_csv_filename(folder, prefix, date):
    """Generate the correct file path based on date."""
    return os.path.join(folder, f"{prefix}_{date}.csv")

def load_json_from_csv(filename):
    """Loads JSON formatted lines from CSV file into a DataFrame."""
    if not os.path.exists(filename):
        print(f" File not found: {filename}")
        return pd.DataFrame()  # Return empty DataFrame if file doesn't exist
    
    with open(filename, "r", encoding="utf-8") as file:
        data = [json.loads(line.strip().strip('"').replace('""', '"')) for line in file]
    
    return pd.DataFrame(data)

def calculate_slippage(date):
    """Merges trade and book ticker data to calculate slippage with backward matching."""
    # Construct file paths
    book_ticker_file = get_csv_filename(BOOK_TICKER_FOLDER, "book_ticker", date)
    trade_file = get_csv_filename(TRADE_FOLDER, "trades", date)
    slippage_file = get_csv_filename(SLIPPAGE_FOLDER, "slippage", date)

    # Load data
    trade_df = load_json_from_csv(trade_file)
    book_df = load_json_from_csv(book_ticker_file)

    # If any data is missing, skip processing
    if trade_df.empty or book_df.empty:
        print(f"🚨 Skipping {date}: Missing trade or book ticker data.")
        return

    # Rename columns for clarity
    trade_df = trade_df.rename(columns={"e": "event_type_trade", "E": "event_time_trade", "s": "symbol_trade", 
                                         "a": "agg_trade_id", "p": "trade_price", "q": "trade_quantity", 
                                         "f": "first_trade_id", "l": "last_trade_id", "T": "trade_time_trade", 
                                         "m": "is_market_maker"})
    
    book_df = book_df.rename(columns={"e": "event_type_book", "E": "event_time_book", "s": "symbol_book", 
                                       "b": "bid_price", "B": "bid_quantity", "a": "ask_price", 
                                       "u": "order_book_update_id",
                                       "A": "ask_quantity", "T": "trade_time_book"})

    # Convert necessary columns to float
    trade_df["trade_price"] = trade_df["trade_price"].astype(float)
    book_df["bid_price"] = book_df["bid_price"].astype(float)
    book_df["ask_price"] = book_df["ask_price"].astype(float)

    # Merge using backward matching (nearest earlier book ticker)
    merged_df = pd.merge_asof(trade_df, book_df, 
                              left_on="trade_time_trade", 
                              right_on="trade_time_book", 
                              direction="backward")

    # Compute Mid Price
    merged_df["mid_price"] = (merged_df["bid_price"] + merged_df["ask_price"]) / 2

    # Compute Slippage
    merged_df["slippage_bps"] = merged_df.apply(
        lambda row: ((row["mid_price"] - row["trade_price"]) / row["trade_price"]) * 10000 
        if not row["is_market_maker"]  # Taker BUY işleminde slippage hesaplama
        else 
        ((row["trade_price"] - row["mid_price"]) / row["trade_price"]) * 10000,  # Taker SELL işlemi
        axis=1
    )   

    # Save results to CSV
    merged_df.to_csv(slippage_file, index=False)
    print(f" Slippage calculated and saved to {slippage_file}.")

if __name__ == "__main__":
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    calculate_slippage(today)
