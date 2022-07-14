import email
from email.headerregistry import Address
from xml.dom.minidom import Identified
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from .db import executeQuery, tablaAgente, tablaCliente, tablaProducto, tablaVenta, tablaProductoVenta
from configparser import SafeConfigParser
from openpyxl import Workbook
from datetime import date


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
        rows = executeQuery("SELECT * FROM agente where correo == \""+correo+"\"")
        data =[]
        for row in rows:
            data.append({'id':row[0],'name':row[1],'address':row[2],'number':row[3],'email':row[4]})
        return jsonify(data), 200 if len(data) else 204

    @app.route('/agent', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def insertAgent():
        jsonValue = request.get_json()
        idAgente = tablaAgente('INSERTAR',jsonValue.get('name'),jsonValue.get('address'),jsonValue.get('phone'),jsonValue.get('email'))
        return str(idAgente), 201

    @app.route('/agent/<id>', methods= ['PUT'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def updateAgent(id):
        jsonValue = request.get_json()
        idAgente = tablaAgente('ACTUALIZAR',jsonValue.get('name'),jsonValue.get('address'),jsonValue.get('phone'),jsonValue.get('email'),id)
        return str(idAgente), 200

    @app.route('/client/<correo>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def get_dataClient(correo):
        rows = executeQuery("SELECT cliente.id,cliente.idagente,cliente.nombre,cliente.rfc,cliente.telefono,cliente.correo, agente.correo FROM cliente INNER JOIN agente on cliente.idagente = agente.id where cliente.correo == \""+correo+"\"")
        data =[]
        print(rows)
        for row in rows:
            data.append({'id':row[0],'nombre':row[2],'rfc':row[3],'telefono':row[4],'correo':row[5], 'agente':{'id':row[1],'email': row[6] }})
        return jsonify(data), 200 if len(data) else 204


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

    @app.route('/client/<id>', methods= ['PUT'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def updateClient(id):
        jsonValue = request.get_json()
        rows = executeQuery("SELECT id FROM agente where id == \""+str(jsonValue.get('idagente'))+"\"")
        
        if((len(rows)) != 0):
            idCliente = tablaCliente('ACTUALIZAR',jsonValue.get('idagente'),jsonValue.get('nombre'),jsonValue.get('rfc'),jsonValue.get('telefono'),jsonValue.get('correo'),id)
            return str(idCliente), 200
        else:
            return  'NoExisteAgente' , 409

    @app.route('/product/<code>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def get_data_product(code):
        rows = executeQuery("SELECT id, nombre, descripcion, existencia, existencia_real, nom_corto, precio_sugerido FROM producto where nom_corto == \""+code+"\"")
        data =[]
        for row in rows:
            data.append({'id':row[0],'name':row[1],'description':row[2],'amount':row[3],'real_amount':row[4],'code': row[5], 'productPrice':row[6] })
        return jsonify(data), 200 if len(data) else 204

    @app.route('/product', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def insert_product():
        jsonValue = request.get_json()
        idProduct = tablaProducto('INSERTAR',jsonValue.get('name'),jsonValue.get('description'),jsonValue.get('amount'),jsonValue.get('real_amount'),jsonValue.get('code'),jsonValue.get('fecha'), jsonValue.get('productPrice'))
        return str(idProduct), 201

    @app.route('/product/<id>', methods= ['PUT'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def update_product(id):
        jsonValue = request.get_json()
        idProduct = tablaProducto('ACTUALIZAR',jsonValue.get('name'),jsonValue.get('description'),jsonValue.get('amount'),jsonValue.get('real_amount'),jsonValue.get('code'),jsonValue.get('fecha'), jsonValue.get('productPrice'),id,jsonValue.get('isIngreso'),jsonValue.get('difference'))
        return str(idProduct), 200

    @app.route('/sell', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def insert_sell():
        jsonValue = request.get_json()
        idVenta = tablaVenta('INSERTAR',jsonValue.get('client'),jsonValue.get('dateSell'),0,jsonValue.get('payment'),jsonValue.get('total'),0)
        for i in jsonValue.get('list'):
            tablaProductoVenta('INSERTAR',i.get('id'),idVenta,i.get('amount'),i.get('amount'),i.get('unitPrice'))
        return str(idVenta), 201

    return app





