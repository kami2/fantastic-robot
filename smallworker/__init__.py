from flask import Flask
import logging
from smallworker.helpers.route_helper import add_event, generate_image, log_start_app_time
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

app = Flask(__name__)
app.debug = False
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])
start_time = datetime.datetime.now()
log_start_app_time(start_time)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(generate_image, 'interval', hours=1)
scheduler.start()


import smallworker.routes
