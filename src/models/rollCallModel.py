from database.db import getConnection
from .entities.rollCallEntity import rollCall


class rollCallModel():

    @classmethod
    def getRollCalls(self):
        try:
            connection = getConnection()
            calls = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id,id_class,id_classroom,closing_time FROM roll_call ")
                resultset = cursor.fetchall()

                for row in resultset:
                    call = rollCall(row[0], row[1], row[2], row[3])
                    calls.append(rollCall.toJSON(call))

            connection.close()
            return calls
        except Exception as ex:
            raise Exception(ex)
