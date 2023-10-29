from flask import Flask
import logging
import os
from smallworker.helpers.route_helper import image_event
from smallworker.helpers.scheduler_helper import Scheduler

os.environ['FLASK_ENV'] = 'production'

app = Flask(__name__)
app.debug = False
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | PROCESS: %(processName)s | LEVEL: %(levelname)s | %(message)s ',
                    handlers=[logging.StreamHandler()])


scheduler = Scheduler().scheduler
scheduler.add_job(image_event, 'interval', hours=12)
scheduler.start()


import smallworker.routes
