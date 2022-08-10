from openpyxl import load_workbook, Workbook
import win32com.client
#from win32com.client import Dispatch
from .db import get_agente, get_productos, get_estadisticaCliente
import os
import pythoncom
import winshell
from datetime import date, datetime

escritorio = winshell.desktop()
hoy = date.today()
hoyf = hoy.strftime("%d%m%Y")
ruta = os.getcwd()

def catalogoAgentes():
    data = get_agente()
    archivo = "catalogoAgentes"
    base = ruta+"\\reportes\\base\\o"+archivo+".xlsx"
    archivoe = escritorio+"\\REPORTES\\"+archivo+"-"+hoyf+".xlsx"
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
    wb.save(archivoe) 
    crearPdf(archivoe, archivo) 

def catalogoProductos():
    data = get_productos()
    archivo = "catalogoProductos"
    base = ruta+"\\reportes\\base\\o"+archivo+".xlsx"
    archivoe = escritorio+"\\REPORTES\\"+archivo+"-"+hoyf+".xlsx"
    # Crear Excel
    wb = load_workbook(base)
    sheet = wb.active
    contador = 5
    contaprod = 0
    for i in range(len(data)):
        clave = data[contaprod].get('nom_corto')
        descripcion = data[contaprod].get('descripcion')
        nombre = data[contaprod].get('nombre')
        existencia = data[contaprod].get('existencia_real')
        sheet['A'+str(contador)] = clave
        sheet['B'+str(contador)] = descripcion
        sheet['C'+str(contador)] = nombre
        sheet['D'+str(contador)] = existencia 
        contador += 1 
        contaprod += 1
    wb.save(archivoe) 
    crearPdf(archivoe, archivo)       

def estadisticasCliente(id):
    data = get_estadisticaCliente(id)
    archivo = "estadisticasCliente"
    base = ruta+"\\reportes\\base\\o"+archivo+".xlsx"
    archivoe = escritorio+"\\REPORTES\\"+archivo+"-"+hoyf+".xlsx"
    # Crear Excel
    wb = load_workbook(base)
    sheet = wb.active
    cliente = data.get('cliente')
    agente = data.get('agente')
    ventaInfo = data.get('datosVenta')
    sheet['B'+str(3)] = cliente
    sheet['H'+str(3)] = agente
    contador = 6
    conta = 0
    ventaant = ""
    for i in range(len(ventaInfo)):
        vclave = ventaInfo[conta].get('vclave')
        vfecha = ventaInfo[conta].get('vfecha')
        vtotal = ventaInfo[conta].get('vtotal')
        vpago = ventaInfo[conta].get('vpago')
        pdescripcion = ventaInfo[conta].get('pdescripcion')
        pclave = ventaInfo[conta].get('pclave')
        pcantidad = ventaInfo[conta].get('pcantidad')
        pprecio = ventaInfo[conta].get('pprecio')
        pagopen = vtotal - vpago
        d0 = datetime.strptime(vfecha, "%Y-%m-%d")
        d1 = datetime.strptime(hoyf, "%d%m%Y")
        dvencidos = (d1 - d0).days
        if dvencidos < 30 : 
            dvencidos = 0
        if vclave != ventaant:
            sheet['A'+str(contador)] = vclave 
            sheet['B'+str(contador)] = vfecha 
            sheet['C'+str(contador)] = vtotal
            sheet['D'+str(contador)] = pagopen
            sheet['E'+str(contador)] = dvencidos
            sheet['F'+str(contador)] = pdescripcion
            sheet['G'+str(contador)] = pclave
            sheet['H'+str(contador)] = pcantidad
            sheet['I'+str(contador)] = pprecio
        else:
            sheet['F'+str(contador)] = pdescripcion
            sheet['G'+str(contador)] = pclave
            sheet['H'+str(contador)] = pcantidad
            sheet['I'+str(contador)] = pprecio
        ventaant = vclave
        contador += 1 
        conta += 1
    wb.save(archivoe) 
    crearPdf(archivoe, archivo)

# Crear PDF
def crearPdf(archivoe, archivo):
    try:
        pythoncom.CoInitialize()
        excel_file = win32com.client.Dispatch("Excel.Application")
        xl_sheets = excel_file.Workbooks.Open(archivoe)
        worksheets = xl_sheets.Worksheets[0]
        worksheets.ExportAsFixedFormat(0, escritorio+"\\REPORTES\\"+archivo+"-"+hoyf+".pdf")
        excel_file.quit()
    except Exception as inst:
        print("OS error: {0}".format(inst))
    return

# reportes()