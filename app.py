import os

from flask import Flask, abort
from flask import render_template
from flask import request
from flask_misaka import Misaka
from flask_pymongo import PyMongo

from methods import comment_history, recreate_body_diffs, parse_identifier

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://steemit:steemit@mongo1.steemdata.com:27017/SteemData'

mongo = PyMongo(app)
Misaka(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/history', methods=['GET'])
def history():
    identifier_uri = request.args.get('identifier')
    app.logger.info(identifier_uri)
    comments = comment_history(mongo.db, identifier_uri)
    if not comments:
        abort(404)
    original, diffs = recreate_body_diffs(comments)
    return render_template('history.html',
                           identifier=parse_identifier(identifier_uri),
                           original=original,
                           diffs=diffs)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST', '127.0.0.1'),
            debug=not os.getenv('PRODUCTION', False))
