import pandas as pd
import numpy as np

def calculate_6_layer_confluence(df):
    if df.empty or len(df) < 50:
        return {"signal": "WAITING", "score": 0, "trend": "Neutral"}
    
    # EMA Calculation
    df['ema_fast'] = df['close'].ewm(span=9, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=21, adjust=False).mean()
    
    # RSI Calculation
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    last = df.iloc[-1]
    
    # 6-Layer Filters
    layer1 = last['ema_fast'] > last['ema_slow']
    layer2 = last['rsi'] < 65
    layer3 = last['close'] > last['open']
    layer4 = last['vol'] > df['vol'].rolling(20).mean().iloc[-1]
    layer5 = last['close'] > df['low'].rolling(20).min().iloc[-1]
    layer6 = last['close'] > last['ema_fast']
    
    score = sum([layer1, layer2, layer3, layer4, layer5, layer6])
    
    signal = "NONE"
    if score >= 5: signal = "CALL"
    elif score <= 1: signal = "PUT"
        
    return {"signal": signal, "score": int(score), "trend": "Bullish" if layer1 else "Bearish"}
  
