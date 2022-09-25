import numpy as np

panel_lider = ['GGAL','BMA','YPFD','ALUA','CEPU','BBAR']
print(panel_lider)
print(type(panel_lider))

panel_lider.append('COME')
print(panel_lider)

print(panel_lider[1:4])

panel_lider.sort()
print(panel_lider)

ggal = float(input('Ingrese el valor de Galicia: '))

if ggal>200.0:
    print('Galicia está caro')
else:
    print('Galicia está barato')

panel_lider_tupla = ('GGAL','BMA','YPFD','ALUA','CEPU','BBAR')
try:
    panel_lider_tupla[0]='ALUA'
except:
    print('ocurrió una excepción porque las tuplas son inmutables')

cotizaciones = {'GGAL':257.6, 'BMA':488.55, 'YPFD': 1961.75}
print(cotizaciones.keys())
print(cotizaciones.values())
print(f'La cotización de GGAL es {cotizaciones["GGAL"]}')
print(f'La cotización de BMA es {cotizaciones.get("BMA")}')

if cotizaciones['GGAL']>cotizaciones['BMA']:
    print('Galicia está mas cara que Banco Macro')
elif cotizaciones['GGAL']==cotizaciones['BMA']:
    print('Galicia y Banco Macro tienen la misma cotización')
else:
    print('Banco Macro está más cara que Galicia')

print(np.arange(10.0,20.0,0.5))

accion='ALUA'
if accion is not list(cotizaciones.keys()):
    print('no tengo la cotización de Aluar')



