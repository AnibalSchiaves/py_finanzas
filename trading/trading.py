import numpy as np
import yfinance as yf
import math
import pandas as pd
from datetime import date, datetime
from core import get_stock_data, test_inversion, print_resultados
from medias import ma_estrategy, ema_estrategy
pd.options.mode.chained_assignment = None  # default='warn'


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
