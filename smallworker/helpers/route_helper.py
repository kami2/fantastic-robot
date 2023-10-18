import json
import requests
from smallworker.utils.config import get_config


def get_headers():
    return {
        "Authorization": f"Bearer {get_config('CRON_SECRET')}",
        "Content-Type": "application/json"
    }


def add_event():
    event_data = {
        "Event": "Added remotely from small worker, interval : 5H",
        "Scheduled": True
    }
    response = requests.post('https://chaotic.vercel.app/add_event', headers=get_headers(), data=json.dumps(event_data))
    return response


def generate_image():
    event_data = {
        "Event": "Generated image from worker, interval : 10H",
        "Scheduled": True
    }
    response = requests.post('https://chaotic.vercel.app/add_event', headers=get_headers(), data=json.dumps(event_data))
    return response
