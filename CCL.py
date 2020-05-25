import pandas as pd
from Reuters import Reuters


datos4principales = [['GGAL.BA','GGAL.N',10,'Grupo Financiero Galicia'],['YPFD.BA','YPF.N',1,'YPF'],
                     ['PAMP.BA','PAM.N',25,'Pampa Energía'],['BMA.BA','BMA.N',10,'Banco Macro']]
datos = [['GGAL.BA','GGAL.N',10,'Grupo Financiero Galicia'],['YPFD.BA','YPF.N',1,'YPF'],
         ['PAMP.BA','PAM.N',25,'Pampa Energía'],['BMA.BA','BMA.N',10,'Banco Macro'],
         ['BBAR.BA','BBAR.N',3,'BBVA Banco Frances'],
         ['CEPU.BA','CEPU.N',10,'Central Puerto'],['CRES.BA','CRESY.N',10,'Cresud'],
         ['EDN.BA','EDN.N',20,'Edenor'],['TGSU2.BA','TGS.N',5,'Transp. de Gas del Sur'],
         ['PAMP.BA','PAM.N',25,'Pampa Energia'],['SUPV.BA','SUPV.N',5,'Supervielle'],
         ['TECO2.BA','TEO.N',5,'Telecom Argentina'],['IRSA.BA','IRS.N',10,'Irsa']]
valoresAcciones = {} 
#1- Calcular promedio CCL -se calcula con los 4 principales-
         
def calcularCCL(data):
    preciosCCL = {}
    for simbolo in data:
        try:
            ccLiqui = float(Reuters(simbolo[0]).getPrice()) / (float(Reuters(simbolo[1]).getPrice()) / simbolo[2])
            preciosCCL[simbolo[3]] = ccLiqui
        except:
            print('error dato')
    
    return preciosCCL

def cclPromedio(preciosCCL):
    valor = 0
    for item in preciosCCL.values():
        valor += item
    print ("DOLAR CONTADO CON LIQUI= " + str(valor / len(preciosCCL)) + " -Se utiliza para el calculo el promedio de los 4 ADR con mas volumen. GGAL,PAMPA,YPF y MACRO")
    return valor/len(preciosCCL)

#2- Calculo del valor arbitrado de cada adr
    
def valorArbitrado(cclPromedio):
    valorAccionArbitrado={}    
    for simbolo in datos:
        valorAccionArbitrado[simbolo[3]] = float(Reuters(simbolo[1]).getPrice()) / simbolo[2] * cclPromedio
    return valorAccionArbitrado

#3- Comparamos el valor arbitrado(obtenido en 2) con el valor de cierre en Argentina:


def valorAcciones () :   
    for simbolo in datos:
        try:         
            valoresAcciones[simbolo[3]] =  float(Reuters(simbolo[0]).getPrice())
        except:
            print('No se logro obtener el precio de ' + simbolo[0])
    

def diferencias(valoresArbitrados): #comparar 2 con accion y guardarlo en un diccionario
    diferencia = {}
    for simbolo in valoresArbitrados.items() :
        try:
            diferencia[simbolo[0]]=  valoresAcciones[simbolo[0]] - simbolo[1]
        except:
            print("error")
    return diferencia

def calcularDifPorcentual(precioArbitrado,diferencia):
    porcentaje = {}
    for item in precioArbitrado:
        porcentaje[item]= diferencia[item] / precioArbitrado[item] * 100
    return porcentaje

def tabla(preciosArbitrados,cclxAccion,diferencia,porcentaje):
    df1 = pd.DataFrame({'CCL Accion':list(cclxAccion.values()),        
                        'Cotizacion Accion': list(valoresAcciones.values()),
                        'Precio Arbitrado':list(preciosArbitrados.values()),
                        'Diferencia':list(diferencia.values()),
                        '%':list(porcentaje.values())
                       },
                       index = valoresAcciones.keys())
    return df1
   

def iniciar():
    CCL = calcularCCL(datos4principales)
    promedioCCL = cclPromedio(CCL)
    valorArbitradoADR = valorArbitrado(promedioCCL)
    valorAcciones()
    cclxAccion = calcularCCL(datos)
    difPrecio = diferencias(valorArbitradoADR)    
    porcentajes = calcularDifPorcentual(valorArbitradoADR,difPrecio)
    df = tabla(valorArbitradoADR,cclxAccion,difPrecio,porcentajes)    
    return df

iniciar()

