from database.db import getConnection


class messageModel():

    @classmethod
    def createMsg(self, title, txt, info, idEmployee):
        try:
            connection = getConnection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO messages (title,message , info) VALUES (%s,%s,%s) RETURNING ID", (title, txt, info,))
                idMsg = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO users_messages (id_message,id_user) VALUES (%s,%s)", (
                        idMsg, idEmployee,)
                )
            connection.commit()
            connection.close()

            return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def msgAdmin(self, title, txt, info):
        try:
            connection = getConnection()

            with connection.cursor() as cursor:
                cursor.execute("select id from users u where id_role = 2")
                users = cursor.fetchall()
                for user in users:
                    idUser = user[0]
                    cursor.execute(
                        "INSERT INTO messages (title,message , info) VALUES (%s,%s,%s) RETURNING ID", (title, txt, info,))
                    idMsg = cursor.fetchone()[0]
                    cursor.execute(
                        "INSERT INTO users_messages (id_message,id_user) VALUES (%s,%s)", (idMsg, idUser,))
            connection.commit()
            connection.close()

            return None
        except Exception as ex:
            raise Exception(ex)
