class Attendence():

    def __init__(self, id, idStudent, idRollCall, timeArrival, present, late, imgEncoded) -> None:
        self.id = id
        self.idStudent = idStudent
        self.idRollCall = idRollCall
        self.timeArrival = timeArrival
        self.present = present
        self.late = late
        self.imgEncoded = imgEncoded

    def toJSON(self):
        return {
            "id": self.id,
            "idStudent": self.idStudent,
            "idRollCall": self.idRollCall,
            "timeArrival": self.timeArrival,
            "present": self.present,
            "late": self.late,
            "imgEncoded": self.imgEncoded,
        }