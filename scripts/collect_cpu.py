import psutil
import csv
import time
from datetime import datetime
import os

# Dosya konumu
FILENAME = "data/cpu_usage.csv"
INTERVAL = 5  # saniye

# CSV dosyası gerekiyorsa ekle
def write_header_if_needed():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "cpu_percent"])

# CPU kullanımını alındı ve zamanla birlikte dönüldü
def log_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)  # 1 sn ölçüm alır
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [timestamp, cpu]

# Veri CSV dosyasına eklndi
def append_to_csv(row):
    with open(FILENAME, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

if __name__ == "__main__":
    print(" CPU izleme başlatıldı... (Durdurmak için CTRL+C)\n")
    write_header_if_needed()
    try:
        while True:
            row = log_cpu_usage()
            append_to_csv(row)
            print("Kayıt:", row)
            time.sleep(INTERVAL - 1)  # çünkü zaten 1 sn ölçüm yapıldı
    except KeyboardInterrupt:
        print("\nİzleme durduruldu.")

