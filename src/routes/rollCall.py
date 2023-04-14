from flask import Blueprint, jsonify, request
from datetime import date
import uuid

# Entities
from models.entities.rollCallEntity import RollCall

# Models
from models.rollCallModel import rollCallModel

main = Blueprint('rollCallBlueprint', __name__)
    
@main.route('/today/<idClassStud>')
def getRollCallToday(idClassStud):
    try:
        call = rollCallModel.rolTodayfromClass(idClassStud).toJSON()
        return jsonify(call)
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/create/<idClassStud>', methods=['POST'])
def add_rollCall(idClassStud):
    try:
        rollDate = date.today()
        rollCall = RollCall(1,idClassStud,rollDate)

        affected_rows = rollCallModel.createRollCall(rollCall)

        if affected_rows == 1:
            return jsonify({'message': "Created new roll Call"})
        else:
            return jsonify({'message': "Error on insert"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
