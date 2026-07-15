import csv
import random

# Simulate a CAN log: three message IDs, like a real vehicle network
MESSAGE_IDS = [256, 512, 1024]

def generate_can_log(filename, num_rows=1000):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "message_id", "signal_value"])  # header row

        timestamp = 0.0
        for _ in range(num_rows):
            timestamp += random.uniform(0.01, 0.05)  # time moves forward
            msg_id = random.choice(MESSAGE_IDS)

            # Different message IDs have different normal signal ranges
            if msg_id == 256:
                value = random.uniform(40, 60)
            elif msg_id == 512:
                value = random.uniform(80, 120)
            else:
                value = random.uniform(150, 250)

            # 5% chance of an outlier (simulating a sensor glitch)
            if random.random() < 0.05:
                value *= 3

            writer.writerow([round(timestamp, 3), msg_id, round(value, 2)])

    print(f"Generated {num_rows} rows into {filename}")

def analyze_can_log(filename):
    data_by_id = {}

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            msg_id = int(row["message_id"])
            value = float(row["signal_value"])

            if msg_id not in data_by_id:
                data_by_id[msg_id] = []
            data_by_id[msg_id].append(value)

    print("\n--- CAN Log Analysis ---")
    for msg_id, values in sorted(data_by_id.items()):
        count = len(values)
        mean_val = sum(values) / count
        min_val = min(values)
        max_val = max(values)

        variance = sum((v - mean_val) ** 2 for v in values) / count
        std_dev = variance ** 0.5

        print(f"\nMessage ID {msg_id}:")
        print(f"  Count: {count}")
        print(f"  Mean:  {mean_val:.2f}")
        print(f"  Min:   {min_val:.2f}")
        print(f"  Max:   {max_val:.2f}")
        print(f"  StdDev:{std_dev:.2f}")
def detect_anomalies(filename, threshold_std=2.0):
    # First pass: compute mean and std dev per message_id
    data_by_id = {}
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            msg_id = int(row["message_id"])
            value = float(row["signal_value"])
            if msg_id not in data_by_id:
                data_by_id[msg_id] = []
            data_by_id[msg_id].append(value)

    stats = {}
    for msg_id, values in data_by_id.items():
        mean_val = sum(values) / len(values)
        variance = sum((v - mean_val) ** 2 for v in values) / len(values)
        std_dev = variance ** 0.5
        stats[msg_id] = (mean_val, std_dev)

    # Second pass: flag any row that's too far from its message ID's normal range
    anomalies = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            msg_id = int(row["message_id"])
            value = float(row["signal_value"])
            timestamp = row["timestamp"]

            mean_val, std_dev = stats[msg_id]
            deviation = abs(value - mean_val)

            if std_dev > 0 and deviation > threshold_std * std_dev:
                num_std = deviation / std_dev
                anomalies.append((timestamp, msg_id, value, num_std))

    print(f"\n--- Anomaly Detection (threshold: {threshold_std} std devs) ---")
    print(f"Found {len(anomalies)} anomalies\n")
    for timestamp, msg_id, value, num_std in anomalies[:10]:
        print(f"  t={timestamp}  ID={msg_id}  value={value:.2f}  ({num_std:.1f} std devs from mean)")

    if len(anomalies) > 10:
        print(f"  ... and {len(anomalies) - 10} more")

    return anomalies
if __name__ == "__main__":
    generate_can_log("can_log.csv")
    analyze_can_log("can_log.csv")
    detect_anomalies("can_log.csv")