from datetime import date, datetime
from database.db import getConnection
from .entities.rollCallEntity import RollCall


class rollCallModel():

    @classmethod
    def getTodayRollCalls(self):
        try:
            connection = getConnection()
            calls = []
            totalStudents = {}
            today = date.today()

            with connection.cursor() as cursor:
                cursor.execute(
                    "select roll_call.id,id_student_class,close_time,count(id_student) from roll_call left join attendences on roll_call.id = attendences.id_roll_call where roll_date = %s group by  roll_call.id ", (today,))
                resultset = cursor.fetchall()

                for row in resultset:
                    call = {
                        "id_roll_call": row[0],
                        "id_student_class": row[1],
                        "close_time": row[2],
                        "present_students": row[3],
                    }
                    calls.append(call)

                cursor.execute(
                    "SELECT student_class.id,count(id_personal),id_employee,school_year,school_section FROM student_class left join students on student_class.id =students.id_student_class group by student_class.id order by student_class.id asc")
                resultset = cursor.fetchall()

                for row in resultset:
                    totalStudents[row[0]] = {
                        "total_Students": row[1],
                        "id_employee": row[2],
                        "school_year": row[3],
                        "school_section": row[4],
                    }

            connection.close()
            return calls, totalStudents
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def createRollCall(self, roll):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO roll_call (id_classroom,roll_date,ip_classroom) VALUES (%s,%s,%s) RETURNING ID", (
                    roll.idClassroom, roll.rollDate, roll.ipClassroom))
                result = cursor.fetchone()
                connection.commit()
                connection.close()
                return result[0]

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def setUp(self):
        try:
            today = date.today()
            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM student_class where id not in (SELECT id_student_class FROM  roll_call where roll_date =  %s)", (today,))
                missingRol = cursor.fetchall()

                for missingClass in missingRol:
                    idClass = missingClass[0]
                    cursor.execute(
                        "insert into roll_call (id_student_class,roll_date) values (%s,%s)", (idClass, today,))
                connection.commit()

            connection.close()
            return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def closeRollCall(self, idRoll):
        try:
            now = datetime.now()
            closeTime = str(now.hour) + ":" + str(now.minute)
            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE roll_call SET close_time = %s where roll_call.id  = %s ", (closeTime, idRoll,))
                connection.commit()
                connection.close()
                return None

        except Exception as ex:
            raise Exception(ex)
