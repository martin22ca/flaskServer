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
                    call = Attendence(row[0], row[1], row[2], row[3],row[4],row[5],row[6])
                    calls.append(Attendence.toJSON(call))

            connection.close()
            return calls
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def createAttendence(self,idClassroom,idStudent,timeArrival,present,late,imgEncoded):
        try:
            connection = getConnection()
            today = date.today()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id,id_classroom,roll_date FROM roll_call WHERE roll_date = %s and id_classroom = %s", (today,idClassroom))
                result = cursor.fetchone()

                if result == None: 
                    cursor.execute("INSERT INTO roll_call (id_classroom,roll_date) VALUES (%s,%s) RETURNING ID", (idClassroom,today,))
                    result = cursor.fetchone()

                cursor.execute("SELECT id_student,id_roll_call FROM attendences WHERE id_student = %s AND id_roll_call= %s", (idStudent,result[0],))
                alreadyIn = cursor.fetchone()

                if alreadyIn == None: 
                    cursor.execute("INSERT INTO attendences (id_student,id_roll_call,time_arrival,present,on_time,img_encoded) VALUES (%s,%s,%s,%s,%s,%s)", 
                                   (idStudent,result[0],timeArrival,present,late,imgEncoded))
                    connection.commit()
                    connection.close()
                    return 'New Attendence'
                else:
                    connection.close()
                    return 'Already marked'

        except Exception as ex:
            raise Exception(ex)