from openpyxl import load_workbook, Workbook
import win32com.client
#from win32com.client import Dispatch
from .db import get_agente
import os
import pythoncom
import winshell
from datetime import date


#import db

def reportes():
    hoy = date.today()
    hoyf = hoy.strftime("%d%m%Y")
    ruta = os.getcwd()
    escritorio = winshell.desktop()
    data = get_agente()
    base = ruta+"\\reportes\\base\\ocatalogoAgentes.xlsx"
    archivo = escritorio+"\\REPORTES\\catalogoAgentes-"+hoyf+".xlsx"
    # Crear Excel
    wb = load_workbook(base)
    sheet = wb.active
    contador = 6
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
    try:
        pythoncom.CoInitialize()
        excel_file = win32com.client.Dispatch("Excel.Application")
        xl_sheets = excel_file.Workbooks.Open(archivo)
        worksheets = xl_sheets.Worksheets[0]
        worksheets.ExportAsFixedFormat(0, escritorio+"\\REPORTES\\catalogoAgentes-"+hoyf+".pdf")
        excel_file.quit()
    except Exception as inst:
        print("OS error: {0}".format(inst))
    return

# reportes()