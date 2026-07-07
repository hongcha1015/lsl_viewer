from __future__ import annotations

import math
import random
import threading
import time

from pylsl import StreamInfo, StreamOutlet, local_clock

from lsl_viewer.config import DemoConfig


class SimulatedEegOutlet:
    """Publish a small synthetic EEG-like stream through LabStreamingLayer."""

    def __init__(self, config: DemoConfig) -> None:
        self.config = config
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

        info = StreamInfo(
            name=config.stream_name,
            type=config.stream_type,
            channel_count=config.channel_count,
            nominal_srate=config.sample_rate,
            channel_format="float32",
            source_id=config.source_id,
        )
        self._add_channel_metadata(info)
        self.outlet = StreamOutlet(info)

    def start(self) -> None:
        """Start publishing in a background thread."""

        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._publish_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Ask the publishing thread to stop and wait briefly for it."""

        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)

    def _add_channel_metadata(self, info: StreamInfo) -> None:
        channels = info.desc().append_child("channels")
        for name in self.config.channel_names:
            channel = channels.append_child("channel")
            channel.append_child_value("label", name)
            channel.append_child_value("unit", "microvolts")
            channel.append_child_value("type", self.config.stream_type)

    def _publish_loop(self) -> None:
        period = 1.0 / self.config.sample_rate
        next_push = time.perf_counter()

        while not self._stop_event.is_set():
            elapsed = local_clock()
            sample = self._make_sample(elapsed)
            self.outlet.push_sample(sample, timestamp=elapsed)

            next_push += period
            sleep_for = next_push - time.perf_counter()
            if sleep_for > 0:
                time.sleep(sleep_for)

    def _make_sample(self, t: float) -> list[float]:
        """Create multi-channel EEG-like data with alpha rhythm and noise."""

        sample = []
        for channel_index in range(self.config.channel_count):
            alpha_hz = 9.0 + channel_index * 0.7
            slow_hz = 1.0 + channel_index * 0.2
            alpha = 35.0 * math.sin(2.0 * math.pi * alpha_hz * t)
            slow_wave = 12.0 * math.sin(2.0 * math.pi * slow_hz * t)
            noise = random.gauss(0.0, 4.0)
            sample.append(alpha + slow_wave + noise)
        return sample
