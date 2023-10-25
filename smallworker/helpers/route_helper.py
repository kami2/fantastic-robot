import json
import requests
import logging
from smallworker.utils.config import get_config
import openai
import random


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


def generate_prompt():
    random_year = random.randint(1400, 2020)
    openai.api_key = get_config("OPEN_AI_APIKEY")
    prompt = None
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": f"Take an event from {random_year} year and describe it as building in maximum of 100 words. "
                                              f"Describe colors, shape, add some details about it. Always start with 'Isometric view of'  "
                                              f"Good if you refer to country where event happened. You can add some details about surrounding area."}
            ]
        )
        prompt = completion['choices'][0]['message']['content']

    except Exception as e:
        logging.info(f"ERROR : Prompt generator failed {e}")

    return prompt


if __name__ == "__main__":
    generate_prompt()
