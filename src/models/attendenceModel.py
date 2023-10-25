from database.db import getConnection
from datetime import date


class attendenceModel():

    @classmethod
    def createAttendence(self, idModule, idRecog, certainty, arrival, imgBytes):
        try:
            connection = getConnection()
            today = date.today()

            with connection.cursor() as cursor:
                query = """select a.id from attendances a inner join roll_call rc ON a.id_roll = rc.id  
                inner join grade g on rc.id_grade = g.id  inner join students s on s.id_grade = g.id  
                inner join personal_data pd on s.id_personal =pd.id  
                where rc.att_date = %s and pd.id_recog = %s """

                cursor.execute(query, (str(today), idRecog))
                alreadyIn = cursor.fetchone()
                attId = alreadyIn[0]
                cursor.execute("UPDATE attendances SET arrival = %s,present = true ,certainty = %s,img_encoded = %s,id_module = %s where id = %s",
                               (arrival, certainty, imgBytes, idModule, attId,))
                connection.commit()
                connection.close()
                return 'Already marked'

        except Exception as ex:
            print(ex)
            raise Exception(ex)
