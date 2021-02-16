import flask
from flask import request, jsonify
from model.library import Library

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    library = Library()
    books = library.findAll()
    library.closeConnection()
    return jsonify(books)


@app.route('/findBooks', methods=['GET'])
def findBooks():
    library = Library()
    query_parameters = request.args
    target = query_parameters.get('target')
    books = library.findBooksByTarget(target)
    library.closeConnection()
    return jsonify(books)


app.run()
