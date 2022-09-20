from __future__ import print_function
import email
from email.headerregistry import Address
from xml.dom.minidom import Identified
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from .db import *
from .reportes import catalogoAgentes, catalogoProductos, estadisticasCliente, saldosCliente, comprobantePago, comprobanteVenta, reporteCierreVenta
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
        data = get_agente(correo)
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

    @app.route('/client/', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def get_Clients():
        query = "SELECT cliente.id,cliente.idagente,cliente.nombre,cliente.rfc,cliente.telefono,cliente.correo, agente.correo, agente.nombre FROM cliente INNER JOIN agente on cliente.idagente = agente.id";
        # print(query)
        rows = executeQuery(query)
        data =[]
        for row in rows:
            data.append({'id':row[0],'nombre':row[2],'rfc':row[3],'telefono':row[4],'correo':row[5], 'agente':{'id':row[1],'email': row[6], 'name':row[7] }})
        return jsonify(data), 200 if len(data) else 204

    @app.route('/client/<nombre>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def get_dataClient(nombre):
        query = "SELECT cliente.id,cliente.idagente,cliente.nombre,cliente.rfc,cliente.telefono,cliente.correo, agente.correo, agente.nombre FROM cliente INNER JOIN agente on cliente.idagente = agente.id where cliente.nombre == \""+nombre+"\"";
        # print(query)
        rows = executeQuery(query)
        data =[]
        for row in rows:
            data.append({'id':row[0],'nombre':row[2],'rfc':row[3],'telefono':row[4],'correo':row[5], 'agente':{'id':row[1],'email': row[6], 'name':row[7] }})
        return jsonify(data), 200 if len(data) else 204


    @app.route('/client', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def insertClient():
        clientJson = request.get_json();
        rows = executeQuery("SELECT * FROM cliente where nombre == \""+clientJson.get('nombre')+"\"")
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

    @app.route('/product', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def get_all_data_product():
        rows = executeQuery("SELECT id, nombre, descripcion, existencia, existencia_real, nom_corto, precio_sugerido,umedida FROM producto")
        data =[]
        for row in rows:
            data.append({'id':row[0],'name':row[1],'description':row[2],'amount':row[3],'real_amount':row[4],'code': row[5], 'productPrice':row[6], 'metric': row[7] })
        return jsonify(data), 200 if len(data) else 204

    @app.route('/product/<code>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def get_data_product(code):
        rows = executeQuery(f"SELECT id, nombre, descripcion, existencia, existencia_real, nom_corto, precio_sugerido, umedida FROM producto where nom_corto == '{code}'")
        if len(rows) == 0:
            return '', 204
        else:
            id = rows[0][0]
            infoSell = executeQuery(f"SELECT id FROM producto_venta where idproducto == '{id}'")
            data = {'id':id,'name':rows[0][1],'description':rows[0][2],'amount':rows[0][3],'real_amount':rows[0][4],'code': rows[0][5], 'productPrice':rows[0][6], 'metric':rows[0][7],'hasSells': True if len(infoSell) else False }
        return jsonify(data), 200

    @app.route('/product', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def insert_product():
        jsonValue = request.get_json()
        idProduct = tablaProducto('INSERTAR',jsonValue.get('name'),jsonValue.get('description'),jsonValue.get('amount'),jsonValue.get('real_amount'),jsonValue.get('code'),jsonValue.get('fecha'), jsonValue.get('productPrice'), jsonValue.get('metric') )
        return str(idProduct), 201

    @app.route('/product/<id>', methods= ['PUT'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def update_product(id):
        jsonValue = request.get_json()
        idProduct = tablaProducto('ACTUALIZAR',jsonValue.get('name'),jsonValue.get('description'),jsonValue.get('amount'),jsonValue.get('real_amount'),jsonValue.get('code'),jsonValue.get('fecha'), jsonValue.get('productPrice'),jsonValue.get('metric'),id,jsonValue.get('isIngreso'),jsonValue.get('difference'))
        return str(idProduct), 200

    @app.route('/sell', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def insert_sell():
        jsonValue = request.get_json()
        payment = jsonValue.get('payment')
        if(payment == ''):
            payment = 0
        else:
            payment = round(float(payment), 2)
        idVenta = creatVenta(jsonValue.get('client'),jsonValue.get('date'),payment,jsonValue.get('total'),jsonValue.get('invoice'), jsonValue.get('delivered'))
        idPago = -1
        if payment != 0:
            idPago = insertarHistorialPago(idVenta, date.today(), payment ,jsonValue.get('paymentType'))
        if idVenta != -1:
            for i in jsonValue.get('list'):
                # registra el precio y la cantidad por producto
                tablaProductoVenta('INSERTAR',i.get('id'),idVenta,i.get('amount'),i.get('unitPrice'))
                # actualiza cantidad del producto
                actualizar_producto_existencia(i.get('id'),i.get('newAmount'))
                # ingresa el egreso de un producto en su bitacora 
                insertProductHistory(i.get('id'), jsonValue.get('date'), i.get('amount'), 0, idVenta)
            return {'venta':idVenta,'pago':idPago}, 201
        else: 
            return 'FACTURA_REPETIDA', 409

    @app.route('/sell/<id>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def search_sell(id):
        rows = executeQuery(f"SELECT venta.id, fecha, monto_pago, total, entregado, factura, cliente.nombre, agente.nombre FROM venta INNER JOIN cliente on venta.idcliente == cliente.id INNER JOIN agente on agente.id == cliente.idagente where venta.id == '{id}'")
        if len(rows) != 0 :
            data =[]
            products = []
            listProducts = executeQuery(f"SELECT producto_venta.cantidad, producto_venta.precio, producto.nombre,producto.nom_corto, producto.umedida FROM producto_venta INNER JOIN producto on producto_venta.idproducto = producto.id where idventa == '{id}'")

            for row in listProducts:
                products.append({'amount':row[0],'unitPrice':row[1], 'product': row[2], 'code': row[3], 'metric': row[4]})

            paymentInfo = executeQuery(f"SELECT historial_pagos.fecha, historial_pagos.monto, historial_pagos.forma_pago,  historial_pagos.id FROM historial_pagos INNER JOIN venta on historial_pagos.idventa = venta.id where idventa == '{id}'")
            paymentDictionary = []
            for i in paymentInfo:
                paymentDictionary.append({'amount':i[1], 'date':i[0], 'paymentType':i[2],'id':i[3]})
            row = rows[0]
            data.append({'id':row[0],'date':row[1],'payment':row[2],'total':row[3],'delivered': row[4], 'invoice':row[5], 'list': products, 'clientName':row[6], 'agent':row[7], 'paymentHistory': paymentDictionary})

            return jsonify(data), 200
        else: 
            return 'VENTA_NO_ENCONTRADA', 204

    @app.route('/sell/deliver/<id>', methods= ['PUT'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def sell_deliver(id):
        VentaEntrega(id)
        return 'OK', 200

    @app.route('/payment', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def insert_payment():
        jsonValue = request.get_json()
        idSell = jsonValue.get('idSell')
        payment = jsonValue.get('payment')
        paymentType = jsonValue.get('paymentType')
        instruction = f"SELECT id, total , monto_pago FROM venta where id == '{idSell}'"
        rows = executeQuery(instruction)
        if len(rows) == 0: 
            return 'VENTA_NO_ENCONTRADA', 204
        sell = rows[0]
        newPayment = round(float(sell[2]),2 ) + round(float(payment), 2)

        total = sell[1]
        if total < newPayment:
            return 'MONTO_INVALIDO', 409
        paymentDate = date.today()
        idPayment = insertarHistorialPago(idSell,paymentDate, payment,paymentType, newPayment)
        return jsonify({'id':idPayment, 'amount': payment, 'date':str(paymentDate), 'paymentType': str(paymentType)}), 200

    @app.route('/productHistory/<idProduct>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def get_product_history(idProduct):
        rows = executeQuery(f"SELECT id, fecha, cantidad, ingreso, idventa  FROM producto_bitacora where idproducto == '{idProduct}'")
        data =[]
        for row in rows:
            data.append({'id':row[0],'date':row[1],'amount':row[2],'type':row[3],'idSell':row[4] })
        return jsonify(data), 200 if len(data) else 204

    @app.route('/report/agent', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def report_agent():
        catalogoAgentes()
        return 'ok'

    @app.route('/report/product', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def report_productos():
        catalogoProductos()
        return 'ok'

    @app.route('/report/staticClient/<idClient>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def report_estCliente(idClient):
        estadisticasCliente(idClient)
        return 'ok'

    @app.route('/report/delinquentCustomers', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def report_saldosCliente():
        saldosCliente()
        return 'ok'

    @app.route('/report/payment/<idVenta>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def report_payment(idVenta):
        comprobantePago(idVenta)
        return 'ok'

    @app.route('/report/sellAck/<idVenta>', methods= ['GET'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def report_sellAck(idVenta):
        comprobanteVenta(idVenta)
        return 'ok'

    @app.route('/report/endSell', methods= ['POST'])
    @cross_origin(origin='0.0.0.0',headers=['Content- Type','Authorization'])
    def report_endSell():
        jsonValue = request.get_json()
        startDate = jsonValue.get('startDate')
        endDate = jsonValue.get('endDate')
        startDateNum = startDate[0:4]+startDate[5:7]+startDate[8:10]
        endDateNum = None
        if endDate != '':
            endDateNum = endDate[0:4]+endDate[5:7]+endDate[8:10]
        reporteCierreVenta(startDateNum, endDateNum)
        return 'ok'

    return app





