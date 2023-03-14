from flask import Blueprint, jsonify, request

# Entities
from models.entities.studentEntity import Student

# Models
from models.studentModel import studentModel

main = Blueprint('studentBlueprint', __name__)

@main.route('/')
def getStudents():
    try:
        students = studentModel.getStudents()
        return jsonify(students)
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/newStudent')    
def setNewStudent(request):
    try:
        print(request)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


