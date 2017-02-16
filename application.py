# Flask application script
from flask import Flask, request, jsonify, Response, render_template
import os
import compare_api

application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Hello World! Nothing is broken... yet!'

@application.route('/compare', methods=['POST'])
def compare():
    return compare_api.compare(request.get_json())


if __name__ == '__main__':
    application.debug = True
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0',port = port, debug = True)
