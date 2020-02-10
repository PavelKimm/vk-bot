from src import config
from src import message_handler
from flask import Flask, request, json
from src.models import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config.from_object("config")
app.config.from_object("config.DevelopmentConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


Session = sessionmaker()
Session.configure(bind=create_engine(config.Config.SQLALCHEMY_DATABASE_URI))
session = Session()


@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return config.confirmation_token
    elif data['type'] == 'message_new':
        message_handler.create_answer(data['object'], config.token)
        return 'ok'


if __name__ == "__main__":
    app.run()
