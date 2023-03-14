from utils.DateFormat import DateFormat


class Student():

    def __init__(self,id,id_student_class) -> None:
        self.id = id
        self.id_student_class = id_student_class

    def toJSON(self):
        return {
            'id': self.id,
            'id_student_class': self.id_student_class
        }
    