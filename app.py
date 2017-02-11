import os

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://steemit:steemit@mongo1.steemdata.com:27017/SteemData'

mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST', '127.0.0.1'),
            debug=not os.getenv('PRODUCTION', False))
