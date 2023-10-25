from database.db import getConnection


class gradeModel():

    @classmethod
    def openGrades(self, today):
        try:
            connection = getConnection()
            with connection.cursor() as cursor:

                cursor.execute(
                    "select id from grade g where id not in(select id_grade from roll_call rc where att_date = %s)", (today,))
                grades = cursor.fetchall()

                for grade in grades:
                    cursor.execute(
                        "insert into roll_call (id_grade,att_date) values (%s,%s) RETURNING ID", (grade[0], str(today),))
                    roll = cursor.fetchone()
                    query = """ insert into attendances (id_recog,id_roll)  
                    select id_recog ,%s from students s inner join personal_data pd on s.id_personal = pd.id  
                    where s.id_grade = %s"""
                    cursor.execute(query, (roll[0], grade[0],))

                connection.commit()
                connection.close()

            return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def checkStatus(self, today):
        try:
            connection = getConnection()

            with connection.cursor() as cursor:

                query = """SELECT sc.id as sc,sc.status,sc.school_year,sc.school_section,sc.id_employee ,count(a.id) as present,count(s.id) as total 
                FROM student_class sc inner join students s on s.id_student_class = sc.id 
                left join attendances a on a.id_student = s.id and a.att_date  = %s 
                group by sc.id ORDER BY school_year desc"""

                cursor.execute(query, (today, ))
                resultset = cursor.fetchall()
                connection.commit()
                connection.close()
            return resultset
        except Exception as ex:
            print(ex)
            raise Exception(ex)
