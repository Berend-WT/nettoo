import csv
import json
import sys
import os

out_path = os.path.join(os.path.dirname(__file__), "results_07.csv")
data_path = sys.argv[1]

with open(data_path, "r", encoding="utf-8") as f:
    rows = json.load(f)

file_exists = os.path.exists(out_path)
write_header = not file_exists or os.path.getsize(out_path) == 0

with open(out_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["excel_row", "bron_url", "geverifieerd", "gecorrigeerd_antwoord", "opmerking"])
    if write_header:
        writer.writeheader()
    for row in rows:
        writer.writerow(row)

print(f"Wrote {len(rows)} rows to {out_path}")
