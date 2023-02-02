import sqlite3
from datetime import date, datetime, timedelta

def createDB():
    # Stabilished a connection
    con = sqlite3.connect('C:\\Users\\uemar\\Desktop\\calera\\report_sa_services\\msa.db')
    # Create a cursor objet
    cur = con.cursor()

    # Create table
    cur.execute('''CREATE TABLE producto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        nom_corto TEXT,
        descripcion TEXT,
        existencia INT,
        existencia_real INT,
        umedida TEXT,
        precio_sugerido REAL)''')

    cur.execute('''CREATE TABLE compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idproducto INT,
        empresa TEXT,
        cantidad INT,
        costo REAL)''')

    cur.execute('''CREATE TABLE agente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        direccion TEXT,
        telefono TEXT,
        correo TEXT)''')

    cur.execute('''CREATE TABLE cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idagente INT,
        nombre TEXT,
        rfc TEXT,
        telefono TEXT,
        correo TEXT)''')

    cur.execute('''CREATE TABLE venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idcliente INT,
        fecha TEXT,
        monto_pago REAL,
        total REAL,
        entregado INT,
        factura TEXT)''')

    cur.execute('''CREATE TABLE historial_pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idventa INT,
        fecha TEXT,
        forma_pago INT,
        monto REAL)''')

    cur.execute('''CREATE TABLE producto_venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idproducto INT,
        idventa INT,
        cantidad INT,
        precio REAL)''')

    cur.execute('''CREATE TABLE producto_bitacora (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idproducto INT,
        fecha TEXT,
        cantidad INT,
        ingreso INT,
        idventa INT)''')

    # Insert a row of data
    #cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()

def get_agente(correo=None):
    instruccion = f"SELECT agente.id,agente.nombre,agente.direccion,agente.telefono,agente.correo,cliente.nombre, cliente.correo, cliente.telefono FROM agente LEFT JOIN cliente ON agente.id==cliente.idagente"
    if correo is not None:
        instruccion = instruccion + " where agente.correo == \""+correo+"\""
    instruccion = instruccion + " ORDER BY agente.nombre asc"
    rows = executeQuery(instruccion)
    data =[]
    for row in rows:
        data.append({'id':row[0],'name':row[1],'address':row[2],'number':row[3],'email':row[4],'client':row[5],'clientEmail':row[6],'clientNumber':row[7]})
    return data

def get_productos():
    instruccion = f"SELECT nom_corto,descripcion,nombre,existencia_real, umedida FROM producto"
    rows = executeQuery(instruccion)
    data =[]
    for row in rows:
        data.append({'nom_corto':row[0],'descripcion':row[1],'nombre':row[2],'existencia_real':f'{row[3]} {row[4]}'})
    return data

def get_compPago(idVenta):
    instruccion = f"SELECT fecha, monto FROM historial_pagos WHERE historial_pagos.idventa == {idVenta}"
    rows = executeQuery(instruccion)
    payment =[]
    for row in rows:
        payment.append({'fecha':row[0],'monto':row[1]})

    instruccion = f"SELECT cliente.nombre, agente.nombre, venta.fecha, venta.total, venta.monto_pago FROM venta INNER JOIN cliente on venta.idcliente == cliente.id INNER JOIN agente on agente.id = cliente.idagente WHERE venta.id == {idVenta}"
    rows = executeQuery(instruccion)
    data = {'cliente':rows[0][0],'agente':rows[0][1],'vfecha':rows[0][2],'vtotal':rows[0][3],'vpagado':rows[0][4], 'historial': payment}

    return data

def get_compVenta(idVenta):
    #instruccion = f"SELECT idproducto, cantidad, precio FROM producto_venta WHERE idventa == {idVenta}"
    instruccion = f"SELECT producto.nom_corto, producto_venta.cantidad, producto_venta.precio, producto.descripcion FROM producto_venta INNER JOIN producto ON producto.id == producto_venta.idproducto WHERE idventa == {idVenta}"
    rows = executeQuery(instruccion)
    productos =[]
    for row in rows:
        productos.append({'idproducto':row[0],'cantidad':row[1],'precio':row[2],'descripcion':row[3]})

    instruccion = f"SELECT cliente.nombre, agente.nombre, venta.fecha, venta.total FROM venta INNER JOIN cliente on venta.idcliente == cliente.id INNER JOIN agente ON agente.id = cliente.idagente WHERE venta.id == {idVenta}"
    rows = executeQuery(instruccion)
    data = {'cliente':rows[0][0],'agente':rows[0][1],'vfecha':rows[0][2],'vtotal':rows[0][3], 'productos': productos}

    return data

