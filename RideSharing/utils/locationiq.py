import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.getenv("LOCATIONIQ_API_KEY")


def get_distance_and_time(lat1, lon1, lat2, lon2):
    BASE_URL = "https://us1.locationiq.com/v1/directions/driving/"
    url = f"{BASE_URL}{lon1},{lat1};{lon2},{lat2}"
    params = {"key": API_KEY, "overview": "false", "continue_straight": "false"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "routes" in data:
            hr = 0
            minute = 0
            sec = 0
            route = data["routes"][0]
            distance = route["distance"] / 1000
            duration = route["duration"]
            if duration > 360:
                hr = duration // 360
                duration %= 360
            if duration > 60:
                minute = duration // 60
                duration %= 60
            sec = duration
            time_taken = ""
            if hr > 0:
                time_taken += f"{hr} hr. "
                if sec > 0:
                    time_taken += f"{minute + 1} min."
                else:
                    time_taken += f"{minute} min."
            elif minute > 0:
                if sec > 0:
                    time_taken += f"{minute + 1} min."
                else:
                    time_taken += f"{minute} min."
            else:
                time_taken = "less than 1 min."

            return distance, time_taken

    return 0, 0


def get_address_from_coords(lat, lon):
    url = "https://us1.locationiq.com/v1/reverse"
    params = {"key": API_KEY, "lat": lat, "lon": lon, "format": "json"}

    try:
        response = requests.get(url, params=params)
        time.sleep(2)
        response.raise_for_status()
        data = response.json()
        return data.get("display_name")
    except requests.RequestException as e:
        print(f"Error fetching address: {e}")
        return None
