from bd import executeQuery
from openpyxl import Workbook
import os

# using getlogin() returning username
usuario = os.getlogin()
print(usuario)
fileex="C:\\Users\\"+usuario+"\\OneDrive\\Documentos\\Reportes\\sample.xlsx"

workbook = Workbook(fileex)
sheet = workbook.active

rows = executeQuery('Select * from Usuarios')
data =[]
for row in rows:
    data.append([x for x in row])

sheet['A3'] = data
workbook.save(fileex)