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
from models.gradeModel import gradeModel
from models.recogModel import recogModel
from models.attendenceModel import attendenceModel
from models.messageModel import messageModel


class Manager():
    def __init__(self) -> None:
        self.today = date.today()
        if (recogModel.checkForBuild()):
            self.buildModel()
        self.startDay()
        pass

    def startDay(self):
        gradeModel.openGrades(self.today)

    def closeAttendance(self, studClass, today):
        print("closeAttendance")

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
