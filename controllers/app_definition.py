from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import os
from .load_info import load_information 

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def get_data():
        key = request.args.get('key')
        data = load_information(key)
        return jsonify(data)

    @app.route('/repair', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def post_request():
        return 'ok'

    return app





