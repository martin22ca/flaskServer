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
                    "update files set model = %s, latest = latest + 1  where id = %s ", (Binary(model_pickle), 1,))
                cursor.execute(
                    "update files set model = %s, latest = latest + 1  where id = %s ", (Binary(names_pickle), 2,))
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

                cursor.execute("select * from ai_data r where r.id_status = 2")

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
                    "update ai_data set id_status = 3 where id_status = 2")

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
                    "select s.id,ad.encodings from students s inner join ai_data ad ON s.id_data = ad.id ")
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
                    "select model,latest from files f where id = 1 and latest > %s", (versionKnn,))
                if cursor.rowcount > 0:
                    knnModel, newVersionKnn = cursor.fetchone()
                cursor.execute(
                    "select model,latest from files f where id = 2 and latest > %s", (versionNames,))
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
                cursor.execute('select id_data from students s where id = %s',(idStud,))
                existAiData = cursor.fetchone()[0]
                if existAiData != None:
                    print(existAiData)
                    idAi = existAiData
                    cursor.execute('update ai_data set id_status = %s ,encodings = %s where id = %s', (2,token,idAi,))
                else:
                    cursor.execute('INSERT INTO ai_data (id_status,encodings) values (%s,%s) returning ID', (2,token,))
                    idAi = cursor.fetchone()[0]
                    cursor.execute('update students set id_data = %s where id = %s',(idAi,idStud,))

                connection.commit()
                cursor.close()
                connection.close()

            return None

        except Exception as ex:
            print(ex)
            raise Exception(ex)
