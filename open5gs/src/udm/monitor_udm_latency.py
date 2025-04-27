import re
from prometheus_client import start_http_server, Gauge
import subprocess
import time

# Define Prometheus Gauges for different ss statistics
tcp_established_gauge = Gauge('tcp_established_connections', 'Number of established TCP connections')
tcp_rtt_gauge = Gauge('tcp_average_rtt', 'Average Round-Trip Time (RTT) for TCP connections in ms')
tcp_total_rtt_gauge = Gauge('tcp_total_rtt', 'Cumulative Round-Trip Time (RTT) for TCP connections in ms')  # New Gauge
tcp_cwnd_gauge = Gauge('tcp_cwnd', 'Congestion Window (CWND) for TCP connections')
tcp_pacing_rate_gauge = Gauge('tcp_pacing_rate', 'Pacing rate of TCP connections (Gbps)')
tcp_delivery_rate_gauge = Gauge('tcp_delivery_rate', 'Delivery rate of TCP connections (Gbps)')
tcp_bytes_sent_gauge = Gauge('tcp_bytes_sent', 'Bytes sent over TCP connections')
tcp_bytes_acked_gauge = Gauge('tcp_bytes_acked', 'Bytes acknowledged over TCP connections')
tcp_bytes_received_gauge = Gauge('tcp_bytes_received', 'Bytes received over TCP connections')

# Global variable for cumulative RTT
cumulative_rtt = 0.0  # Initialize cumulative RTT

# UDM IP address to filter
udm_ip = "127.0.0.12"

# Function to capture ss output
def capture_ss_stats():
    cmd = ["ss", "-t", "-i", f"dst {udm_ip}"]  # Filter by destination IP (UDM)
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    return output

# Function to parse the ss output for relevant metrics, filtered by UDM IP
def parse_ss_output(output):
    established_count = 0
    total_rtt = 0.0
    rtt_samples = 0
    total_cwnd = 0
    total_pacing_rate = 0.0
    total_delivery_rate = 0.0
    total_bytes_sent = 0
    total_bytes_acked = 0
    total_bytes_received = 0

    # Split the output into lines and process them
    lines = output.splitlines()

    for i, line in enumerate(lines):
        if "ESTAB" in line:  # Only process established connections
            # Process the second line containing metrics
            metrics_line = lines[i + 1] if i + 1 < len(lines) else None
            if metrics_line:
                # Use regex to extract metrics
                rtt_match = re.search(r'rtt:(\d+\.\d+)/', metrics_line)
                if rtt_match:
                    rtt = float(rtt_match.group(1))
                    total_rtt += rtt
                    rtt_samples += 1

                cwnd_match = re.search(r'cwnd:(\d+)', metrics_line)
                if cwnd_match:
                    cwnd = int(cwnd_match.group(1))
                    total_cwnd += cwnd

                pacing_rate_match = re.search(r'pacing_rate (\d+\.\d+)Gbps', metrics_line)
                if pacing_rate_match:
                    pacing_rate = float(pacing_rate_match.group(1))
                    total_pacing_rate += pacing_rate

                delivery_rate_match = re.search(r'delivery_rate (\d+\.\d+)Gbps', metrics_line)
                if delivery_rate_match:
                    delivery_rate = float(delivery_rate_match.group(1))
                    total_delivery_rate += delivery_rate

                bytes_sent_match = re.search(r'bytes_sent:(\d+)', metrics_line)
                if bytes_sent_match:
                    total_bytes_sent += int(bytes_sent_match.group(1))

                bytes_acked_match = re.search(r'bytes_acked:(\d+)', metrics_line)
                if bytes_acked_match:
                    total_bytes_acked += int(bytes_acked_match.group(1))

                bytes_received_match = re.search(r'bytes_received:(\d+)', metrics_line)
                if bytes_received_match:
                    total_bytes_received += int(bytes_received_match.group(1))

    # Calculate average RTT if samples exist
    average_rtt = total_rtt / rtt_samples if rtt_samples > 0 else 0.0
    return (established_count, average_rtt, total_rtt, total_cwnd, total_pacing_rate, total_delivery_rate, 
            total_bytes_sent, total_bytes_acked, total_bytes_received)

# Function to collect and update Prometheus metrics
def collect_ss_metrics():
    global cumulative_rtt  # Use the global cumulative RTT

    output = capture_ss_stats()
    (established, average_rtt, total_rtt, total_cwnd, total_pacing_rate, total_delivery_rate, 
     total_bytes_sent, total_bytes_acked, total_bytes_received) = parse_ss_output(output)

    # Update cumulative RTT
    cumulative_rtt += total_rtt

    # Set Prometheus metrics
    tcp_established_gauge.set(established)
    tcp_rtt_gauge.set(average_rtt)
    tcp_total_rtt_gauge.set(cumulative_rtt)  # Update the total RTT gauge
    tcp_cwnd_gauge.set(total_cwnd)
    tcp_pacing_rate_gauge.set(total_pacing_rate)
    tcp_delivery_rate_gauge.set(total_delivery_rate)
    tcp_bytes_sent_gauge.set(total_bytes_sent)
    tcp_bytes_acked_gauge.set(total_bytes_acked)
    tcp_bytes_received_gauge.set(total_bytes_received)

if __name__ == "__main__":
    # Start Prometheus exporter on port 8000
    start_http_server(8000)
    print("Exporter started on port 8000...")

    # Collect metrics every 10 seconds
    while True:
        collect_ss_metrics()
        time.sleep(10)
