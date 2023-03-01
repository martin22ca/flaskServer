from database.db import getConnection
from .entities.studentEntity import student


class studentModel():

    @classmethod
    def getStudents(self):
        try:
            connection = getConnection()
            students = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id,id_class FROM students")
                resultset = cursor.fetchall()

                for row in resultset:
                    stud = student(row[0], row[1])
                    students.append(student.toJSON(stud))

            connection.close()
            return students
        except Exception as ex:
            raise Exception(ex)
