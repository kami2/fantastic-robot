from flask import Flask
import logging
import os
from smallworker.helpers.route_helper import generate_image
from apscheduler.schedulers.background import BackgroundScheduler

os.environ['FLASK_ENV'] = 'production'

app = Flask(__name__)
app.debug = False
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | PROCESS: %(processName)s | LEVEL: %(levelname)s | %(message)s ',
                    handlers=[logging.StreamHandler()])


scheduler = BackgroundScheduler()
scheduler.add_job(generate_image, 'interval', args=["10 minutes"], minutes=10)
scheduler.start()


import smallworker.routes
