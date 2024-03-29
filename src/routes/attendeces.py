from base64 import b64decode
from flask import Blueprint, jsonify, request

# Models
from models.attendenceModel import attendenceModel

main = Blueprint('attendeceBlueprint', __name__)
    
@main.route('/newAttendence',methods=['POST'])    
def postNewAttendece():
    try:
        req = request.json
        imgStr = req['image']
        imgBytes = b64decode(imgStr)
        idClassroom = req['idClassroom']
        certainty = req['certainty']
        idStudent = req['studentId']
        timeArrival = req['timeOfEntry']
        msg = attendenceModel.createAttendence(idClassroom,idStudent,certainty,timeArrival,imgBytes)

        return jsonify({'message':msg},200)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


