from base64 import b64decode
from flask import Blueprint, jsonify, request

# Entities
from models.entities.attendenceEntity import Attendence

# Models
from models.attendenceModel import attendenceModel

main = Blueprint('attendeceBlueprint', __name__)

@main.route('/',methods=['GET'])
def getAttendences():
    try:
        students = attendenceModel.getAttendences()
        return jsonify(students)
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/newAttendence',methods=['POST'])    
def postNewAttendece():
    try:
        req = request.json
        imgStr = req['image']
        imgBytes = b64decode(imgStr)
        classroomId = req['classroomId']
        idStudent = req['studentId']
        timeArrival = req['timeOfEntry']
        present = True
        late = req['onTime']
        msg = attendenceModel.createAttendence(classroomId,idStudent,timeArrival,present,late,imgBytes)

        return jsonify({'message':msg},200)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


