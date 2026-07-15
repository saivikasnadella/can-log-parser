# CAN Log Analysis Tool

A small Python tool that simulates CAN bus log data, computes per-signal statistics, and flags anomalies using z-score analysis.

Built as a hands-on Python learning project, applying concepts from my automotive diagnostics background (Vector CANoe/CANalyzer, UDS, DTC analysis) to Python-based data analysis.

## What it does

1. **Generates synthetic CAN log data** (`generate_can_log`) — simulates three CAN message IDs with realistic per-signal value ranges and a controlled 5% injection rate of outlier values (simulating sensor glitches).

2. **Computes statistics per message ID** (`analyze_can_log`) — count, mean, min, max, and standard deviation for each signal, read back from the generated CSV.

3. **Detects anomalies** (`detect_anomalies`) — flags any reading more than 2 standard deviations from its signal's mean (z-score method), printing the timestamp, message ID, value, and how far out of range it is.

## Example output
Generated 1000 rows into can_log.csv
--- CAN Log Analysis ---
Message ID 256:
Count: 316
Mean:  56.02
StdDev:24.14
--- Anomaly Detection (threshold: 2.0 std devs) ---
Found 47 anomalies
t=0.151  ID=1024  value=671.23  (4.8 std devs from mean)

## Run it
python3 can_log_tool.py
Requires Python 3.11+. No external dependencies — uses only the standard library (`csv`, `random`).

## Background

I work as a Vehicle Integration Engineer on autonomous Class 8 trucks, with daily experience in CAN/J1939 diagnostics, UDS, and fault analysis using Vector CANoe/CANalyzer and DiagnosticLink. This project is part of building my Python skills for scripting and log analysis, applied directly to problems from my domain.