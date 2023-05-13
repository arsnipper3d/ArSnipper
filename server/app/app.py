# restful api flask app
from flask import Flask
from api.router import object_detection
from api.router import users
app = Flask(__name__)

app.route('/', methods=['GET'])
def root():
    return "Welcome to the AR Snipper 3D API!"
# register blueprint endpoints
app.register_blueprint(object_detection.object_detect, url_prefix='/object_detect')
app.register_blueprint(users.users)

if __name__ == '__main__':
    app.run(host='0.0.0.0')