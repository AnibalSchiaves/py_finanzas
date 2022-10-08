import numpy as np
import yfinance as yf
import math
import pandas as pd
from datetime import date, datetime
from medias import ma_estrategy, ema_estrategy
pd.options.mode.chained_assignment = None  # default='warn'

def get_stock_data(ticker,fecha_inicio,fecha_fin,intervalo):
    df = yf.download(tickers=ticker,start=fecha_inicio,end=fecha_fin,interval=intervalo,auto_adjust=True)
    df['date'] = df.index
    return df

def seniales_compra_venta(df,ticker,fecha_inicio,fecha_fin,suffix):
    ganancia = 0
    position = 'position_'+suffix
    for i, row in df.iterrows():
        if df.loc[i,position] == 1:
            precio_compra = round(df.loc[i,'comprar'],2)
            fecha_compra = df.loc[i,'date']
        if df.loc[i,position] == -1:
            precio_venta = round(df.loc[i,'vender'],2)
            fecha_venta = df.loc[i,'date']
            if precio_venta>precio_compra:
                resultado = 'Trade Ganador'
            else:
                resultado = 'Trade Perdedor'
            diferencia = precio_venta - precio_compra
            #print('{}{:^17}{}{:^17}{:^17}'.format(fecha_compra,precio_compra,fecha_venta,precio_venta,resultado))
    return df

def test_inversion(df,ticker,fecha_inicio,fecha_fin,capital_inicial,porc_comision,truncar_activos,suffix):
    # assumptions:
    capital_inicial = int(capital_inicial)
    ganancia = 0 
    ganancia_total = 0
    position = 0
    total_ganancia = 0 
    cant_activos = 0
    balance = capital_inicial
    precio_compra = 0 # per share 
    total_compra = 0
    total_venta = 0 
    #MA_wealth = initial_wealth # moving average wealth
    #LT_wealth = initial_wealth # long-term wealth
    venta_inicial = 0 
    position = 'position_'+suffix
    position_int = 0
    df[position].iloc[-1] = -1

    result = []

    #print('-'*100)
    #print('{:^15}{:^10}{:^15}{:^20}{:^20}{:^10}{:^20}{:^20}{:^20}{:^20}'.format('Fec Compra','Pre Compra($)','Fec Venta','Ven Precio($)','Inversion($)','Cant Act','Tot Compra','Tot Venta','Ganancia','Balance')) #,'MA_wealth'
    #print('-'*100)

    for i,row in df.iterrows():
        if position_int == 0:
            if df.loc[i,position] == 1:
                capital_inicial = balance
                precio_compra =round( df.loc[i,'Close'],2)
                fec_compra = df.loc[i,'date']
                cant_activos = balance / precio_compra
                if truncar_activos:
                    cant_activos = math.trunc(cant_activos)
                total_compra = round(precio_compra * cant_activos,2)
                comision_compra = round(total_compra * porc_comision,2)
                balance = balance - total_compra - comision_compra
                position_int = 1
            #else:
        elif position_int == 1:
            if df.loc[i,position] == -1:
                precio_venta = round(df.loc[i,'Close'],2)
                fec_venta = df.loc[i,'date']
                total_venta = round(precio_venta * cant_activos,2)
                comision_venta = round(total_venta * porc_comision,2)
                ganancia = round(total_venta - total_compra,2)
                ganancia_desp_comi = ganancia - comision_venta - comision_compra
                porc_ganancia = round((ganancia_desp_comi / capital_inicial)*100,2)
                ganancia_total = round(ganancia_total + ganancia,2)
                balance = balance + total_venta - comision_venta
                #sell_balance = round(balance + total_profit,2)
                #MA_wealth = round(balance + total_sell_p,2)
                #balance = round(balance,2)
                nro = i
                
                #print('{}{:^15}{}{:^15}{:^15}{:^15}{:^20}{:^20}{:^10}{:^15}'.format(fec_compra,precio_compra,fec_venta,precio_venta,capital_inicial,cant_activos,total_compra,total_venta,ganancia,balance ))#,MA_wealth
                result.append({'Fec Compra':fec_compra,'Pre Compra($)':precio_compra,'Fec Venta':fec_venta,'Ven Precio($)':precio_venta,'Inversion($)':capital_inicial,'Cant Act':cant_activos,'Tot Compra':total_compra,'Comi Compra':comision_compra,'Tot Venta':total_venta,'Comi Venta':comision_venta,'Ganancia($)':ganancia,'Gan - Comi':ganancia_desp_comi,'Ganacia(%)':porc_ganancia,'Balance':balance})
                #sell_balance = balance + total_sell_p
                position_int = 0
            #else:

    return pd.DataFrame(result)

def print_resultados(df,ticker,fecha_inicio,fecha_fin,capital_inicial,dias,titulo):
    print('Stock: {}'.format(ticker))
    print('Period: {} - {}'.format(fecha_inicio, fecha_fin))
    print('Capital Inicial: {}'.format(capital_inicial))
    print('Trading {}:'.format(titulo))
    print('-'*100)
    print(df)
    print('-'*100)
    capital_final = round(df.iloc[-1]['Balance'],2)
    print('Capital Final: {}'.format(capital_final))
    ganancia_total = round(capital_final-capital_inicial,2)
    print('Ganancia Neta($): {}'.format(ganancia_total))
    porc_ganancia = round(ganancia_total / capital_inicial * 100,2)
    print('Ganancia Neta(%): {}'.format(porc_ganancia))
    porc_ganancia_anual = round(porc_ganancia/dias*365,2)
    print('Ganancia Anual(%): {}'.format(porc_ganancia_anual))


larga_MA = 20
corta_MA = 5
titulo = 'estrategia EMA larga {} días contra EMA corta {} días'.format(larga_MA, corta_MA)
capital_inicial = 1000
ticker = 'PAMP.BA'
truncar_activos = True
#ticker = 'BTC-USD' 
#truncar_activos = False
fecha_inicio = '2022-01-01'
date_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
fecha_fin = '2022-09-30'
date_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
dias = (date_fin - date_inicio).days

intervalo = '1d'
ganancia_total = 0
porc_comision = 0.005

df = get_stock_data(ticker,fecha_inicio,fecha_fin,intervalo)
suffix = 'EMA_20_vs_10'
df = ema_estrategy(df,corta_MA,larga_MA,suffix)
#df = seniales_compra_venta(df,ticker,fecha_inicio,fecha_fin,suffix)
rdf = test_inversion(df,ticker,fecha_inicio,fecha_fin,capital_inicial,porc_comision,truncar_activos,suffix)
print_resultados(rdf,ticker,fecha_inicio,fecha_fin,capital_inicial,dias,titulo)
