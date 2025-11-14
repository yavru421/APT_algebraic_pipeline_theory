#!/usr/bin/env python3
"""
Nexus Agent for APT Nexus Security Monitoring
Algebraic Pipeline Theory - Fatal Enforcement Mode

This agent monitors system and web logs for suspicious activity.
Upon detection, enters RED MODE: fatal halt with traceback.

Contract:
Inputs: log_files (list of paths), check_interval (int seconds)
Outputs: None (runs indefinitely until ⊥)
Errors: APTSuspiciousActivityError on detection
Success Criteria: Continuous monitoring without incidents
Algebraic: y = m(x) where m checks logs, y = ⊥ on suspicion
"""

import sys
import time
import re
import os
import csv
import traceback
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# APT Strict Mode Import
import strict_mode  # Enforces fatal exceptions

class APTSuspiciousActivityError(Exception):
    """Fatal error for suspicious activity in APT paradigm."""
    pass

class NexusAgent:
    def __init__(self, log_files: Optional[List[str]] = None, check_interval: int = 60):
        self.log_files: List[str] = log_files or [
            '/var/log/nginx/access.log',
            '/var/log/nginx/error.log',
            '/var/log/auth.log',
            '/var/log/syslog'
        ]
        self.check_interval: int = check_interval
        self.last_positions: Dict[str, int] = {log: 0 for log in self.log_files}
        self.traffic_csv: str = '/home/jdd/hybrid_api/traffic_log.csv'
        self._init_csv()
        self.suspicious_patterns: List[str] = [
            # Web attacks
            r'(?i)(union\s+select|script\s*>)',  # SQL injection, XSS
            r'(?i)(\.\./|\.\.\\)',  # Path traversal
            r'(?i)(eval\(|exec\(|system\()',  # Code injection
            # Brute force
            r'Failed password for',
            r'Invalid user',
            # Unusual traffic
            r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b.*\b(GET|POST)\b.*\b(php|asp|jsp)\b',  # Script kiddie scans
            # High frequency from same IP (simplified)
            # Note: Real implementation would track counters
        ]

    def _init_csv(self) -> None:
        if not os.path.exists(self.traffic_csv):
            with open(self.traffic_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'ip', 'request', 'status', 'user_agent'])

    def check_logs(self) -> None:
        for log_file in self.log_files:
            if not Path(log_file).exists():
                continue
            try:
                with open(log_file, 'r') as f:
                    f.seek(self.last_positions[log_file])
                    lines = f.readlines()
                    self.last_positions[log_file] = f.tell()
                    for line in lines:
                        if self.is_suspicious(line):
                            raise APTSuspiciousActivityError(f"Suspicious activity detected in {log_file}: {line.strip()}")
                        # Collect traffic data for access logs
                        if 'access.log' in log_file:
                            entry = self.parse_nginx_log(line)
                            if entry:
                                self.write_to_csv(entry)
            except PermissionError:
                # Log permission issue but continue
                print(f"Warning: Cannot read {log_file} - permission denied")

    def is_suspicious(self, line: str) -> bool:
        for pattern in self.suspicious_patterns:
            if re.search(pattern, line):
                return True
        return False

    def parse_nginx_log(self, line: str) -> Optional[List[str]]:
        """Parse Nginx access log line into [timestamp, ip, request, status, user_agent]"""
        # Assuming default log format: $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
        parts = line.split()
        if len(parts) < 9:
            return None
        try:
            ip = parts[0]
            timestamp = parts[3][1:] + ' ' + parts[4][:-1]  # e.g., 13/Nov/2025:00:00:00 +0000
            request = parts[5][1:-1]  # e.g., GET / HTTP/1.1
            status = parts[8]
            # User agent is from parts[11] onwards, joined
            user_agent_start = line.find('"', line.find('"', line.find('"') + 1) + 1) + 1
            user_agent = line[user_agent_start:].strip('"') if user_agent_start > 0 else ''
            return [timestamp, ip, request, status, user_agent]
        except (IndexError, ValueError):
            return None

    def write_to_csv(self, entry: List[str]) -> None:
        """Append entry to traffic CSV"""
        try:
            with open(self.traffic_csv, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(entry)
        except Exception as e:
            print(f"Failed to write to CSV: {e}")

    def enter_red_mode(self, error: Exception) -> None:
        print("\n❌ APT FATAL ERROR: Suspicious Activity Detected")
        print(f"Error: {error}")
        traceback.print_exc()
        # Red mode actions
        self.shutdown_services()
        self.log_incident(error)
        sys.exit(1)

    def shutdown_services(self) -> None:
        """Shutdown critical services in red mode."""
        services = ['nginx', 'uvicorn', 'fastapi']  # Adjust based on your setup
        for service in services:
            try:
                os.system(f'sudo systemctl stop {service}')
                print(f"Stopped {service}")
            except Exception as e:
                print(f"Failed to stop {service}: {e}")

    def log_incident(self, error: Exception) -> None:
        """Log the incident to a secure file."""
        log_path = '/var/log/apt_nexus_incidents.log'
        try:
            with open(log_path, 'a') as f:
                f.write(f"{time.ctime()}: {error}\n")
        except Exception as e:
            print(f"Failed to log incident: {e}")

    def run(self) -> None:
        print("⚙️ APT Nexus Agent Active: Monitoring logs for suspicious activity.")
        while True:
            try:
                self.check_logs()
                time.sleep(self.check_interval)
            except APTSuspiciousActivityError as e:
                self.enter_red_mode(e)
            except KeyboardInterrupt:
                print("Agent shutdown by user.")
                break
            except Exception as e:
                # Non-suspicious errors: log but continue
                print(f"Agent error: {e}")
                time.sleep(self.check_interval)

if __name__ == '__main__':
    agent = NexusAgent()
    agent.run()