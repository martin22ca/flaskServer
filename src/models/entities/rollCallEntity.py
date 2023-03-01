from utils.DateFormat import DateFormat


class rollCall():

    def __init__(self, id, idClass, idClassroom, closingTime, edited=False, idEmployee=None) -> None:
        self.id = id
        self.idClass = idClass
        self.idClassroom = idClassroom
        self.closingTime = closingTime
        self.edited = edited,
        self.idEmployee = idEmployee

    def toJSON(self):
        return {
            "id": self.id,
            "idClass": self.idClass,
            "idClassroom": self.idClassroom,
            "closingTime": self.closingTime,
        }
