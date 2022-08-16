from pkgutil import get_data
from pydoc import cli
from openpyxl import load_workbook, Workbook
import win32com.client
#from win32com.client import Dispatch
from .db import get_agente, get_productos, get_estadisticaCliente, get_saldoCliente, get_compPago
import os
import pythoncom
import winshell
from datetime import date, datetime, timedelta

escritorio = winshell.desktop()
hoy = date.today()
hoyf = hoy.strftime("%d%m%Y")
ruta = os.getcwd()

def catalogoAgentes():
    data = get_agente()
    archivo = "catalogoAgentes"
    base = ruta+"\\reportes\\base\\o"+archivo+".xlsx"
    archivor = escritorio+"\\REPORTES\\"+archivo+"-"+hoyf
    archivoe = archivor+".xlsx"
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
    crearPdf(archivor, archivo) 

def catalogoProductos():
    data = get_productos()
    archivo = "catalogoProductos"
    base = ruta+"\\reportes\\base\\o"+archivo+".xlsx"
    archivor = escritorio+"\\REPORTES\\"+archivo+"-"+hoyf
    archivoe = archivor+".xlsx"
    # Crear Excel
    wb = load_workbook(base)
    sheet = wb.active
    contador = 5
    for i in range(len(data)):
        clave = data[i].get('nom_corto')
        descripcion = data[i].get('descripcion')
        nombre = data[i].get('nombre')
        existencia = data[i].get('existencia_real')
        sheet['A'+str(contador)] = clave
        sheet['B'+str(contador)] = descripcion
        sheet['C'+str(contador)] = nombre
        sheet['D'+str(contador)] = existencia 
        contador += 1 
    wb.save(archivoe) 
    crearPdf(archivor, archivo)       

def estadisticasCliente(id):
    data = get_estadisticaCliente(id)
    archivo = "estadisticasCliente"
    base = ruta+"\\reportes\\base\\o"+archivo+".xlsx"
    archivor = escritorio+"\\REPORTES\\"+archivo+"-"+hoyf
    archivoe = archivor+".xlsx"
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
        else : 
            dvencidos = dvencidos - 30
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
    crearPdf(archivor, archivo)

def saldosCliente():
    data = get_saldoCliente()
    archivo = "saldoDeudorCliente"
    archivor = escritorio+"\\REPORTES\\"+archivo+"-"+hoyf
    base = ruta+"\\reportes\\base\\o"+archivo+".xlsx"
    archivoe = archivor+".xlsx"
    # Crear Excel
    wb = load_workbook(base)
    sheet = wb.active
    contador = 5
    for i in range(len(data)):
        cliente = data[i].get('cliente')
        compra = data[i].get('idVenta')
        fecha = data[i].get('fecha')
        pagado = data[i].get('montoPagado')
        apagar = data[i].get('totalPagar')
        ppendiente = apagar - pagado
        d0 = datetime.strptime(fecha, "%Y-%m-%d")
        d1 = datetime.strptime(hoyf, "%d%m%Y")
        dvencidos = (d1 - d0).days
        if dvencidos < 30 : 
            dvencidos = 0
        else : 
            dvencidos = dvencidos - 30
        sheet['A'+str(contador)] = cliente 
        sheet['B'+str(contador)] = compra 
        sheet['C'+str(contador)] = fecha
        sheet['D'+str(contador)] = apagar
        sheet['E'+str(contador)] = pagado
        sheet['F'+str(contador)] = ppendiente
        sheet['G'+str(contador)] = dvencidos
        contador += 1 
    wb.save(archivoe) 
    crearPdf(archivor, archivo)

def comprobantePago(idVenta):
    data = get_compPago(idVenta)
    archivo = "comprobantePago"
    base = ruta+"\\reportes\\base\\o"+archivo+".xlsx"
    cliente = data.get('cliente')
    agente = data.get('agente')
    vfecha = data.get('vfecha')
    vtotal = data.get('vtotal')
    vpagado = data.get('vpagado')
    historial = data.get('historial')
    fecha = datetime.strptime(vfecha, "%Y-%m-%d")
    flimite = fecha + timedelta(days=30)
    # Crear Excel
    archivor = escritorio+"\\REPORTES\\"+archivo+idVenta+"-"+hoyf
    archivoe = archivor+".xlsx"
    wb = load_workbook(base)
    sheet = wb.active
    sheet['B'+str(6)] = cliente
    sheet['B'+str(7)] = agente
    sheet['F'+str(6)] = idVenta
    sheet['F'+str(7)] = fecha.strftime("%d/%m/%Y")
    sheet['F'+str(8)] = flimite
    sheet['F'+str(9)] = vtotal
    sheet['F'+str(10)] = vpagado
    filae = 13
    for i in range(len(historial)):
        fechap = historial[i].get('fecha')
        fechaf = datetime.strptime(vfecha, "%Y-%m-%d")
        montop = historial[i].get('monto')
        sheet['A'+str(filae)] = fechaf.strftime("%d/%m/%Y")
        sheet['B'+str(filae)] = montop
        filae += 1
    wb.save(archivoe) 
    crearPdf(archivor, archivo)  

# Crear PDF
def crearPdf(archivor, archivo):
    try:
        pythoncom.CoInitialize()
        excel_file = win32com.client.Dispatch("Excel.Application")
        xl_sheets = excel_file.Workbooks.Open(archivor+".xlsx")
        worksheets = xl_sheets.Worksheets[0]
        worksheets.ExportAsFixedFormat(0, archivor+".pdf")
        excel_file.quit()
    except Exception as inst:
        print("OS error: {0}".format(inst))
    return
