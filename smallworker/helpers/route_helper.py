import json
import requests
import logging
from smallworker.utils.config import get_config
from smallworker.helpers.image_generator import generate_prompt, create_generation, get_generation


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


def image_event():
    logging.info("Image event start")
    status = "Failed"
    try:
        prompt = generate_prompt()
        generate_id = create_generation(prompt)
        generations = get_generation(generate_id)
        if generations:
            logging.info(f"Generation {generate_id} is ready to process")
            for image in generations['generated_images']:
                payload = {
                    "prompt": generations['prompt'],
                    "file_url": image['url'],
                    "created_at": generations['createdAt']
                }
                response = requests.post("https://chaotic.vercel.app/process_generated_image", json=payload, headers=get_headers())
                if response.status_code != 200:
                    continue
                status = "Success"
    except Exception as e:
        logging.info(f"Image event failed: {e}")

    return add_event(f"Generated image send from worker : {status}")


def log_start_app_time(start_time):
    logging.info(f"App started at {start_time}")
    return add_event(f"Deployed at {str(start_time)}")


def keep_app_alive():
    logging.info("Wake up worker!")


if __name__ == "__main__":
    image_event()
