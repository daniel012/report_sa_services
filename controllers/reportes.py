from openpyxl import load_workbook, Workbook
from win32com import client
from .db import get_agente
import os
#import db

def reportes():
    rutaservicio = os.getcwd()
    data = get_agente()
    #ruta = "C:\\Users\\%USERNAME%\\Escritorio\\calera\\report_sa_services\\reportes\\"
    base = rutaservicio+"\\reportes\\base\\ocatalogoAgentes.xlsx"
    os.chdir("..\\..")
    #archivo = "C:\\Users\\uemar\\Desktop\\REPORTES\\catalogoAgentes.xlsx"
    ruta = os.getcwd()
    archivo = ruta+"\\REPORTES\\catalogoAgentes.xlsx"
    # Crear Excel
    wb = load_workbook(base)
    sheet = wb.active
    contador = 5
    contagent = 0
    agenteant = ""
    for i in range(len(data)):
        agente = data[contagent].get('id')
        nombre = data[contagent].get('name')
        correo = data[contagent].get('email')
        telefono = data[contagent].get('number')
        cliente = data[contagent].get('client')
        if agente != agenteant:
            sheet['A'+str(contador)] = nombre
            sheet['B'+str(contador)] = correo
            sheet['C'+str(contador)] = telefono
            sheet['D'+str(contador)] = cliente
        else:
            sheet['D'+str(contador)] = cliente
        agenteant = agente
        contador += 1 
        contagent += 1
        wb.save(archivo)

    # Crear PDF
    excel_file = client.Dispatch("Excel.Application")
    xl_sheets = excel_file.Workbooks.Open(archivo)
    worksheets = xl_sheets.Worksheets[0]
    worksheets.ExportAsFixedFormat(0, ruta+"\\reportes\\catalogoAgentes.pdf")
    excel_file.Workbooks.Close()
    os.chdir(rutaservicio)

reportes()