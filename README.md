# LabStreamingLayer Basics Demo

A small Python project demonstrating the basic LabStreamingLayer flow:

1. Publish simulated EEG data with a `StreamOutlet`.
2. Resolve and receive that stream with a `StreamInlet`.
3. Display one channel in real time with `matplotlib`.
4. Save all received channels to CSV.

## Setup

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```powershell
python -m lsl_viewer.app
```

or, after installing the package in editable mode:

```powershell
python -m pip install -e .
lsl-viewer
```

The demo runs for 30 seconds by default and writes:

```text
data/simulated_eeg.csv
```

## Project Layout

```text
src/lsl_viewer/config.py      Shared demo settings
src/lsl_viewer/outlet.py      Simulated EEG StreamOutlet
src/lsl_viewer/inlet.py       StreamInlet resolver and receiver
src/lsl_viewer/plotting.py    Realtime matplotlib plot
src/lsl_viewer/csv_logger.py  CSV writer
src/lsl_viewer/app.py         Demo entry point
```

Change `DemoConfig` in `src/lsl_viewer/config.py` to adjust sample rate, channel count, runtime, output path, or plot window length.
