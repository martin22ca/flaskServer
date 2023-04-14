from utils.DateFormat import DateFormat

class RollCall():

    def __init__(self, id, idClassroom,rollDate,ipClassroom, idStudentClass=None, closeTime=None) -> None:
        self.id = id
        self.idStudentClass = idStudentClass
        self.idClassroom = idClassroom
        self.idClassroom = idClassroom
        self.rollDate = rollDate
        self.closeTime = closeTime
        self.ipClassroom = ipClassroom

    def toJSON(self):
        return {
            "id": self.id,
            "idClass": self.idStudentClass,
            "idClassroom": self.idClassroom,
            "closeTime": self.closeTime,
            "rollDate": self.rollDate,
            "ipClassroom":self.ipClassroom
        }
