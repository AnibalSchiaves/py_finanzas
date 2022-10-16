from core import get_stock_data, test_inversion, print_resumen
from medias import ema_estrategy
from datetime import date, datetime
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def get_resumen_trading(ticker,fecha_inicio,fecha_fin,intervalo,capital_inicial,porc_comision,truncar_activos,corta_MA_inicio, corta_MA_fin, larga_MA_inicio, larga_MA_fin):
    resumen = []
    for larga_MA in range(larga_MA_inicio,larga_MA_fin+1):
        for corta_MA in range(corta_MA_inicio, corta_MA_fin):
            df = get_stock_data(ticker,fecha_inicio,fecha_fin,intervalo)
            suffix = 'EMA'
            df = ema_estrategy(df,corta_MA,larga_MA,suffix)
            rdf = test_inversion(df,ticker,fecha_inicio,fecha_fin,capital_inicial,porc_comision,truncar_activos,suffix)
            cant_trading = 0
            trades_exito = 0
            capital_final = 0
            for i,row in rdf.iterrows():
                cant_trading = cant_trading + 1
                if row['Ganancia($)']>0:
                    trades_exito = trades_exito + 1
            capital_final = round(rdf.iloc[-1]['Balance'],2)
            ganancia = round(capital_final-capital_inicial,2)
            porc_ganancia = round(ganancia / capital_inicial * 100,2)
            porc_ganancia_anual = round(porc_ganancia/dias*365,2)
            titulo = 'Estrategia corta EMA {} larga EMA {}'.format(corta_MA, larga_MA)
            resumen.append({'Estrategia':titulo,'Cant Trades':cant_trading,'Trades Exitos':trades_exito,'Cap Inicial':capital_inicial,'Cap Final':capital_final,'Ganancia($)':ganancia,'Ganancia(%)':porc_ganancia,'Ganancia Anual(%)':porc_ganancia_anual})
    dfres = pd.DataFrame(resumen).sort_values('Ganancia($)', ascending=False)
    return dfres

capital_inicial = 1000
#ticker = 'GGAL.BA'
#truncar_activos = True
ticker = 'BTC-USD' 
truncar_activos = False
fecha_inicio = '2020-10-01'
date_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
fecha_fin = '2022-09-30'
date_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
dias = (date_fin - date_inicio).days
intervalo = '1d'
porc_comision = 0.005
corta_MA_inicio = 1
corta_MA_fin = 10
larga_MA_inicio = 18
larga_MA_fin = 25

df = get_resumen_trading(ticker,fecha_inicio,fecha_fin,intervalo,capital_inicial,porc_comision,truncar_activos,corta_MA_inicio, corta_MA_fin, larga_MA_inicio, larga_MA_fin)
print_resumen(df,ticker,fecha_inicio,fecha_fin)




