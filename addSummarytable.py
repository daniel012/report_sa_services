import sqlite3

def createCalculatedTable():
        con = sqlite3.connect('C:\\Users\\jdaniel\\Desktop\\calera_project\\report_sa_services\\msa.db')
        cur = con.cursor()
        cur.execute(''' DROP TABLE precalculatedInformation ''')
        cur.execute('''CREATE TABLE precalculatedInformation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lastSellId INT,
                debt REAL,
                paid REAL,
                balance REAL,
                date TEXT)''')

        con.commit()
        con.close()

createCalculatedTable()
