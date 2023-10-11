from flask import Blueprint, jsonify, request


# Models
from models.classroomModel import classroomModel

main = Blueprint('classroomBlueprint', __name__)


@main.route('/', methods=['GET'])
def helloClassroom():
    try:
        req = request.json
        ipClassroom = req['ipClassroom']
        idClassroom = req['idClassroom']

        res = classroomModel.helloClassroom( ipClassroom, idClassroom)
        return jsonify({'message': 'Classroom hello', 'idClassroom': res})

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/register', methods=['GET'])
def registerClassroom():
    try:
        req = request.json
        classNumber = req['classNumber']
        className = req['className']
        ipClassroom = req['ipClassroom']

        res = classroomModel.registerClassroom(
            classNumber, className, ipClassroom)
        return jsonify({'message': 'Classroom Registered', 'idClassroom': res})

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
