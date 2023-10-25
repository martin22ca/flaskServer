from flask import Blueprint, jsonify, request


# Models
from models.modulesModel import modulesModel

main = Blueprint('classroomBlueprint', __name__)


@main.route('/', methods=['GET'])
def hello():
    try:
        req = request.json
        ipClassroom = req['ipClassroom']
        idClassroom = req['idClassroom']

        res = modulesModel.startup(ipClassroom, idClassroom)
        return jsonify({'message': 'Classroom hello', 'idClassroom': res})

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/newModule', methods=['GET'])
def register():
    try:
        req = request.json
        classNumber = req['classNumber']
        ipClassroom = req['ipClassroom']

        res = modulesModel.register(classNumber, ipClassroom)
        return jsonify({'message': 'Classroom Registered', 'idClassroom': res})

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
