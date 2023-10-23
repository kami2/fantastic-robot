from apscheduler.schedulers.background import BackgroundScheduler
import logging


class Scheduler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logging.info("Initialize Scheduler")
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance.scheduler = BackgroundScheduler()
        return cls._instance
