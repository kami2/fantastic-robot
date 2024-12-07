import datetime
from flask import render_template, request, jsonify
from smallworker import app
from smallworker.utils.config import get_config
import logging


@app.route("/")
def main():
    start_time_str = get_config("APP_START_TIME")
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    start_time = datetime.datetime.strptime(start_time_str, date_format)
    enter_text = f"Start time {str(start_time)}, Loaded {round((datetime.datetime.utcnow() - start_time).total_seconds() / 3600, 2)}H ago"
    return render_template("index.html", enter_text=enter_text)


@app.route("/wake_up", methods=['GET'])
def wake_up():
    logging.info("Wake up worker!")
    return "I am awake!"


@app.route("/test_refresh", methods=['GET'])
def refresh_headers():
    headers = dict(request.headers)
    logging.info(headers)
    status_code = request.headers.get('code')

    if status_code == '200':
        return jsonify(message="Success"), 200
    elif status_code == '500':
        return jsonify(message="Failed"), 500
    else:
        return jsonify(message="Invalid status code"), 400
