import os
import csv
import threading
import datetime

# Thread safety lock
csv_lock = threading.Lock()

def get_today_filename(folder, prefix):
    """Generate the filename with a prefix based on today's date."""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{prefix}_{today}.csv"
    return os.path.join(folder, filename)

def initialize_csv(folder, prefix):
    """Initialize a CSV file for the given folder, ensuring it exists."""
    os.makedirs(folder, exist_ok=True)  # Create directory if it doesn't exist
    filename = get_today_filename(folder, prefix)

    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

def save_to_csv(folder, prefix, data):
    """Append raw JSON data to a CSV file in the specified folder."""
    filename = get_today_filename(folder, prefix)

    with csv_lock:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data])  # Write data as a new row
