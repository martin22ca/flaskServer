from database.db import getConnection
from psycopg2 import Binary

class recogModel():

    @classmethod
    def checkForBuild(self):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:

                cursor.execute("select * from recog r where r.status = 1")

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
    def updateStatus(self):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:

                # Insert the pickled objects into the database
                cursor.execute("update recog set status = 2 where status = 1")

                connection.commit()

                cursor.close()
                connection.close()
                return None

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

                cursor.close()
                connection.close()
                print(knnModel, names)

                return knnModel, newVersionKnn, names, newVersionNames

        except Exception as ex:
            print(ex)
            raise Exception(ex)
