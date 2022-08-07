import sqlite3

def createDB():
    # Stabilished a connection
    con = sqlite3.connect('C:\\Users\\jdaniel\\Desktop\\calera_project\\report_sa_services\\msa.db')
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
        forma_pago INT,
        monto_pago REAL,
        total REAL,
        entregado INT,
        factura TEXT)''')

    cur.execute('''CREATE TABLE historial_pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idventa INT,
        fecha TEXT,
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
    instruccion = f"SELECT agente.id,agente.nombre,agente.direccion,agente.telefono,agente.correo,cliente.nombre FROM agente LEFT JOIN cliente ON agente.id==cliente.idagente"
    if correo is not None:
        instruccion = instruccion + " where agente.correo == \""+correo+"\""
    rows = executeQuery(instruccion)
    data =[]
    for row in rows:
        data.append({'id':row[0],'name':row[1],'address':row[2],'number':row[3],'email':row[4],'client':row[5]})
    return data

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
        instruction = f"INSERT INTO cliente (idagente, nombre, rfc, telefono, correo) VALUES ({idagente}, '{nombre}', '{rfc}', '{telefono}', '{correo}' )" 
        id = cur.lastrowid
    elif sql == "ACTUALIZAR":
        instruction = f"UPDATE cliente SET idagente = '{idagente}' , nombre = '{nombre}' , rfc = '{rfc}', telefono = '{telefono}' WHERE id = '{id}' "

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

def tablaProducto(sql, nombre, descripcion, existencia, existencia_real, code, fecha, precio_sugerido, id=None, isIngreso= None, difference=None):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()

    if sql == "INSERTAR":

        instruction = f"INSERT INTO producto (nombre, descripcion, existencia, existencia_real, nom_corto, precio_sugerido) VALUES ('{nombre}', '{descripcion}', '{existencia}', '{existencia_real}', '{code}', '{precio_sugerido}')" 
        cur.execute(instruction)
        id = cur.lastrowid
        instruction = f"INSERT INTO producto_bitacora (idproducto, fecha, cantidad, ingreso) VALUES ('{id}', '{fecha}', '{existencia}', '{1}')" 
        cur.execute(instruction)
    elif sql == "ACTUALIZAR":
        instruction = f"UPDATE producto SET nombre = '{nombre}' , descripcion = '{descripcion}' , existencia = '{existencia}', existencia_real = '{existencia_real}', nom_corto = '{code}' , precio_sugerido = '{precio_sugerido}' WHERE id = '{id}' " 
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

def tablaVenta(sql, idcliente, fecha, forma_pago, monto_pago, total, factura, entregado):
    if sql == "INSERTAR":
        if factura != '' :
            facturabd = executeQuery(f"SELECT factura FROM venta WHERE factura = '{factura}'")
            if len(facturabd) != 0:
                return -1
        con = sqlite3.connect('msa.db')
        cur = con.cursor()
        instruction = f"INSERT INTO venta (idcliente, fecha, forma_pago, monto_pago, total, factura, entregado) VALUES ('{idcliente}', '{fecha}', '{forma_pago}', '{monto_pago}', '{total}', '{factura}', '{bool(entregado)}')" 
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

def insertarHistorialPago(idventa,paymentDate,  payment, newPayment = None):
    con = sqlite3.connect('msa.db')
    cur = con.cursor()
    instruction = f"INSERT INTO historial_pagos (idventa, monto, fecha) VALUES ('{idventa}', '{payment}', '{paymentDate}')" 
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

# createDB()