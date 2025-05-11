import csv


class CSVOutputHandler:
    """Handles writing results to a CSV file."""

    def write(
        self,
        filename: str,
        header: list[str],
        rows: list[list[str]],
        metadata_row: list[str] | None = None,
    ) -> None:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if metadata_row is not None:
                writer.writerow(metadata_row)
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)
