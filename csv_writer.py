import csv
from pathlib import Path

pairs = {"BTC-ETH", "BTC-XMR"}

for pair in pairs:
    log_file = open("AssetLogs/" + pair + ".csv", "a+")
    writer = csv.writer(log_file)
    writer.writerow([5,6,7,8,9])



