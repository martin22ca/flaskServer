from utils.DateFormat import DateFormat


class student():

    def __init__(self,id,idClass) -> None:
        self.aiKey = id
        self.idClass = idClass

    def toJSON(self):
        return {
            self.aiKey: self.idClass,
        }
    