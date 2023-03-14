from database.db import getConnection
from .entities.studentEntity import Student


class studentModel():

    @classmethod
    def getStudents(self):
        try:
            connection = getConnection()
            students = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id,id_student_class FROM students")
                resultset = cursor.fetchall()

                for row in resultset:
                    stud = Student(row[0], row[1])
                    students.append(Student.toJSON(stud))

            connection.close()
            return students
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def getClassFromId(self,id):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id,id_student_class FROM students WHERE id = %s", (id,))
                result = cursor.fetchone()

                connection.close()
                if result != None:
                    return result[1]
                else:
                    return None
        except Exception as ex:
            raise Exception(ex)
