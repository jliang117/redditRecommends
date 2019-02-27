from flask import Flask, jsonify, request
from flask_cors import CORS
import json

import search
import gconfig 


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/search', methods=['POST'])
def search_with_posted_string():
    if not request.json:
        abort(400)
    return search.searchAndExtract(request.json['search'])

@app.route('/', methods=['GET'])
def health():
    return "Hello"




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=gconfig.PORT, debug=gconfig.DEBUG_MODE)