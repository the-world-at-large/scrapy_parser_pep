import csv
from collections import defaultdict
from datetime import datetime as dt

from constants import BASE_DIR


class PepParsePipeline:
    def __init__(self):
        self.status_count = defaultdict(int)

    def open_spider(self, spider):
        self.status_count.clear()

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
        RESULTS_DIR = 'results'
        FILE_FORMAT = 'csv'

        now = dt.now()
        now_formatted = now.strftime(TIME_FORMAT)
        file_name = f"status_summary_{now_formatted}.{FILE_FORMAT}"
        file_path = f"{BASE_DIR}/{RESULTS_DIR}/{file_name}"
        with open(file_path, "w", encoding="utf-8", newline='') as csvfile:
            fieldnames = ['Status', 'Count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for status, count in self.status_count.items():
                writer.writerow({'Status': status, 'Count': count})
            writer.writerow({'Status': 'Total',
                             'Count': sum(self.status_count.values())})
