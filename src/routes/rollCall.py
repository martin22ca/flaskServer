from flask import Blueprint, jsonify, request
import uuid

# Entities
from models.entities.rollCallEntity import rollCall

# Models
from models.rollCallModel import rollCallModel

main = Blueprint('rollCallBlueprint', __name__)

@main.route('/')
def getRollCalls():
    try:
        calls = rollCallModel.getRollCalls()
        return jsonify(calls)
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
