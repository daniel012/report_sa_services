from asyncio.windows_events import NULL
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
        existencia_real INT)''')

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
        factura TEXT)''')

    cur.execute('''CREATE TABLE historial_pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idventa INT,
        fecha TEXT,
        nombre_corto TEXT,
        existencia INT
        existencia_real INT)''')

    cur.execute('''CREATE TABLE producto_venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idproducto INT,
        idventa INT,
        cantidad INT,
        entregado INT,
        precio REAL)''')

    # Insert a row of data
    #cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()

def tablaAgente(sql, nombre, direccion, telefono, correo, id=NULL):
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


def tablaCliente(sql, idagente, nombre, rfc, telefono, correo, id=NULL):
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

def tablaProducto(sql, nombre, descripcion, existencia, existencia_real, code, id=NULL):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()

    if sql == "INSERTAR":
        instruction = f"INSERT INTO producto (nombre, descripcion, existencia, existencia_real, nom_corto) VALUES ('{nombre}', '{descripcion}', '{existencia}', '{existencia_real}', '{code}')" 
        id = cur.lastrowid
    elif sql == "ACTUALIZAR":
        instruction = f"UPDATE producto SET nombre = '{nombre}' , descripcion = '{descripcion}' , existencia = '{existencia}', existencia_real = '{existencia_real}', nom_corto = '{code}' WHERE id = '{id}' " 

    cur.execute(instruction)
    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()
    return id

def tablaProductoVenta(sql, idproducto, idventa, cantidad, entregado, costo):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()

    if sql == "INSERTAR":
        instruction = f"INSERT INTO producto_venta (idproducto, idventa, cantidad, entregado, precio) VALUES ({idproducto}, {idventa}, {cantidad}, {entregado}, {costo})" 

    cur.execute(instruction)
    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()

def tablaVenta(sql, idcliente, fecha, forma_pago, monto_pago, total, factura):
    # Stabilished a connection
    con = sqlite3.connect('msa.db')
    # Create a cursor objet
    cur = con.cursor()

    if sql == "INSERTAR":
        instruction = f"INSERT INTO venta (idcliente, fecha, forma_pago, monto_pago, total, factura) VALUES ('{idcliente}', '{fecha}', '{forma_pago}', '{monto_pago}', '{total}', '{factura}')" 

    cur.execute(instruction)
    # Save (commit) the changes
    con.commit()
    # We can also close the connection if we are done with it.
    con.close()

def executeQuery(query):
    con = sqlite3.connect('msa.db')
    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    con.close()
    return rows
