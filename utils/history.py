import os
import csv
from datetime import datetime

HISTORY_FILE = os.path.join("results", "history.csv")


def log_result(file_name, stripe_count, visibility_percent, quality_score, condition):
    os.makedirs("results", exist_ok=True)
    file_exists = os.path.isfile(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["timestamp", "file_name", "stripe_count", "visibility_percent", "quality_score", "condition"]
            )

        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                file_name,
                stripe_count,
                visibility_percent,
                quality_score,
                condition,
            ]
        )


def read_history():
    if not os.path.isfile(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
