from flask import Flask
import logging
from smallworker.helpers.route_helper import add_event
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

# scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(add_event, 'interval', hours=10)
scheduler.start()

import smallworker.routes
