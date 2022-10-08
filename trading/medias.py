import numpy as np
import yfinance as yf
import math
import pandas as pd
from datetime import date, datetime
pd.options.mode.chained_assignment = None  # default='warn'

def ma_estrategy(df,corta_MA,larga_MA,suffix):
    df['corta_MA'] = df['Close'].rolling(int(corta_MA)).mean()
    df['larga_MA'] = df['Close'].rolling(int(larga_MA)).mean()
    cruces = 'cruces_'+suffix
    df[cruces]   = np.where(df['corta_MA']>df['larga_MA'],1.0,0.0)
    position = 'position_'+suffix
    df[position] = df[cruces].diff()
    df[position].iloc[-1] = -1
    for i, row in df.iterrows():
        if df.loc[i,position] == 1:
            precio_compra = round(df.loc[i,'Close'],2)
            df.loc[i,'comprar'] = precio_compra
        if df.loc[i,position] == -1:
            precio_venta = round(df.loc[i,'Close'],2)
            df.loc[i,'vender'] = precio_venta
    return df

def ema_estrategy(df,corta_MA,larga_MA,suffix):
    df['corta_MA'] = df['Close'].ewm(span=int(corta_MA)).mean()
    df['larga_MA'] = df['Close'].ewm(span=int(larga_MA)).mean()
    cruces = 'cruces_'+suffix
    df[cruces]   = np.where(df['corta_MA']>df['larga_MA'],1.0,0.0)
    position = 'position_'+suffix
    df[position] = df[cruces].diff()
    df[position].iloc[-1] = -1
    for i, row in df.iterrows():
        if df.loc[i,position] == 1:
            precio_compra = round(df.loc[i,'Close'],2)
            df.loc[i,'comprar'] = precio_compra
        if df.loc[i,position] == -1:
            precio_venta = round(df.loc[i,'Close'],2)
            df.loc[i,'vender'] = precio_venta
    return df

