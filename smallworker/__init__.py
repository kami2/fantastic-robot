from flask import Flask
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

import smallworker.routes
