import time
import threading
import psutil
import socket
import subprocess
import re
from typing import Optional
from tracer.core import BaseTracer
from tracer import LogDomain


class NetTracer(BaseTracer):
    """
    Network tracer that collects network metrics including:
    - Download/Upload speeds (basic estimation)
    - Ping latency
    - Packet loss
    - Bytes sent/received
    - Public IP address
    """

    def __init__(self, domain: LogDomain, interval: int = 60):
        """
        Initialize the NetTracer.

        Args:
            domain: The log domain (should be LogDomain.NET)
            interval: Time interval in seconds between metric collections (default: 60)
        """
        super().__init__(domain)
        self.interval = interval
        self._running = False
        self._stop_event = threading.Event()
        self.log_file = self.writer.file_path

    def start(self):
        """
        Start collecting network metrics at regular intervals.
        """
        self._running = True
        self._stop_event.clear()
        print(f"Started network monitoring (interval: {self.interval}s)")

        try:
            while not self._stop_event.is_set():
                metrics = self._collect_metrics()
                if metrics:
                    print(metrics)
                    self.writer.append(metrics)

                # Wait for interval or until stop is requested
                self._stop_event.wait(timeout=self.interval)
        except Exception as e:
            print(f"An error occurred during network tracing: {e}")
        finally:
            self._running = False
            print("Network monitoring stopped.")

    def stop(self):
        """
        Stop the network tracer.
        """
        self._stop_event.set()
        self._running = False
        print("Stopping network monitoring...")

    def _collect_metrics(self) -> dict:
        """
        Collect all network metrics.

        Returns:
            Dictionary containing network metrics
        """
        # Get network I/O counters
        net_io = psutil.net_io_counters()

        metrics = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "download": self._estimate_download_speed(),
            "upload": self._estimate_upload_speed(),
            "ping_ms": self._get_ping(),
            "packet_loss": self._get_packet_loss(),
            "public_ip": self._get_public_ip(),
        }

        return metrics

    def _estimate_download_speed(self) -> Optional[float]:
        """
        Estimate download speed by measuring bytes received over a short period.

        Returns:
            Download speed in Mbps or None if unable to measure
        """
        try:
            # Take initial measurement
            initial = psutil.net_io_counters()
            time.sleep(1)
            final = psutil.net_io_counters()

            # Calculate bytes per second and convert to Mbps
            bytes_per_sec = final.bytes_recv - initial.bytes_recv
            mbps = (bytes_per_sec * 8) / 1_000_000
            return round(mbps, 2)
        except Exception:
            return None

    def _estimate_upload_speed(self) -> Optional[float]:
        """
        Estimate upload speed by measuring bytes sent over a short period.

        Returns:
            Upload speed in Mbps or None if unable to measure
        """
        try:
            # Take initial measurement
            initial = psutil.net_io_counters()
            time.sleep(1)
            final = psutil.net_io_counters()

            # Calculate bytes per second and convert to Mbps
            bytes_per_sec = final.bytes_sent - initial.bytes_sent
            mbps = (bytes_per_sec * 8) / 1_000_000
            return round(mbps, 2)
        except Exception:
            return None

    def _get_ping(self, host: str = "8.8.8.8") -> Optional[float]:
        """
        Get ping latency to a host.

        Args:
            host: Host to ping (default: Google DNS)

        Returns:
            Ping latency in milliseconds or None if unreachable
        """
        try:
            # Use platform-appropriate ping command
            import platform

            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", host]

            result = subprocess.run(command, capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                # Parse the output to get the time
                output = result.stdout
                if platform.system().lower() == "windows":
                    # Windows: "Reply from x.x.x.x: bytes=32 time=XXms TTL=XX"
                    match = re.search(r"time[=<](\d+)ms", output)
                else:
                    # Unix: "64 bytes from x.x.x.x: icmp_seq=1 ttl=XX time=XX.X ms"
                    match = re.search(r"time=(\d+\.?\d*)\s*ms", output)

                if match:
                    return float(match.group(1))
            return None
        except (subprocess.TimeoutExpired, Exception):
            return None

    def _get_packet_loss(
        self, host: str = "8.8.8.8", count: int = 4
    ) -> Optional[float]:
        """
        Get packet loss percentage.

        Args:
            host: Host to ping
            count: Number of ping requests

        Returns:
            Packet loss percentage (0-100) or None if unable to measure
        """
        try:
            import platform

            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, str(count), host]

            result = subprocess.run(command, capture_output=True, text=True, timeout=30)

            output = result.stdout

            if platform.system().lower() == "windows":
                # Windows: "Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)"
                match = re.search(r"\((\d+)%\s*(loss|perdida)\)", output)
            else:
                # Unix: "4 packets transmitted, 4 received, 0% packet loss"
                match = re.search(r"(\d+)%\s*packet loss", output)

            if match:
                return float(match.group(1))
            return None
        except (subprocess.TimeoutExpired, Exception):
            return None

    def _get_public_ip(self) -> Optional[str]:
        """
        Get the public IP address.

        Returns:
            Public IP address as a string or None if unable to determine
        """
        try:
            import urllib.request

            # Use a reliable IP detection service
            services = [
                "https://api.ipify.org",
                "https://ifconfig.me/ip",
                "https://icanhazip.com",
            ]

            for service in services:
                try:
                    with urllib.request.urlopen(service, timeout=5) as response:
                        ip = response.read().decode("utf-8").strip()
                        # Validate IP format
                        socket.inet_aton(ip)
                        return ip
                except Exception:
                    continue
            return None
        except Exception:
            return None
