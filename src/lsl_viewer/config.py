from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DemoConfig:
    """Shared settings for the simulated EEG LSL demo."""

    stream_name: str = "SimulatedEEG"
    stream_type: str = "EEG"
    source_id: str = "lsl-viewer-simulated-eeg"
    channel_count: int = 4
    sample_rate: int = 250
    duration_seconds: float = 30.0
    plot_window_seconds: float = 5.0
    output_csv: Path = Path("data/simulated_eeg.csv")

    @property
    def channel_names(self) -> list[str]:
        return [f"EEG{i + 1}" for i in range(self.channel_count)]
