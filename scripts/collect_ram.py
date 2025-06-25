import psutil
import csv
import time
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILENAME = os.path.join(BASE_DIR, "data", "ram_usage.csv")
INTERVAL = 5  

# RAM kullanımına göre etiket verildi(cache-buffer gözetilerek)
def label_ram(p):
    if p > 85:
        return "anomalous"
    elif p > 50:
        return "under_load"
    else:
        return "normal"


def write_header_if_needed():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "ram_percent", "label"])

# cache ve buffer değerleri dahil
def log_ram_usage():
    vm = psutil.virtual_memory()
    ram_percent = vm.percent
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = label_ram(ram_percent)
    return [timestamp, round(ram_percent, 2), label]

# CSV'ye eklendi
def append_to_csv(row):
    with open(FILENAME, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

# Ana döngü
if __name__ == "__main__":
    print(" RAM monitoring started (vm.percent)... (CTRL+C to stop)\n")
    write_header_if_needed()
    try:
        while True:
            row = log_ram_usage()
            append_to_csv(row)
            print("Logged:", row)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n Monitoring stopped.")

