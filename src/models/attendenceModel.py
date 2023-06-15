from database.db import getConnection
from datetime import date,time
from .entities.attendenceEntity import Attendence


class attendenceModel():

    @classmethod
    def createAttendence(self, idClassroom, idStudent, certainty, timeArrival, imgBytes):
        try:
            connection = getConnection()
            today = date.today()

            with connection.cursor() as cursor:

                cursor.execute(
                    "select sc.status from students s inner join student_class sc ON s.id_student_class = sc.id  where s.id = %s", (idStudent,))
                late = cursor.fetchone()[0]
                late = not late 

                cursor.execute(
                    "SELECT id,id_student,att_date FROM attendances WHERE id_student = %s AND att_date = %s", (idStudent, today,))
                alreadyIn = cursor.fetchone()
                if alreadyIn == None:
                    cursor.execute("INSERT INTO attendances (id_student,time_arrival,present,late,certainty,img_encoded,id_classroom,att_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                   (idStudent, timeArrival, True, late, certainty, imgBytes, idClassroom, today,))
                    connection.commit()
                    connection.close()
                    return 'New Attendence'
                else:
                    attId = alreadyIn[0]
                    cursor.execute("UPDATE attendances SET time_arrival = %s,present =%s ,late =%s ,certainty = %s,img_encoded = %s where id = %s",
                                   (timeArrival, True, late, certainty, imgBytes, attId,))
                    connection.commit()

                    connection.close()
                    return 'Already marked'

        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def closeAttendance(self, idClass, today):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "update student_class set status = false, close_date = %s where id = %s", (today, idClass,))

                query = """insert into attendances (id_student,att_date,present)
                SELECT s.id,%s,false FROM students s 
                LEFT JOIN attendances a ON s.id = a.id_student and a.att_date = %s
                WHERE s.id_student_class  = %s and a.id is null ;
                """
                cursor.execute(query, (today, today, idClass,))
                connection.commit()
            connection.close()
            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)
        
    @classmethod
    def cleanOldAtt(self):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute("delete from attendances where att_date < Now() - interval '60 days'")
            connection.commit()
            connection.close()
            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)
