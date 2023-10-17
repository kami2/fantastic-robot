from flask import Flask
import logging
from smallworker.helpers.route_helper import add_event
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

# scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(add_event, 'interval', minutes=3)
scheduler.start()


@app.teardown_appcontext
def stop_scheduler():
    scheduler.shutdown()


import smallworker.routes
