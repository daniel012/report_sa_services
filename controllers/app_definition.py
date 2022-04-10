from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import os
from .db import executeQuery 
from configparser import SafeConfigParser


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
        rows = executeQuery('Select * from Usuarios')
        data =[]
        for row in rows:
            data.append([x for x in row])
        return jsonify(data)


    @app.route('/checking', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def checking():
        return  'hola'

    return app





