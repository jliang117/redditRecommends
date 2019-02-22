from flask import Flask, jsonify, request
from flask_cors import CORS
import json

import dataFetching.search
from dataFetching.processData import NERExtraction


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
    with open('/data/tmp/nyc_ramen.json') as f:
    	data = json.load(f)
    return f

@app.route('/topsubreddits', methods=['GET'])
def top_subreddits():
    return jsonify('pong!')

@app.route('/topextracted', methods=['GET'])
def top_extracted():
    return jsonify('pong!')

def loadModules():
    NERExtraction.loadAllenNlp()


if __name__ == '__main__':
    # loadModules()
    app.run()