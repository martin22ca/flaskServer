import cv2
import base64
import pickle
import numpy as np
from pathlib import Path
from cryptography.fernet import Fernet
from decouple import config as envConfig
from utils.recogLib.faceRecog import encodeFace, loadRecognitionModel
from database.db import getConnection
from psycopg2 import Binary


class recogModel():

    @classmethod
    def uploadFiles(self, model_pickle, names_pickle):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:

                # Insert the pickled objects into the database
                cursor.execute(
                    "update models set model  = %s, model_version = model_version + 1  where id = 1", (Binary(model_pickle),))
                cursor.execute(
                    "update models set model  = %s, model_version = model_version + 1  where id = 2", (Binary(names_pickle),))
                connection.commit()

                cursor.close()
                connection.close()

                if cursor.rowcount > 0:
                    return True
                else:
                    return False

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def checkForBuild(self):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:

                cursor.execute("select id from recognition r where id_state = 2")

                connection.commit()
                connection.close()
                if cursor.rowcount > 0:
                    return True
                else:
                    return False

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def updateStatus(self):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:

                cursor.execute(
                    "update recognition set id_state = 1 where id_state = 2")

                connection.commit()

                cursor.close()
                connection.close()
                return None

        except Exception as ex:
            print(ex)
            raise Exception(ex)
        
    @classmethod
    def getEncodings(self):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:

                cursor.execute(
                    "select id,encodings from recognition r where encodings is not null")
                resultset = cursor.fetchall()

                cursor.close()
                connection.close()
                return resultset

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def getModels(self, versionKnn, versionNames):
        try:
            connection = getConnection()
            knnModel = None
            names = None
            newVersionKnn = versionKnn
            newVersionNames = versionNames
            print(versionKnn, versionNames)
            with connection.cursor() as cursor:
                # Insert the pickled objects into the database
                cursor.execute(
                    "select model ,model_version from models m where id = 1 and model_version > %s", (versionKnn,))
                if cursor.rowcount > 0:
                    knnModel, newVersionKnn = cursor.fetchone()
                cursor.execute(
                    "select model ,model_version from models m where id = 2 and model_version > %s", (versionNames,))
                if cursor.rowcount > 0:
                    names, newVersionNames = cursor.fetchone()

            connection.commit()
            connection.close()

            return knnModel, newVersionKnn, names, newVersionNames

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def registerEncodings(self, images, idStud):
        try:
            binaryKey =  bytes(envConfig('TOKEN_FERNET'), 'utf-8') 
            f = Fernet(binaryKey)
            connection = getConnection()
            modelR = loadRecognitionModel()
            encodings = []

            for pic in images:
                image_data = pic.split(',')[1]
                image_binary = base64.b64decode(image_data)
                image_np = np.frombuffer(image_binary, dtype=np.uint8)
                img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (160, 160))
                enco = encodeFace(img, modelR)
                encodings.append(enco)

            binary_data = pickle.dumps(encodings)
            token = f.encrypt(data=binary_data)
            with connection.cursor() as cursor:
                cursor.execute('select id_recog from students s inner join personal_data pd on s.id_personal = pd.id where s.id = %s',(idStud,))
                idAi = cursor.fetchone()[0]
                cursor.execute('update recognition set id_state = %s ,encodings = %s where id = %s', (2,token,idAi,))

                connection.commit()
                cursor.close()
                connection.close()

            return None

        except Exception as ex:
            print(ex)
            raise Exception(ex)
