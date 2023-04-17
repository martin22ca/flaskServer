from database.db import getConnection

class classModel():

    @classmethod
    def openClasses(self,today):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:

                cursor.execute("update student_class set status = true where close_date < %s", (today,))
                connection.commit()
                connection.close()

            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def checkStatus(self,today):
        try:
            connection = getConnection()
    
            with connection.cursor() as cursor:

                query = """SELECT sc.id as sc,sc.status,sc.school_year,sc.school_section,sc.id_employee ,count(a.id) as present,count(s.id) as total 
                FROM student_class sc inner join students s on s.id_student_class = sc.id 
                left join attendences a on a.id_student = s.id and a.att_date  = %s 
                group by sc.id ORDER BY school_year desc"""

                cursor.execute(query, (today, ))
                resultset = cursor.fetchall()
                connection.commit()
                connection.close()
            return resultset
        except Exception as ex:
            print(ex)
            raise Exception(ex)
