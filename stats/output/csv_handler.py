"""CSV output handler with chunked writing and validation support."""

import csv
import os
from typing import List


class CSVValidationError(Exception):
    """Raised when CSV validation fails."""

    pass


class CSVOutputHandler:
    """Simplified CSV writer for banner statistics."""

    def __init__(self, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def write(
        self,
        filename: str,
        header: List[str],
        rows: List[List[str]],
    ) -> None:
        """Write data to CSV file with basic validation."""
        if not header:
            raise ValueError("Header cannot be empty")
        if any(len(row) != len(header) for row in rows):
            raise ValueError("Row length must match header length")

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, mode="w", newline="", encoding=self.encoding) as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
