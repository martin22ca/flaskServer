from database.db import getConnection
from datetime import date
from .entities.attendenceEntity import Attendence


class attendenceModel():

    @classmethod
    def getAttendences(self):
        try:
            connection = getConnection()
            calls = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id,id_student,id_roll_call,time_arrival,present,late,img_encoded FROM attendences")
                resultset = cursor.fetchall()

                for row in resultset:
                    call = Attendence(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    calls.append(Attendence.toJSON(call))

            connection.close()
            return calls
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getAttendencesFromRoll(self, idRoll):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "select count(attendences.id) from attendences where id_roll_call = %s group by id_roll_call ", (idRoll, ))
                resultset = cursor.fetchone()

                connection.close()

                return resultset
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def createAttendence(self, idClassroom, idStudent, certainty, timeArrival, present, imgBytes):
        try:
            connection = getConnection()
            today = date.today()
            late = False
            with connection.cursor() as cursor:

                cursor.execute(
                    "select id_student_class from students where id = %s", (idStudent,))
                idClass = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT id,roll_date,close_time,roll_call FROM roll_call WHERE roll_date = %s  and id_student_class = %s", (today, idClass))
                result = cursor.fetchone()

                if result == None:
                    cursor.execute("INSERT INTO roll_call (id_student_class,roll_date) VALUES (%s,%s) RETURNING ID", (
                        idClass, today,))
                    result = cursor.fetchone()
                    idRollCall = result[0]

                    cursor.execute("INSERT INTO attendences (id_student,id_roll_call,time_arrival,present,late,certainty,img_encoded,id_classroom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                   (idStudent, idRollCall, timeArrival, present, late, certainty, imgBytes, idClassroom,))
                    connection.commit()
                    connection.close()
                    return 'New Attendence'

                else:
                    idRollCall = result[0]
                    if result[3] != None:
                        print("Late")
                        late == True

                cursor.execute(
                    "SELECT id_student,id_roll_call FROM attendences WHERE id_student = %s AND id_roll_call= %s", (idStudent, idRollCall,))
                alreadyIn = cursor.fetchone()

                if alreadyIn == None:
                    cursor.execute("INSERT INTO attendences (id_student,id_roll_call,time_arrival,present,late,certainty,img_encoded,id_classroom) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                   (idStudent, idRollCall, timeArrival, present, late, certainty, imgBytes, idClassroom,))
                    connection.commit()
                    connection.close()
                    return 'New Attendence'
                else:
                    connection.close()
                    return 'Already marked'

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def closeAttendence(self, idRoll, idClass):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute("insert into attendences (id_student,id_roll_call) select s.id, %s from students s where s.id_student_class = %s and s.id not in (select attendences.id_student from attendences where attendences.id_roll_call = %s )", (idRoll, idClass, idRoll))
                connection.commit()
            connection.close()
            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)
