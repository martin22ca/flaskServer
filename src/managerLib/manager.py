import os
from requests import get
from pathlib import Path
from datetime import datetime

# Models
from models.rollCallModel import rollCallModel
from models.attendenceModel import attendenceModel
from models.messageModel import messageModel


class Manager():
    def __init__(self) -> None:
        rollCallModel.setUp()
        pass

    def manage(self):
        rolls, completeClass = rollCallModel.getTodayRollCalls()
        for rollCall in rolls:
            if rollCall["close_time"] == None:
                idRollCa = rollCall["id_roll_call"]
                idClass = rollCall["id_student_class"]
                presentStudents = rollCall["present_students"]
                totalStudents = completeClass[idClass]["total_Students"]

                # percentage is number of present students /total studclass
                percentage = 0
                if totalStudents != 0:
                    percentage = (presentStudents/totalStudents)*100
                
                if percentage > 60:
                    self.closeRollCall(idRollCa, completeClass[idClass],idClass)
                    #self.closeDaemon()

    def closeRollCall(self, idRollcall, completeClass,idClass):
        print("closingRoll")
        attendenceModel.closeAttendence(idRollcall,idClass)

        if completeClass["id_employee"] == None:
            idEmployee = 0
        else:
            idEmployee = completeClass["id_employee"]

        schoolYear = str(completeClass["school_year"])
        schoolSection = completeClass["school_section"]
        rollCallModel.closeRollCall(idRollcall)
        now = datetime.now()
        title = "Cerradas asistencias curso " + \
            str(schoolYear) + "-" + str(schoolSection)
        txt = " Las asistencias cerraron a las " + str(now.hour) + ":" \
            + str(now.minute) + " exitosamente para el curso " + str(schoolYear) \
            + "-" + str(schoolSection)
        messageModel.createMsg(title, txt, None, idEmployee)

    def closeDaemon(self, ipClassroom):
        try:
            x = get('http://'+ipClassroom+':9022/close')
            if x.status_code == 200:
                print("now Closed")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    Man = Manager()

    Man.manage()
