#!/usr/bin/env python3
import random
from datetime import datetime, timedelta
import os

def generate_ip():
    """Generate a random IP address."""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_sample_logs(num_files=10, entries_per_file=100):
    """Generate sample HTTP log files with realistic data."""
    # Common URLs to simulate
    urls = [
        "/home", "/about", "/contact", "/api/v1/users", 
        "/images/logo.png", "/style.css", "/main.js",
        "/products", "/services", "/login", "/logout"
    ]
    
    # HTTP status codes with weighted probability
    status_codes = {
        200: 50,
        301: 5,
        302: 5,
        400: 5,
        401: 3,
        403: 2,
        404: 5,
        500: 23,
        503: 2
    }
    
    # User identifiers
    users = ["james", "mary", "john", "patricia", "robert", "jennifer", "michael", "linda"]
    
    # Generate files
    current_time = datetime.now()
    
    for file_num in range(1, num_files + 1):
        filename = f"Http-{file_num:02d}.log"
        
        with open(filename, 'w') as f:
            for _ in range(entries_per_file):
                # Generate random time within last 15 minutes
                time_offset = random.randint(0, 900)  # 15 minutes in seconds
                log_time = current_time - timedelta(seconds=time_offset)
                formatted_time = log_time.strftime('%d/%b/%Y:%H:%M:%S +0000')
                
                # Generate log entry
                ip = generate_ip()
                user = random.choice(users)
                url = random.choice(urls)
                status = random.choices(list(status_codes.keys()), 
                                     weights=list(status_codes.values()))[0]
                bytes_sent = random.randint(500, 5000)
                
                log_entry = f'{ip} user-identifier {user} [{formatted_time}] "GET {url} HTTP/1.0" {status} {bytes_sent}\n'
                f.write(log_entry)
    
    print(f"Generated {num_files} log files with {entries_per_file} entries each.")
    print("Files created:", ", ".join(f"Http-{i:02d}.log" for i in range(1, num_files + 1)))

if __name__ == "__main__":
    for f in [f for f in os.listdir('.') if f.startswith('Http-') and f.endswith('.log')]:
        os.remove(f)
    
    generate_sample_logs()