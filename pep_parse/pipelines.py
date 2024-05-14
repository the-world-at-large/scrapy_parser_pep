import csv
from collections import defaultdict
from datetime import datetime as dt

from pep_parse.constants import BASE_DIR, RESULTS_DIR, TIME_FORMAT, FILE_FORMAT


class PepParsePipeline:
    def __init__(self):
        self.status_count = defaultdict(int)

    def open_spider(self, spider):
        self.status_count.clear()

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        now_formatted = dt.now().strftime(TIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.{FILE_FORMAT}'
        file_path = f'{BASE_DIR}/{RESULTS_DIR}/{file_name}'
        with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['Status', 'Count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            rows = [{'Status': status, 'Count': count}
                    for status, count in self.status_count.items()]
            rows.append({'Status': 'Total', 'Count': sum(
                                            self.status_count.values())})

            writer.writerows(rows)
