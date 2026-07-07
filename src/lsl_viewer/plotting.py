from collections import deque

import matplotlib.pyplot as plt

from lsl_viewer.config import DemoConfig


class RealtimeEegPlot:
    """Maintain a scrolling matplotlib plot for one EEG channel."""

    def __init__(self, config: DemoConfig, channel_index: int = 0) -> None:
        self.config = config
        self.channel_index = channel_index
        max_points = int(config.sample_rate * config.plot_window_seconds)
        self.times: deque[float] = deque(maxlen=max_points)
        self.values: deque[float] = deque(maxlen=max_points)

        plt.ion()
        self.figure, self.axes = plt.subplots()
        (self.line,) = self.axes.plot([], [], linewidth=1.5)
        self.axes.set_title(f"Realtime LSL EEG: {config.channel_names[channel_index]}")
        self.axes.set_xlabel("Seconds ago")
        self.axes.set_ylabel("Amplitude (microvolts)")
        self.axes.grid(True, alpha=0.3)

    def add_sample(self, timestamp: float, sample: list[float]) -> None:
        self.times.append(timestamp)
        self.values.append(sample[self.channel_index])

    def update(self) -> None:
        if len(self.times) < 2:
            return

        newest_time = self.times[-1]
        x = [timestamp - newest_time for timestamp in self.times]
        y = list(self.values)
        self.line.set_data(x, y)
        self.axes.set_xlim(-self.config.plot_window_seconds, 0.0)
        self.axes.relim()
        self.axes.autoscale_view(scalex=False, scaley=True)
        self.figure.canvas.draw_idle()
        self.figure.canvas.flush_events()

    def keep_open(self) -> None:
        plt.ioff()
        plt.show()
