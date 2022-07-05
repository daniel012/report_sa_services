from xml.dom.minidom import Identified
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import os
from .db import executeQuery, tablaAgente, tablaCliente
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



    @app.route('/client', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def insertClient():
        clientJson = request.get_json();
        rows = executeQuery("SELECT * FROM cliente where correo == \""+clientJson.get('correo')+"\"")
        if((len(rows)) != 0):
            return  'clienteExiste' , 409
        else:
            rowAgente = executeQuery("SELECT id FROM agente where correo == \""+clientJson.get('correoAgente')+"\"")
            if(len(rowAgente) == 0):
                return 'agenteNoExiste', 409
            else:
                idClient = tablaCliente("INSERTAR",rowAgente[0][0],clientJson.get('nombre'),clientJson.get('rfc'),clientJson.get('telefono'),clientJson.get('correo'))
                return str(idClient), 201
    return app





