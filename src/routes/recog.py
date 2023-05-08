import io
import pickle
import zipfile
from flask import Blueprint, jsonify, make_response, request

# Models
from models.recogModel import recogModel

main = Blueprint('recogBlueprint', __name__)


@main.route('/update', methods=['GET'])
def updateModels():
    try:
        req = request.json
        knnVersion = req['Knn']
        namesVersion = req['Names']

        knn, knnNewVersion, names, namesNewVersion = recogModel.getModels(
            knnVersion, namesVersion)

        if knn is None and names is None:
            return jsonify({'message': 'OK'}), 200

        response = make_response()
        response.status_code = 200
        file_dict = {}
        if knn is not None:
            knnModel_bytes = pickle.dumps(pickle.loads(knn))
            file_dict['knn'] = knnModel_bytes
            response.headers['knnNewVersion'] = str(knnNewVersion)
        if names is not None:
            names_bytes = pickle.dumps(pickle.loads(names))
            file_dict['names'] = names_bytes
            response.headers['namesNewVersion'] = str(namesNewVersion)

        zip_data = io.BytesIO()
        with zipfile.ZipFile(zip_data, mode='w') as zip_file:
            for filename, file_content in file_dict.items():
                zip_file.writestr(filename, file_content)

        # Set the response data to the ZIP archive contents
        response.data = zip_data.getvalue()
        response.headers['Content-Disposition'] = 'attachment; filename=files.zip'
        response.headers['Content-Type'] = 'application/zip'
        return response

    except Exception as ex:
        print(ex)
        return jsonify({'message': str(ex)}), 500
