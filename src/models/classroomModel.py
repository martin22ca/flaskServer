from database.db import getConnection


class classroomModel():

    @classmethod
    def helloClassroom(self, classNumber, className, ipClassroom, idClassroom=None):
        try:
            connection = getConnection()

            with connection.cursor() as cursor:

                if idClassroom == None:
                    cursor.execute(
                        "INSERT INTO classroom (class_number,class_name,ip_classroom) VALUES (%s,%s,%s) RETURNING ID", (classNumber, className, ipClassroom,))
                    idClassroom = cursor.fetchone()[0]
                    connection.commit()
                    connection.close()
                    return idClassroom
                else:
                    cursor.execute(
                        "update classroom set ip_classroom = %s where id = %s", (ipClassroom, idClassroom,))
                    connection.commit()
                    connection.close()

            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)
