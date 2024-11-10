import os
from datetime import datetime


class ParseInfo:
    """Utility class to parse information files and returns data in a suitable format."""

    def __init__(self):
        # Change directory into launch-count/
        os.chdir(f"{os.path.dirname(os.path.abspath(__file__))}/")
        self.dates = self.parse_dates()
        self.locations = self.parse_file("info/locations.txt")

    def parse_file(self, file_path: str):
        """Parse the file passes in.
        Returns an array of data, separated by line."""

        # Read the file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Filter out comments or invalid lines
        # Also make every string lowercase
        data_array = [
            line.strip().lower()
            for line in lines
            if line.strip() and not line.startswith("#")
        ]

        return data_array or []

    def parse_dates(self) -> list[datetime]:
        """Converts strings into Datetime objects."""
        dates = self.parse_file("info/dates.txt")

        for index, date in enumerate(dates):
            y, mo, d, h, mi, s = map(int, date.split(","))
            dates[index] = datetime(y, mo, d, h, mi, s)

        # Sort the dates in order of: earliest to latest
        dates = sorted(dates)

        return dates