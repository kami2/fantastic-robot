import requests
import logging
from smallworker.utils.config import get_config
import openai
import random

BASE_URL = "https://cloud.leonardo.ai/api/rest/v1/"


def get_headers():
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {get_config('LEONARDO_APIKEY')}"
    }


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


def generate_image():
    logging.info("Generating image process")

    url = f"{BASE_URL}generations"
    payload = {

    }
    # TODO Need to add basic params, prompt from generate_prompt() and handle errors
    response = requests.post(url, headers=get_headers(), data=payload)

    return response


def get_generation(generation_id):
    url = f"{BASE_URL}generations/{generation_id}"
    response = requests.get(url, headers=get_headers())
    # TODO Need to add extra steps
    return response