def get_estadisticaCliente(cliente):
    instruccion = f"SELECT cliente.nombre, agente.nombre FROM cliente INNER JOIN agente ON cliente.idagente==agente.id WHERE cliente.id=={cliente} "
    rows = executeQuery(instruccion)
    if len(rows):
        instruccion = f"SELECT venta.id, venta.fecha, venta.total, venta.monto_pago, producto.descripcion, producto.nom_corto, producto_venta.cantidad, producto_venta.precio, producto.umedida FROM venta INNER JOIN producto_venta ON producto_venta.idventa==venta.id INNER JOIN producto ON producto.id==producto_venta.idproducto WHERE venta.idcliente=={cliente} "
        dataVenta = executeQuery(instruccion)
        listaVenta = []
        for info in dataVenta:
            listaVenta.append({'vclave':info[0],'vfecha':info[1],'vtotal':info[2],'vpago':info[3],'pdescripcion':info[4],'pclave':info[5],'pcantidad':f'{info[6]} {info[8]}','pprecio':info[7]})
        data = {'cliente':rows[0][0],'agente':rows[0][1],'datosVenta':listaVenta}
    return data

def get_saldoCliente():
    instruccion = f"SELECT venta.id,cliente.nombre,venta.fecha,venta.monto_pago,venta.total, agente.nombre,(venta.total - venta.monto_pago), producto.nom_corto FROM venta  INNER JOIN cliente ON cliente.id==venta.idcliente JOIN agente on agente.id == cliente.idagente JOIN producto_venta ON producto_venta.idventa == venta.id JOIN producto ON producto.id == producto_venta.idproducto WHERE venta.total!=venta.monto_pago ORDER BY agente.nombre,cliente.nombre, (venta.total - venta.monto_pago) DESC"
    rows = executeQuery(instruccion)
    map = {}
    agentSum = {}
    total = 0
    for row in rows:
        if row[5] not in map: 
            map[row[5]] = {}
            agentSum[row[5]] = 0
        if row[1] not in map[row[5]]:
            map[row[5]][row[1]] = {'debt': 0, 'data':[]} 
        debt = row[4] - row[3]
        map[row[5]][row[1]]['debt'] += debt
        agentSum[row[5]] += debt
        total += debt
        fecha = datetime.strptime(row[2],'%Y-%m-%d')
        map[row[5]][row[1]]['data'].append({'idVenta':row[0],'cliente':row[1],'fecha': fecha,'montoPagado':row[3], 'totalPagar':row[4], 'agente':row[5], 'deuda':row[6], 'debt': debt, 'product': row[7]})
    return {'data':map, 'agentSum':agentSum, 'total': total}

def tablaAgente(sql, nombre, direccion, telefono, correo, id=None):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()

    if sql == "INSERTAR":
        instruction = f"INSERT INTO agente (nombre, direccion, telefono, correo) VALUES ('{nombre}', '{direccion}', '{telefono}', '{correo}' )"
        id = cur.lastrowid
    elif sql == "ACTUALIZAR":
        instruction = f"UPDATE agente SET nombre = '{nombre}' , direccion = '{direccion}' , telefono = '{telefono}' WHERE id = '{id}' "

    cur.execute(instruction)
    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()
    return id

def tablaCliente(sql, idagente, nombre, rfc, telefono, correo, id=None):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()

    if sql == "INSERTAR":
        instruction = f"INSERT INTO cliente (idagente, nombre, rfc, telefono, correo) VALUES ({idagente}, '{(nombre.rstrip())}', '{rfc}', '{telefono}', '{correo}' )"
        id = cur.lastrowid
    elif sql == "ACTUALIZAR":
        instruction = f"UPDATE cliente SET idagente = '{idagente}' , nombre = '{nombre}' , rfc = '{rfc}', telefono = '{telefono}', correo='{correo}' WHERE id = '{id}' "

    cur.execute(instruction)
    id = cur.lastrowid
    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()
    return id

def tablaCompras(sql, idproducto, empresa, cantidad, costo):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()

    if sql == "INSERTAR":
        instruction = f"INSERT INTO compras (idproducto, empresa, cantidad, costo) VALUES ({idproducto}, '{empresa}', {cantidad}, {costo})"

    cur.execute(instruction)
    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()

