# Tests for output/csv_handler.py
import pytest
import os
import csv
from output.csv_handler import CSVOutputHandler


@pytest.fixture
def csv_handler():
    """Return a CSVOutputHandler instance."""
    return CSVOutputHandler()


@pytest.fixture
def sample_csv_data():
    """Return sample data for CSV writing."""
    header = ["ID", "Name", "Value"]
    rows = [[1, "Alice", 100], [2, "Bob", 200], [3, "Charlie", 300]]
    return header, rows


def test_csv_output_handler_write(csv_handler, sample_csv_data, tmp_path):
    """Test the write method of CSVOutputHandler."""
    header, rows = sample_csv_data
    filename = tmp_path / "test_output.csv"

    csv_handler.write(str(filename), header, rows)

    assert os.path.exists(filename)

    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        read_header = next(reader)
        assert read_header == header

        read_rows = [row for row in reader]
        expected_rows_str = [[str(cell) for cell in row] for row in rows]
        assert read_rows == expected_rows_str


def test_csv_output_handler_write_empty_rows(csv_handler, tmp_path):
    """Test writing with an empty list of rows."""
    header = ["ColumnA", "ColumnB"]
    rows = []
    filename = tmp_path / "empty_output.csv"

    csv_handler.write(str(filename), header, rows)
    assert os.path.exists(filename)

    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        read_header = next(reader)
        assert read_header == header
        with pytest.raises(StopIteration):
            next(reader)


def test_csv_output_handler_write_special_characters(csv_handler, tmp_path):
    """Test writing data with special characters like commas and quotes."""
    header = ["ID", "Description"]
    rows = [
        [1, "Item with a comma, in description"],
        [2, 'Item with "quotes" in description'],
        [3, 'Item with "quotes" and a comma, in description'],
    ]
    filename = tmp_path / "special_chars_output.csv"
    csv_handler.write(str(filename), header, rows)
    assert os.path.exists(filename)

    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        read_header = next(reader)
        assert read_header == header
        read_rows = [row for row in reader]
        expected_rows_str = [[str(cell) for cell in row] for row in rows]
        assert read_rows == expected_rows_str
