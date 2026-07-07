import time

from lsl_viewer.config import DemoConfig
from lsl_viewer.csv_logger import CsvSampleLogger
from lsl_viewer.inlet import EegInlet
from lsl_viewer.outlet import SimulatedEegOutlet
from lsl_viewer.plotting import RealtimeEegPlot


def run_demo(config: DemoConfig) -> None:
    """Run the full outlet -> inlet -> plot -> CSV demonstration."""

    outlet = SimulatedEegOutlet(config)
    outlet.start()
    print(f"Publishing LSL stream {config.stream_name!r} at {config.sample_rate} Hz")

    try:
        inlet = EegInlet(config)
        plot = RealtimeEegPlot(config)
        deadline = time.monotonic() + config.duration_seconds

        with CsvSampleLogger(config.output_csv, config.channel_names) as logger:
            print(f"Receiving samples and saving CSV to {config.output_csv}")
            while time.monotonic() < deadline:
                pulled = inlet.pull_sample(timeout_seconds=0.2)
                if pulled is None:
                    continue

                sample, timestamp = pulled
                logger.write(timestamp, sample)
                plot.add_sample(timestamp, sample)
                plot.update()

        print("Demo finished. Close the plot window when you are done inspecting it.")
        plot.keep_open()
    finally:
        outlet.stop()


def main() -> None:
    run_demo(DemoConfig())


if __name__ == "__main__":
    main()
