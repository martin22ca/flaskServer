import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from utils.managerLib.manager import Manager

class BackgroundManager():

    def __init__(self) -> None:
        print("starting background...")
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.interval_task,'interval', seconds=45)
        self.scheduler.start()
        self.manager = Manager()
        pass

    def interval_task(self):
        print("Running interval task...")
        

