import sys
import os
import datetime

sys.path.append(os.getcwd())

from smallworker.helpers.route_helper import log_start_app_time
from smallworker import app as application
start_time = datetime.datetime.utcnow()
os.environ["APP_START_TIME"] = str(start_time)
log_start_app_time(start_time)
