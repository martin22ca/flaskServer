import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from utils.managerLib.manager import Manager

class BackgroundManager():

    def __init__(self) -> None:
        print("starting background...")
        self.scheduler = BackgroundScheduler()
        #self.scheduler.add_job(daily_task, 'cron', day_of_week='mon-fri', hour=8)
        self.scheduler.add_job(self.interval_task,'interval', seconds=45)
        self.scheduler.start()
        self.manager = Manager()
        pass

    def interval_task(self):
        print("Running interval task...")
        self.manager.manage()
        
    # Define your task functions
    def daily_task(self):
        print("Running daily task...")
        self.manager.manage()
        # Calculate the start time for the interval task based on the current time
        now = datetime.now()
        start_time = now + datetime.timedelta(minutes=40 - now.minute % 40, seconds=-now.second,
                                              microseconds=-now.microsecond)
        # Schedule the interval task to start at the calculated time
        self.scheduler.add_job(self.interval_task, 'interval', minutes=40,
                          start_date=start_time)