def tablaProducto(sql, nombre, descripcion, existencia, existencia_real, code, fecha, precio_sugerido, umedida, id=None, isIngreso= None, difference=None):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()

    if sql == "INSERTAR":

        instruction = f"INSERT INTO producto (nombre, descripcion, existencia, existencia_real, nom_corto, precio_sugerido, umedida) VALUES ('{nombre}', '{descripcion}', '{existencia}', '{existencia_real}', '{(code.rstrip())}', '{precio_sugerido}', '{umedida}')"
        cur.execute(instruction)
        id = cur.lastrowid
        instruction = f"INSERT INTO producto_bitacora (idproducto, fecha, cantidad, ingreso) VALUES ('{id}', '{fecha}', '{existencia}', '{1}')"
        cur.execute(instruction)
    elif sql == "ACTUALIZAR":
        instruction = f"UPDATE producto SET nombre = '{nombre}' , descripcion = '{descripcion}' , existencia = '{existencia}', existencia_real = '{existencia_real}', nom_corto = '{code}' , precio_sugerido = '{precio_sugerido}' , umedida= '{umedida}' WHERE id = '{id}' "
        cur.execute(instruction)
        if id is not None and isIngreso is not None and difference is not None and fecha is not None:
            instruction = f"INSERT INTO producto_bitacora (idproducto, fecha, cantidad, ingreso) VALUES ('{id}', '{fecha}', '{difference}', '{isIngreso}')"
            cur.execute(instruction)
    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()
    return id

def actualizar_producto_existencia(id, existencia):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()
    instruction = f"UPDATE producto SET existencia = '{existencia}', existencia_real = '{existencia}' WHERE id = '{id}' "
    cur.execute(instruction)
    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()
    return id

def tablaProductoVenta(sql, idproducto, idventa, cantidad, costo):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()

    if sql == "INSERTAR":
        instruction = f"INSERT INTO producto_venta (idproducto, idventa, cantidad, precio) VALUES ({idproducto}, {idventa}, {cantidad}, {costo})"
    cur.execute(instruction)
    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()

def creatVenta(idcliente, fecha, monto_pago, total, factura, entregado):
    if factura != '' :
        facturabd = executeQuery(f"SELECT factura FROM venta WHERE factura = '{factura}'")
        if len(facturabd) != 0:
            return -1
    con = sqlite3.connect('msa.db')
    cur = con.cursor()
    instruction = f"INSERT INTO venta (idcliente, fecha, monto_pago, total, factura, entregado) VALUES ('{idcliente}', '{fecha}', '{monto_pago}', '{total}', '{factura}', '{bool(entregado)}')"
    cur.execute(instruction)
    con.commit()
    id = cur.lastrowid
    con.close()
    return id

def VentaEntrega(id):
    con = sqlite3.connect('msa.db')
    cur = con.cursor()
    instruction = f"UPDATE venta SET entregado = '{True}' where id = '{id}'"
    cur.execute(instruction)
    con.commit()
    con.close()
    return id

def insertarHistorialPago(idventa,paymentDate,  payment, paymentType, newPayment = None):
    con = sqlite3.connect('msa.db')
    cur = con.cursor()
    instruction = f"INSERT INTO historial_pagos (idventa, monto, fecha, forma_pago) VALUES ('{idventa}', '{payment}', '{paymentDate}', '{paymentType}')"
    cur.execute(instruction)
    id = cur.lastrowid
    if newPayment is not None:
        instruction = f"UPDATE venta SET monto_pago = {newPayment} where id = '{idventa}'"
        cur.execute(instruction)
    con.commit()
    con.close()
    return id

def insertProductHistory(idproducto, fecha, cantidad,ingreso, idventa):
    con = sqlite3.connect('msa.db')
    cur = con.cursor()
    instruction = f"INSERT INTO producto_bitacora (idproducto, fecha, cantidad, ingreso, idventa) VALUES ('{idproducto}', '{fecha}', '{cantidad}', '{ingreso}', '{idventa}')"
    cur.execute(instruction)
    id = cur.lastrowid
    con.commit()
    con.close()
    return id

def executeQuery(query):
    # con = sqlite3.connect('C:\\Users\\uemar\\OneDrive\\Escritorio\\calera\\report_sa_services\\msa.db')
    con = sqlite3.connect('msa.db')
    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    con.close()
    return rows

def cierreDeVenta(generatePrevInfo:bool, startDate, endDate=None):
    con = sqlite3.connect('msa.db')
    cursor = con.cursor()
    basicInfo = createBasicInfo(cursor, startDate, endDate)
    preCalculated = {}
    
    if generatePrevInfo: 
        preCalculated = summaryPreCalculated(cursor)
    
    con.commit()
    con.close()
    return {
       'basicInfo': basicInfo, 
       'preCalculated': preCalculated
    }

