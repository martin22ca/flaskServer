from utils.DateFormat import DateFormat

class RollCall():

    def __init__(self, id, idClassroom,rollDate, idStudentClass=None, closeTime=None) -> None:
        self.id = id
        self.idStudentClass = idStudentClass
        self.idClassroom = idClassroom
        self.idClassroom = idClassroom
        self.rollDate = rollDate
        self.closeTime = closeTime

    def toJSON(self):
        return {
            "id": self.id,
            "idClass": self.idStudentClass,
            "idClassroom": self.idClassroom,
            "closingTime": self.closeTime,
            "rollDate": self.rollDate
        }
