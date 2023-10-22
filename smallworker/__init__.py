from flask import Flask
import logging
import os
from smallworker.helpers.route_helper import generate_image
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.debug = False
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | LEVEL: %(levelname)s | %(message)s',
                    handlers=[logging.StreamHandler()])


if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(generate_image, 'interval', jobstore='generator', hours=1)
    scheduler.start()


import smallworker.routes