def summaryPreCalculated(cursor: sqlite3.Cursor):
    query:str = "SELECT lastSellId, debt, paid, date, balance FROM precalculatedInformation ORDER BY id DESC limit 1"
    cursor.execute(query)
    preCalculated = cursor.fetchall()
    prevLastid:int = 0
    prevDebt:int =0
    prevPaid:int =0
    prevDate = ''
    prevBalance:int = 0
    currentInfo = {
        'paid': 0, 
        'debt': 0,
        'balance':0,
        'lastSellId': 0
    }

    if len(preCalculated) > 0: 
        prevLastid = preCalculated[0][0]
        prevDebt = preCalculated[0][1]
        prevPaid = preCalculated[0][2]
        prevDate = preCalculated[0][3]
        prevBalance = preCalculated[0][4]

        if preCalculated[0][3] == datetime.today().date().strftime('%Y/%m/%d'):
            return {
                'currentInfo': {
                    'paid':prevPaid,
                    'debt':prevDebt,
                    'balance': prevBalance
                }, 
                'prevDebt': prevDebt, 
                'prevPaid': prevPaid, 
                'prevDate': prevDate,
                'prevBalance': prevBalance,
                'lastSellId': prevLastid
            }

    query = f"SELECT total, monto_pago, id FROM venta WHERE id > {prevLastid} ORDER BY id desc"
    cursor.execute(query)
    current = cursor.fetchall()
    if len(current) > 0:
        for sell in current: 
            currentInfo['paid'] += sell[1]
            currentInfo['debt'] += (sell[0] -sell[1])
        currentInfo['lastSellId'] = current[0][2]
    else:
        currentInfo['lastSellId'] = prevLastid
    
    currentInfo['balance'] = currentInfo['paid'] + prevBalance

    query = f"INSERT INTO precalculatedInformation (date, lastSellId, balance, paid, debt) values('{datetime.today().date().strftime('%Y/%m/%d')}', {currentInfo['lastSellId']}, {currentInfo['balance']}, {currentInfo['paid']}, {currentInfo['debt']})"
    cursor.execute(query)

    

    return {
        'currentInfo': currentInfo, 
        'prevDebt': prevDebt, 
        'prevPaid': prevPaid, 
        'prevDate': prevDate,
        'prevBalance': prevBalance
    }

def createBasicInfo(cursor: sqlite3.Cursor, startDate, endDate=None):
    result = []
    productSum = {}
    sumSellType = {
        'cash': 0,
        'debt':0
    }
    
    query = f"SELECT venta.factura, cliente.nombre, venta.id, venta.fecha, venta.total, venta.monto_pago FROM venta INNER JOIN cliente on venta.idcliente == cliente.id "
    clause = ''
    if endDate is None:
        clause = f"Where CAST( substr(venta.fecha,1,4)||substr(venta.fecha,6,2)||substr(venta.fecha,9,2) AS INT)  >= {startDate}"
    else:
        clause = f"Where CAST( substr(venta.fecha,1,4)||substr(venta.fecha,6,2)||substr(venta.fecha,9,2) AS INT)  BETWEEN {startDate} AND {endDate}"

    query = query + clause
    cursor.execute(query)
    rows = cursor.fetchall()
    idsVenta= []
    info = {}
    for venta in rows:
        idsVenta.append(f"{venta[2]}")
        info[venta[2]] = {'ventaId':venta[2], 'ventaFactura':venta[0], 'ventaCliente':venta[1],'date':venta[3],'total':venta[4], 'pagado':venta[5]}
        sumSellType['cash'] += venta[5]
        sumSellType['debt'] += venta[4]-venta[5]
    idsVenta = ",".join(idsVenta)
    query =f"SELECT producto_venta.idventa, producto_venta.precio, producto_venta.cantidad, producto.nom_corto, producto.nombre, producto.umedida FROM producto_venta INNER JOIN producto ON producto.id == producto_venta.idproducto WHERE idventa IN ({idsVenta}) ORDER BY producto_venta.idventa"
    cursor.execute(query)
    rows = cursor.fetchall()
    for producto in rows:
        idVenta = producto[0]
        listProduct = []
        if('listProduct' in info[idVenta]):
            listProduct = info[idVenta]['listProduct']
        price = round(float(producto[2])*float(producto[1]),2)
        listProduct.append({'price':price, 'code':producto[3], 'name': producto[4], 'amount': f"{producto[2]} {producto[5]}"})
        info[idVenta]['listProduct'] = listProduct
        if producto[3] not in productSum:
            productSum[producto[3]] = {'sum' :0, 'amount':0 }

        productSum[producto[3]]['amount'] += producto[2]
        productSum[producto[3]]['sum'] += (producto[1] * producto[2])

    query = f"SELECT idventa, monto, forma_pago FROM historial_pagos WHERE idventa IN ({idsVenta}) "

    cursor.execute(query)
    rows = cursor.fetchall()
    for payment in rows:
        listCounts = {}
        if 'payment' in info[payment[0]]:
            listCounts = info[payment[0]]['payment']
        if payment[2] == 'True':
            key = 'cash'
        else:
            key = 'credit'

        if(key in listCounts):
            listCounts[key] = round(listCounts[key] + float(payment[1]),2)
        else:
            listCounts[key] = round(float(payment[1]),2)

        info[payment[0]]['payment'] = listCounts   
    for row in info:
        result.append(info[row])
    
    return {'info': result, "productSum":productSum, "sumSell": sumSellType}
