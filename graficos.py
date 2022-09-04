import yfinance as yf
#import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import scipy

data = yf.download("ARKK",
                    #start="2022-01-01",
                    #period="5wk",
                    #interval="1wk",
                    auto_adjust=True)

#Estilos
plt.style.use('dark_background')
plt.figure(figsize=(20,8))
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.title('Cotización Histórica ARKK')

plt.plot(data['Close'])

#Grafico de línea con matplotlib
plt.show()

df=data[-250:] #Ultimas 250 cotizaciones

#Gráfico de Velas con mplfinance
mpf.plot(df,type='candle',volume=True,mav=(21,50),style='mike')
mpf.show()

#Gráfico de Velas con plotly
fig= go.Figure(data=[go.Candlestick(x=df.index,open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'])])
fig.update_layout(template='plotly_dark',xaxis_title='Fecha',yaxis_title='Precio',title_text='ARKK últimos 250 días')
fig.show()

#Gráfico de Dispersión con plotly
df['Var_%']=df['Close'].pct_change()*100
fig2= go.Figure(data=[go.Scatter(x=df.index,y=df['Var_%'])])
fig2.update_layout(template='plotly_dark',xaxis_title='Fecha',yaxis_title='Retorno %',title_text='Retornos ARKK últimos 250 días')
fig2.show()

#Gráfico de Distribución de Probabilidades
fig3= ff.create_distplot([df['Var_%'].dropna()],['ARKK'],bin_size=0.2,curve_type='kde',show_rug=False,histnorm='probability',show_curve=False)
fig3.update_layout(template='plotly_dark',xaxis_title='Var %',yaxis_title='Probabilidad',title_text='Distribución de Probabilidades ARKK últimos 250 días')
fig3.show()

#Gráfico de Distribución de Probabilidades Comparativo
#Datos de SPY
dataSPY= yf.download('SPY',auto_adjust=True)
df2= dataSPY[-250:]
df2['Var_%']=df2['Close'].pct_change()*100
fig4= make_subplots(rows=1, cols=1)
#Figura superior
figsup= ff.create_distplot([df['Var_%'].dropna()],['ARKK'],bin_size=0.2,curve_type='kde',show_rug=False,colors=['dodgerblue'])
fig4.add_trace(figsup.data[0],row=1,col=1)
#Figura inferior
figinf= ff.create_distplot([df2['Var_%'].dropna()],['SPY'],bin_size=0.2,curve_type='kde',show_rug=False,colors=['red'])
fig4.add_trace(figinf.data[0],row=1,col=1)
fig4.update_layout(template='plotly_dark',title_text='Distribución Comparativa ARKK vs SPY')
fig4.show()

