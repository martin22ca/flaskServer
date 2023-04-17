from database.db import getConnection


class classroomModel():

    @classmethod
    def helloClassroom(self, classNumber, className, ipClassroom, idClassroom=None):
        try:
            connection = getConnection()

            with connection.cursor() as cursor:

                if idClassroom == None:
                    cursor.execute(
                        "INSERT INTO classroom (class_number,class_name,ip_classroom,status) VALUES (%s,%s,%s,true) RETURNING ID", (classNumber, className, ipClassroom,))
                    idClassroom = cursor.fetchone()[0]
                    connection.commit()
                    connection.close()
                    return idClassroom
                else:
                    cursor.execute(
                        "update classroom set ip_classroom = %s, status = true where id = %s", (ipClassroom, idClassroom,))
                    connection.commit()
                    connection.close()

            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def closeClassroom(self, idRollCall):
        try:
            connection = getConnection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "select id_classroom ,count(*) * 100 / sum(count(*)) over() as percentage from attendences where  id_roll_call = %s group by id_classroom order by percentage desc", (idRollCall,))
                topClass = cursor.fetchone()
                connection.commit()
                connection.close()
            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)