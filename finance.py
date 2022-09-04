import yfinance as yf
#import pandas as pd

data = yf.download("ARKK",
                    #start="2022-01-01",
                    #period="5wk",
                    #interval="1wk",
                    auto_adjust=True)

print(data)

dia0208 = data.loc["2022-08-02"]

print(dia0208)

primero = data.iloc[0]

print(primero)

ultimo = data.iloc[-1]

print(ultimo)

ultimo_close = data.iloc[-1]['Close']

print(ultimo_close)

ultimos_20 = data.iloc[-20:]['Close']

print('Últimos 20 cierres:')
print(ultimos_20)

este_anio = data.loc[data.index>'2022-01-01']
print('Datos de este año de ARKK')
print(este_anio)
#data.to_excel("data.xlsx")

data_galle = yf.download(['GGAL','GGAL.BA'],auto_adjust=True)['Close'].dropna()

data_galle['CCL'] = data_galle['GGAL.BA']*10/data_galle['GGAL']

print('Datos de Galicia')
print(data_galle)