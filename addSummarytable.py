import sqlite3
from datetime import date, timedelta

def createCalculatedTable(newSalary : int):
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
        selectQuery = f"SELECT id from venta order by id desc limit 1"
        cur.execute(selectQuery)
        selectQ = cur.fetchall()
        yesterday = date.today() - timedelta(days=1)
        # yesterday = date.today() 
        insert = f"INSERT INTO precalculatedInformation (date, lastSellId, balance, paid, debt) values('{yesterday.strftime('%Y/%m/%d')}', {selectQ[0][0]}, {newSalary}, {0}, {0})"
        cur.execute(insert)

        # queryAlter = "ALTER TABLE venta DROP COLUMN pricedOut"
        # cur.execute(queryAlter)

        # queryAlter = "ALTER TABLE venta ADD COLUMN pricedOut number default 0"
        # cur.execute(queryAlter)

        con.commit()
        con.close()

def updateExample():
       con = sqlite3.connect('C:\\Users\\jdaniel\\Desktop\\calera_project\\report_sa_services\\msa.db')
       cur = con.cursor()
       cur.execute('''UPDATE precalculatedInformation SET date="2023/02/04" WHERE id ="1" ''')  
       con.commit()
       con.close()

def deleteLastPreCal():
       con = sqlite3.connect('C:\\Users\\jdaniel\\Desktop\\calera_project\\report_sa_services\\msa.db')
       cur = con.cursor()
       cur.execute('''DELETE FROM precalculatedInformation WHERE id > "1"''')    
       cur.execute('''DELETE FROM venta WHERE id > "483"''')  
       con.commit()
       con.close()

# deleteLastPreCal()
# updateExample()
## use user balance, we cannot do prev work
createCalculatedTable(1000)
