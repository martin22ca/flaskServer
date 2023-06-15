from database.db import getConnection
from datetime import date


class classroomModel():

    @classmethod
    def helloClassroom(self, classNumber, className, ipClassroom, idClassroom=None):
        try:
            connection = getConnection()
            today = date.today()

            with connection.cursor() as cursor:
                if idClassroom == None:
                    cursor.execute(
                        "INSERT INTO classrooms (class_number,class_name,ip_classroom,status) VALUES (%s,%s,%s,%s) RETURNING ID", (classNumber, className, ipClassroom, today,))
                    idClassroom = cursor.fetchone()[0]
                    connection.commit()
                    connection.close()
                    return idClassroom
                else:
                    cursor.execute(
                        "update classrooms set ip_classroom = %s, status = %s where id = %s", (ipClassroom, today, idClassroom,))
                    connection.commit()
                    connection.close()

            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)
