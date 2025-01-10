#!/usr/bin/env python3
import os
import re
from datetime import datetime, timedelta, timezone
import glob
from collections import Counter

def count_recent_http_codes(log_dir, minutes=10):
    """Count HTTP response codes from logs in the past specified minutes."""
    current_time = datetime.now(timezone.utc)
    time_threshold = current_time - timedelta(minutes=minutes)
    
    # Counter for status codes by their first digit (2xx, 3xx, 4xx, 5xx)
    status_groups = Counter()
    # Counter for specific status codes
    specific_codes = Counter()
    
    # Process all HTTP log files
    for log_file in glob.glob(os.path.join(log_dir, 'Http-*.log')):
        with open(log_file, 'r') as f:
            for line in f:
                # Extract timestamp and status code
                match = re.search(r'\[(.*?)\].*" (\d{3})', line)
                if match:
                    timestamp_str, status_code = match.groups()
                    try:
                        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S +0000')
                        timestamp = timestamp.replace(tzinfo=timezone.utc)
                        
                        if timestamp >= time_threshold:
                            # Group by first digit (2xx, 3xx, etc.)
                            status_groups[f"{status_code[0]}xx"] += 1
                            # Also count specific codes
                            specific_codes[status_code] += 1
                    except ValueError:
                        continue

    return status_groups, specific_codes

def main():
    log_dir = "."
    minutes = 10
    
    print(f"\nAnalyzing last {minutes} minutes of HTTP traffic...")
    status_groups, specific_codes = count_recent_http_codes(log_dir, minutes)
    
    if not status_groups:
        print("No HTTP traffic found in the specified time period.")
        return
    
    # Print summary by status code groups
    print("\nStatus Code Groups:")
    print("-" * 30)
    total_requests = sum(status_groups.values())
    for group, count in sorted(status_groups.items()):
        percentage = (count / total_requests) * 100
        print(f"{group}: {count} ({percentage:.1f}%)")
    

    error_codes = {code: count for code, count in specific_codes.items() 
                  if code.startswith(('500'))}
    if error_codes:
        print("\nDetailed Error Codes:")
        print("-" * 30)
        for code, count in sorted(error_codes.items()):
            percentage = (count / total_requests) * 100
            print(f"{code}: {count} ({percentage:.1f}%)")
    
    print(f"\nTotal Requests: {total_requests}")

if __name__ == "__main__":
    main()