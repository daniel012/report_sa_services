import pyodbc
from configparser import SafeConfigParser

filename = "options.cfg"
parser = SafeConfigParser()
parser.read(filename)
        
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+parser['DB']['address'])
cursor = conn.cursor()

def executeQuery(query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

