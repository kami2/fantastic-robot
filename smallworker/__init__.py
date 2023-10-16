from flask import Flask
import logging
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

# scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

import smallworker.routes
