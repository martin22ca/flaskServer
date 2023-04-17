import uuid
import socket
from flask import Flask
from config import config
from managerLib.sheduler import BackgroundManager 
from zeroconf import Zeroconf, ServiceInfo

# Routes
from routes import  attendeces,classroom

app = Flask(__name__)

def page_not_found(error):
    return "<h1>URL Not found</h1>", 404

ip_address = socket.gethostbyname(socket.gethostname()+".local")
info = ServiceInfo(
    "_http._tcp.local.",
    "flaskServer"+ str(uuid.uuid4()) +"._http._tcp.local.",
    addresses=[socket.inet_aton(ip_address)],
    port=5001,
)

zeroconf = Zeroconf()
zeroconf.register_service(info)

if __name__ == '__main__':
    bSheduler = BackgroundManager()
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(attendeces.main, url_prefix='/attendece')
    app.register_blueprint(classroom.main, url_prefix='/classroom')

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.run(host="0.0.0.0", port=5000,use_reloader=False)
