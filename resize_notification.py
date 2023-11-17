#!/usr/bin/env python3

### Script to send FileSystem resizing notifications ###

import json
import requests
import subprocess
import time

service_name = 'resize.service'

def is_service_running(service_name): # Method to check if filesystem is being resized
    result = subprocess.run(['systemctl', 'is-active', service_name],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)
    return result.stdout.strip() == 'active'

def send_notification(): # Method to send visual notification to OSMC GUI
    url = "http://localhost:8080/jsonrpc"
    headers = {'content-type': 'application/json'}

    title = "***Resizing Filesystem***"
    message = "Please wait...\nSystem will reboot shortly!"
    display_time = 4990  # Display notification for just less than 5 seconds

    payload = {
        "jsonrpc": "2.0",
        "method": "GUI.ShowNotification",
        "params": {
            "title": title,
            "message": message,
            "displaytime": display_time,
        },
        "id": 1
    }

    requests.post(url, data=json.dumps(payload), headers=headers)

def main():
    check_count = 0 
    while check_count < 36:
        if is_service_running(service_name): # If service is running, continuously loop this statement
            check_count = 0
            send_notification()
        elif not is_service_running(service_name): # If service isn't running, check every 5 seconds up to 36 times
            check_count += 1
        time.sleep(5)

if __name__ == "__main__":
    main()
