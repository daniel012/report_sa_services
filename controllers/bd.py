import pyodbc
from flask import Flask, jsonify

app = Flask(__name__)

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\uemar\OneDrive\Escritorio\SA_N1\bd1.mdb;')
cursor = conn.cursor()

@app.route('/consulta')
def consulta():
    cursor.execute('select * from Usuarios')
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append([x for x in row])
    return jsonify(data)

@app.route('/')
def index():
    return '<h1>Hola!<h1>'
