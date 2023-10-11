import socket
from flask import Flask
from flask_cors import CORS
from config import config
from decouple import config as envConfig
from utils.managerLib.sheduler import BackgroundManager

# Routes
from routes import attendeces, classroom, recog
app = Flask(__name__)
CORS(app) 


def page_not_found(error):
    return "<h1>URL Not found</h1>", 404


ip_address = socket.gethostbyname(socket.gethostname()+".local")

if __name__ == '__main__':
    bSheduler = BackgroundManager()
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(attendeces.main, url_prefix='/attendece')
    app.register_blueprint(classroom.main, url_prefix='/classroom')
    app.register_blueprint(recog.main, url_prefix='/recog')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.run(host="0.0.0.0", port=int(envConfig('FLASK_PORT')), use_reloader=False)