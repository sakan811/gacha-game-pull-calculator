# CSV output handler stub
import csv
from typing import List, Any

class CSVOutputHandler:
    """Handles writing results to a CSV file."""
    def write(self, filename: str, header: List[str], rows: List[List[Any]]):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
