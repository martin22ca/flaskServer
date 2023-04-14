from database.db import getConnection
from .entities.messageEntity import Message


class messageModel():

    @classmethod
    def createMsg(self,title,txt,info,idEmployee):
        try:
            connection = getConnection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO messages (title,message , info) VALUES (%s,%s,%s) RETURNING ID", (title,txt,info,))
                idMsg = cursor.fetchone()[0]
                
                cursor.execute(
                    "INSERT INTO messages_x_employees (id_message,id_employee) VALUES (%s,%s)", (idMsg,idEmployee,)
                )
            connection.commit()
            connection.close()

            return None
        except Exception as ex:
            raise Exception(ex)