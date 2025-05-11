"""CSV output handler with chunked writing and validation support."""

import csv
import os
from typing import List


class CSVValidationError(Exception):
    """Raised when CSV validation fails."""

    pass


class CSVOutputHandler:
    """Handles writing results to a CSV file with validation and chunked writing."""

    CHUNK_SIZE = 1000  # Number of rows to write at once

    def __init__(self, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def validate_data(self, header: List[str], rows: List[List[str]]) -> None:
        """Validate both header and row data in one pass.

        Args:
            header: The CSV header row
            rows: Data rows to validate

        Raises:
            CSVValidationError: If validation fails
        """
        # Validate header
        if not header:
            raise CSVValidationError("Header cannot be empty")
        if not all(isinstance(col, str) for col in header):
            raise CSVValidationError("All header columns must be strings")
        if len(set(header)) != len(header):
            raise CSVValidationError("Header columns must be unique")

        # Validate rows
        header_length = len(header)
        for row_num, row in enumerate(rows, 1):
            if len(row) != header_length:
                raise CSVValidationError(
                    f"Row {row_num} length {len(row)} does not match header length {header_length}"
                )

    def write(
        self,
        filename: str,
        header: List[str],
        rows: List[List[str]],
    ) -> None:
        """Write data to CSV file in chunks with validation, appending if file exists.

        Args:
            filename: Path to output file.
            header: List of column headers.
            rows: List of data rows.

        Raises:
            CSVValidationError: If data validation fails.
            IOError: If file operations fail.
        """
        # Validate all data upfront
        self.validate_data(header, rows)

        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            file_exists = os.path.exists(filename)
            mode = "a" if file_exists else "w"

            with open(filename, mode=mode, newline="", encoding=self.encoding) as file:
                writer = csv.writer(file)

                # Write header only for new files
                if not file_exists:
                    writer.writerow(header)

                # Write rows in chunks
                for i in range(0, len(rows), self.CHUNK_SIZE):
                    chunk = rows[i : i + self.CHUNK_SIZE]
                    for row in chunk:
                        writer.writerow(row)

        except IOError as e:
            raise IOError(f"Failed to write to CSV file {filename}: {str(e)}")

    def write_stream(
        self,
        filename: str,
        header: List[str],
        row_iterator: Iterator[List[str]],
    ) -> None:
        """Write data to CSV file from an iterator for memory efficiency.

        Args:
            filename: Path to output file.
            header: List of column headers.
            row_iterator: Iterator yielding data rows.

        Raises:
            CSVValidationError: If data validation fails.
            IOError: If file operations fail.
        """
        # Validate header upfront
        if not header:
            raise CSVValidationError("Header cannot be empty")
        if not all(isinstance(col, str) for col in header):
            raise CSVValidationError("All header columns must be strings")
        if len(set(header)) != len(header):
            raise CSVValidationError("Header columns must be unique")

        header_length = len(header)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            with open(filename, mode="w", newline="", encoding=self.encoding) as file:
                writer = csv.writer(file)
                writer.writerow(header)

                for row_num, row in enumerate(row_iterator, 1):
                    if len(row) != header_length:
                        raise CSVValidationError(
                            f"Row {row_num} length {len(row)} does not match header length {header_length}"
                        )
                    writer.writerow(row)

        except IOError as e:
            raise IOError(f"Failed to write to CSV file {filename}: {str(e)}")
