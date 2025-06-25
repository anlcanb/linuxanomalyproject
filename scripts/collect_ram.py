import psutil
import csv
import time
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILENAME  = os.path.join(BASE_DIR, "data", "ram_usage.csv")
INTERVAL  = 5  # saniye


def label_ram(p):
    if p > 90:
        return "anomalous"
    elif p > 30:
        return "under_load"
    else:
        return "normal"

def write_header_if_needed() -> None:
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="") as f:
            csv.writer(f).writerow(["timestamp", "ram_percent", "label"])


#cache ve buffer hariç tutuldu
def log_ram_usage() -> list:
    vm = psutil.virtual_memory()
    real_used = (vm.used - vm.buffers - vm.cached) / vm.total * 100
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label     = label_ram(real_used)
    return [timestamp, round(real_used, 2), label]



def append_to_csv(row: list) -> None:
    with open(FILENAME, "a", newline="") as f:
        csv.writer(f).writerow(row)


if __name__ == "__main__":
    print(" RAM monitoring started... (CTRL+C to stop)\n")
    write_header_if_needed()
    try:
        while True:
            row = log_ram_usage()
            append_to_csv(row)
            print("Logged:", row)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n Monitoring stopped.")

