import csv
from pathlib import Path
from typing import TextIO


class CsvSampleLogger:
    """Write received LSL samples to a timestamped CSV file."""

    def __init__(self, path: Path, channel_names: list[str]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._file: TextIO = path.open("w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file)
        self._writer.writerow(["lsl_timestamp", *channel_names])

    def write(self, timestamp: float, sample: list[float]) -> None:
        self._writer.writerow([f"{timestamp:.6f}", *sample])

    def close(self) -> None:
        self._file.close()

    def __enter__(self) -> "CsvSampleLogger":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
