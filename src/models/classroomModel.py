from database.db import getConnection
import datetime


class classroomModel():

    @classmethod
    def helloClassroom(self, ipClassroom, idClassroom=None):
        try:
            connection = getConnection()
            today = datetime.datetime.now()

            with connection.cursor() as cursor:
                print('as')
                cursor.execute(
                    "update classrooms set ip_classroom = %s, status = true,last_online = %s where id = %s", (ipClassroom, today, idClassroom,))
                connection.commit()
                connection.close()

            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def registerClassroom(self, classNumber, className, ipClassroom):
        try:
            connection = getConnection()
            today = datetime.datetime.now()

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO classrooms (class_number,class_name,ip_classroom,last_online,status) VALUES (%s,%s,%s,%s,true) RETURNING ID", (
                    classNumber, className, ipClassroom, today))
                idClassroom = cursor.fetchone()[0]
                connection.commit()
                connection.close()
            return idClassroom
        except Exception as ex:
            print(ex)
            raise Exception(ex)
