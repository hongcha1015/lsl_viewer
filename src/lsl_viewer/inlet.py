from __future__ import annotations

from pylsl import StreamInlet, resolve_byprop

from lsl_viewer.config import DemoConfig


class EegInlet:
    """Resolve and receive samples from the simulated EEG LSL stream."""

    def __init__(self, config: DemoConfig, timeout_seconds: float = 10.0) -> None:
        streams = resolve_byprop(
            prop="name",
            value=config.stream_name,
            minimum=1,
            timeout=timeout_seconds,
        )
        if not streams:
            raise RuntimeError(f"Could not find LSL stream named {config.stream_name!r}")

        self.inlet = StreamInlet(streams[0])
        self.channel_names = config.channel_names

    def pull_sample(self, timeout_seconds: float = 0.0) -> tuple[list[float], float] | None:
        """Return one sample and its LSL timestamp, or None if nothing is ready."""

        sample, timestamp = self.inlet.pull_sample(timeout=timeout_seconds)
        if sample is None:
            return None
        return sample, timestamp
