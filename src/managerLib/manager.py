import os
from pathlib import Path
from datetime import datetime

class Manager():
    def __init__(self):
        attendenceDir = str(Path.home())+ '/fRecogAttendece/'

        if not os.path.exists(attendenceDir):
            os.makedirs(attendenceDir)

        self.todayDir = attendenceDir+str(datetime.now().date())+'/'


    @classmethod
    def checkRollCall():
        