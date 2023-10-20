from flask import Flask
import logging
from smallworker.helpers.route_helper import add_event, generate_image
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.debug = False
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

# scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(generate_image, 'interval', hours=1)
scheduler.start()


import smallworker.routes
