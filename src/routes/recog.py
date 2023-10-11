import io
import pickle
import zipfile
from flask import Blueprint, jsonify, make_response, request

# Models
from models.recogModel import recogModel
from models.messageModel import messageModel

main = Blueprint('recogBlueprint', __name__)


@main.route('/registerAi', methods=['POST'])
def registerAi():
    try:
        req = request.json 
        images = req['images']
        idStud = req['idStud']
        recogModel.registerEncodings(images,idStud)

        return jsonify({'message': 'ok'}), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update', methods=['GET'])
def updateModels():
    try:
        req = request.json
        classNumber = req['classNumber']
        className = req['className']
        knnVersion = req['Knn']
        namesVersion = req['Names']

        knn, knnNewVersion, names, namesNewVersion = recogModel.getModels(
            knnVersion, namesVersion)

        if knn == None and names == None:
            print("Models up to date")
            return jsonify({'message': 'OK'}), 200

        print("Updating Models")
        response = make_response()
        response.headers['update'] = False
        file_dict = {}
        if knn is not None:
            knnModel_bytes = pickle.dumps(pickle.loads(knn))
            file_dict['knn'] = knnModel_bytes
            response.headers['knnNewVersion'] = str(knnNewVersion)
            response.headers['update'] = True
        if names is not None:
            names_bytes = pickle.dumps(pickle.loads(names))
            file_dict['names'] = names_bytes
            response.headers['namesNewVersion'] = str(namesNewVersion)
            response.headers['update'] = True

        zip_data = io.BytesIO()
        with zipfile.ZipFile(zip_data, mode='w') as zip_file:
            for filename, file_content in file_dict.items():
                zip_file.writestr(filename, file_content)

        txt = 'Se actualizo el curso: ' + \
            str(classNumber) + ' ' + str(className)
        messageModel.msgAdmin('Actualizado Reconocimiento Facial', txt, None)

        # Set the response data to the ZIP archive contents
        response.data = zip_data.getvalue()
        response.headers['Content-Disposition'] = 'attachment; filename=files.zip'
        response.headers['Content-Type'] = 'application/zip'

        return response

    except Exception as ex:
        print(ex)
        return jsonify({'message': str(ex)}), 500
