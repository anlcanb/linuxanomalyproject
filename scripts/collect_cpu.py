import psutil
import csv
import time
from datetime import datetime
import os

# Dinamik dosya yolu
FILENAME = "data/cpu_usage.csv"
INTERVAL = 5

# etiketleme fonksiyonu
def label_cpu(cpu_value):
    if cpu_value > 90:
        return "anomalous"
    elif cpu_value > 30:
        return "under_load"
    else:
        return "normal"

# Dosya başlığını yaz (yoksa)
def write_header_if_needed():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "cpu_percent", "label"])

# Veriyi oku, etiketle
def log_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)
    label = label_cpu(cpu)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [timestamp, cpu, label]

# CSV'ye yaz
def append_to_csv(row):
    with open(FILENAME, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

if __name__ == "__main__":
    print(" CPU monitoring started... (CTRL+C to stop)\n")
    write_header_if_needed()
    try:
        while True:
            row = log_cpu_usage()
            append_to_csv(row)
            print("Logged:", row)
            time.sleep(INTERVAL - 1)
    except KeyboardInterrupt:
        print("\n Monitoring stopped.")
