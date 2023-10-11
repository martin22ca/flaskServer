import os
import cv2
import pickle
from cryptography.fernet import Fernet
from decouple import config as envConfig
from utils.recogLib.faceRecog import encodeFace, loadRecognitionModel
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
        attendenceModel.cleanOldAtt()
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
        binaryKey = bytes(envConfig('TOKEN_FERNET'), 'utf-8')
        f = Fernet(binaryKey)
        print("Builing New Model")
        modelR = loadRecognitionModel()
        encrpytedData = recogModel.getEncodings()
        names = []
        encodings = []

        for idStud, encryptedToken in encrpytedData:
            studName = idStud
            decryptedData = f.decrypt(encryptedToken.tobytes())
            originalData = pickle.loads(decryptedData)
            for i in originalData:
                encodings.append(i)
                names.append(studName)

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
