import os
import cv2
import pickle
from recogLib.faceRecog import encodeFace, loadRecognitionModel
from requests import get
from pathlib import Path
from datetime import datetime, date
from sklearn.neighbors import KNeighborsClassifier

# Models
from models.classModel import classModel
from models.recogModel import recogModel
from models.attendenceModel import attendenceModel
from models.messageModel import messageModel


class Manager():
    def __init__(self) -> None:
        self.today = date.today()
        if (recogModel.checkForBuild()):
            self.buildModel()
        classModel.openClasses(self.today)
        pass

    def manage(self):
        studClasses = classModel.checkStatus(self.today)
        for studClass in studClasses:
            if studClass[1]:
                presentStudents = studClass[5]
                totalStudents = studClass[6]

                # percentage is number of present students /total studclass
                percentage = 0
                if totalStudents > 0:
                    percentage = (presentStudents/totalStudents)*100

                if percentage >= 60:
                    self.closeAttendance(studClass, self.today)
                    # self.closeDaemon()

    def closeAttendance(self, studClass, today):
        print("closeAttendance")
        idClass = studClass[0]
        schoolYear = str(studClass[2])
        schoolSection = studClass[3]

        if studClass[4] == None:
            attendenceModel.closeAttendance(idClass, today)
            return None

        idEmployee = studClass[4]
        now = datetime.now()
        title = "Cerradas asistencias curso " + \
            str(schoolYear) + "-" + str(schoolSection)
        txt = " Las asistencias cerraron a las " + str(now.hour) + ":" \
            + str(now.minute) + " exitosamente para el curso " + str(schoolYear) \
            + "-" + str(schoolSection)

        attendenceModel.closeAttendance(idClass, today)
        messageModel.createMsg(title, txt, None, idEmployee)
        return None

    def closeDaemon(self, ipClassroom):
        try:
            x = get('http://'+ipClassroom+':9022/close')
            if x.status_code == 200:
                print("now Closed")
        except Exception as e:
            print(e)

    def buildModel(self):
        print("Builing New Model")
        modelR = loadRecognitionModel()
        encodings = []
        names = []
        home = str(Path.home()) + '/students/'

        for student in os.listdir(home):
            idStud = int(student)
            studPath = home + student + '/'

            for pic in os.listdir(studPath):
                img = cv2.imread(studPath+pic)
                img = cv2.resize(img, (160, 160))
                enco = encodeFace(img, modelR)
                encodings.append(enco)
                names.append(student)

        model = KNeighborsClassifier(
            n_neighbors=6, weights='distance', algorithm='ball_tree')
        model.fit(encodings, names)
        model_pickle = pickle.dumps(model)
        names_pickle = pickle.dumps(names)

        recogModel.uploadFiles(model_pickle, names_pickle)
        recogModel.updateStatus()
        return None


if __name__ == "__main__":
    Man = Manager()

    Man.manage()
