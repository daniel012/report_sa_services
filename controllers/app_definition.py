from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import os
from .db import executeQuery, tablaAgente
from configparser import SafeConfigParser
from openpyxl import Workbook


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

    @app.route('/agent/<correo>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def get_data(correo):
        #rows = executeQuery("PRAGMA database_list;")
        rows = executeQuery("SELECT * FROM agente where correo == \""+correo+"\"")
        data =[]
        for row in rows:
            data.append([x for x in row])
        return jsonify(data)

    @app.route('/agent', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def insertAgent():
        jsonValue = request.get_json()
        tablaAgente('INSERTAR',jsonValue.get('name'),jsonValue.get('address'),jsonValue.get('phone'),jsonValue.get('email'))
        return 'ok'



    @app.route('/checking', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def checking():
        return  'hola'

    return app





