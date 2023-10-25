from database.db import getConnection
import datetime


class modulesModel():

    @classmethod
    def startup(self, ipClassroom, idClassroom=None):
        try:
            connection = getConnection()
            today = datetime.datetime.now()

            with connection.cursor() as cursor:
                print('as')
                cursor.execute(
                    "update ai_modules set ip_module = %s, online = true, online_date = %s where id = %s", (ipClassroom, today, idClassroom,))
                connection.commit()
                connection.close()

            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def register(self, moduleNumber, ipModule):
        try:
            connection = getConnection()
            today = datetime.datetime.now()

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ai_modules (module_number ,ip_module ,online_date ,online) VALUES (%s,%s,%s,true) RETURNING ID", (
                    moduleNumber, ipModule, today))
                idClassroom = cursor.fetchone()[0]
                connection.commit()
                connection.close()
            return idClassroom
        except Exception as ex:
            print(ex)
            raise Exception(ex)
