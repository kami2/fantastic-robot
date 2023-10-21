import datetime
from flask import jsonify
from flask import render_template
from smallworker import app
import requests
import openai
from smallworker.utils.config import get_config


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
    start_time_str = get_config("APP_START_TIME")
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    start_time = datetime.datetime.strptime(start_time_str, date_format)
    app_data = {
        "Debug": app.debug,
        "Start Time": str(start_time),
        "Uptime": f"{round((datetime.datetime.utcnow() - start_time).total_seconds() / 3600, 2)}H"
    }
    return app_data


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
