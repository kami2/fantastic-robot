import requests
import logging
from smallworker.utils.config import get_config
import openai
import random
import time

BASE_URL = "https://cloud.leonardo.ai/api/rest/v1/"


def get_headers():
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {get_config('LEONARDO_APIKEY')}"
    }


def generate_prompt():
    logging.info("Generating prompt process")
    random_year = random.randint(1900, 2750)
    openai.api_key = get_config("OPEN_AI_APIKEY")
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": f"Take an event from {random_year} year and describe it as building in maximum of 60 words. "
                                              f"Describe colors, shape, add some details about it. Always start with 'Isometric view of'  "
                                              f"Good if you refer to country where event happened. You can add some details about surrounding area."
                                              f" Add words like: high quality, highly detailed"}
            ]
        )
        prompt = completion['choices'][0]['message']['content']
        return prompt

    except Exception as e:
        logging.info(f"ERROR : Prompt generator failed {e}")


def create_generation(prompt):
    logging.info("Creating generation process")

    try:
        url = f"{BASE_URL}generations"
        payload = {
            "height": 768,
            "prompt": prompt,
            "photoRealStrength": 0.55,
            "width": 512,
            "alchemy": True,
            "guidance_scale": 7,
            "nsfw": False,
            "num_images": 1,
            "presetStyle": "CREATIVE",
            "photoReal": True
        }
        response = requests.post(url, headers=get_headers(), json=payload)
        response_json = response.json()
        logging.info(response_json)
        return response_json['sdGenerationJob']['generationId']

    except Exception as e:
        logging.error(f"Failed to create generation: {e}")


def get_generation(generation_id):
    logging.info(f"Getting generation : {generation_id}")
    try:
        url = f"{BASE_URL}generations/{generation_id}"
        while True:
            response = requests.get(url, headers=get_headers())
            generation = response.json()['generations_by_pk']
            logging.info(f"Generation {generation_id} status {generation['status']}")
            if generation['status'] == "COMPLETE":
                return generation
            elif generation['status'] == "FAILED":
                return None
            else:
                logging.info("Wait 20 seconds")
                time.sleep(20)

    except Exception as e:
        logging.info(f"Failed to get generation : {generation_id} : {e}")


def get_model_list():
    logging.info("Getting list of available models")
    try:
        url = f"{BASE_URL}platformModels"
        response = requests.get(url, headers=get_headers())
        return response.json()
    except Exception as e:
        logging.info(f"Failed to get model list : {e}")


if __name__ == "__main__":
    generation_id_test = '1afd83a9-da61-44bf-b0ed-f9f5dda5e211'
    print(get_model_list())
