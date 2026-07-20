import csv
from can_log_tool import generate_can_log, analyze_can_log, detect_anomalies


def test_generate_can_log_creates_file(tmp_path):
    filename = tmp_path / "test_log.csv"
    generate_can_log(str(filename), num_rows=50)
    assert filename.exists()


def test_generate_can_log_row_count(tmp_path):
    filename = tmp_path / "test_log.csv"
    generate_can_log(str(filename), num_rows=50)

    with open(filename, "r") as f:
        rows = list(csv.reader(f))

    assert len(rows) == 51  # header + 50 data rows
    assert rows[0] == ["timestamp", "message_id", "signal_value"]


def test_analyze_can_log_computes_correct_stats(tmp_path):
    filename = tmp_path / "known_log.csv"
    # Hand-crafted, known values: mean=20, min=10, max=30
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "message_id", "signal_value"])
        writer.writerow([0.01, 256, 10])
        writer.writerow([0.02, 256, 20])
        writer.writerow([0.03, 256, 30])

    stats = analyze_can_log(str(filename))

    assert stats[256]["count"] == 3
    assert stats[256]["mean"] == 20
    assert stats[256]["min"] == 10
    assert stats[256]["max"] == 30


def test_detect_anomalies_flags_known_outlier(tmp_path):
    filename = tmp_path / "outlier_log.csv"
    # 10 values tightly clustered around 50-59, one obvious outlier at 500
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "message_id", "signal_value"])
        for i in range(10):
            writer.writerow([i * 0.01, 256, 50 + i])
        writer.writerow([0.11, 256, 500])

    anomalies = detect_anomalies(str(filename), threshold_std=2.0)
    flagged_values = [a[2] for a in anomalies]

    assert 500 in flagged_values


def test_detect_anomalies_no_false_positives_on_normal_data(tmp_path):
    filename = tmp_path / "normal_log.csv"
    # Tight, uniform cluster - nothing should be flagged
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "message_id", "signal_value"])
        for i in range(20):
            writer.writerow([i * 0.01, 256, 50 + (i % 3)])

    anomalies = detect_anomalies(str(filename), threshold_std=2.0)

    assert len(anomalies) == 0