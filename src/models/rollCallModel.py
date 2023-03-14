from database.db import getConnection
from .entities.rollCallEntity import RollCall

class rollCallModel():

    @classmethod
    def getRollCalls(self):
        try:
            connection = getConnection()
            calls = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id,id_student_class,roll_date,id_classroom,close_time FROM roll_call ")
                resultset = cursor.fetchall()

                for row in resultset:
                    call = RollCall(row[0], row[1], row[2], row[3],row[4])
                    calls.append(RollCall.toJSON(call))

            connection.close()
            return calls
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def createRollCall(self,roll):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO roll_call (id_classroom,roll_date) VALUES (%s,%s) RETURNING ID", (roll.idClassroom,roll.rollDate,))
                result = cursor.fetchone()
                connection.commit()
                connection.close()
                return result[0]

        except Exception as ex:
            raise Exception(ex)
