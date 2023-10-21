from flask import render_template
from smallworker import app
import requests
import openai
from smallworker.utils.config import get_config
from smallworker import start_time


@app.route("/event_store", methods=['GET'])
def event_store():
    results = requests.get("https://chaotic.vercel.app/event_store").text
    return results


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


@app.route("/app_info")
def app_info():
    return {"Debug": app.debug, "Start Time": str(start_time)}


@app.route("/generate_prompt")
def generate_prompt():
    openai.api_key = get_config("OPEN_AI_APIKEY")
    completion = openai.ChatCompletion.create(
        model="davinci-002",
        messages=[
            {"role": "system",
             "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
    )
    return completion

