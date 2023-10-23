import json
import requests
import logging
from smallworker.utils.config import get_config


def get_headers():
    return {
        "Authorization": f"Bearer {get_config('CRON_SECRET')}",
        "Content-Type": "application/json"
    }


def add_event(event_data):
    logging.info(f"DATA: {event_data}")
    event_payload = {
        "Event": event_data
    }
    response = requests.post('https://chaotic.vercel.app/add_event', headers=get_headers(), data=json.dumps(event_payload))
    return response


def generate_image(interval: str):
    return add_event(f"Generated image from worker, interval : {interval}")


def log_start_app_time(start_time):
    logging.info(f"App started at {start_time}")
    return add_event(f"Deployed at {str(start_time)}")
