from flask import render_template
from smallworker import app
import requests


@app.route("/event_store", methods=['GET'])
def event_store():
    results = requests.get("https://chaotic.vercel.app/event_store").text
    return results


@app.route("/")
def main():
    enter_text = "Do something..."
    results = render_template("index.html", enter_text=enter_text)
    return results


@app.route("/debug_state")
def debug_state():
    return {"Debug": app.debug}