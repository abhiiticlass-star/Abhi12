from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from analysis import calculate_6_layer_confluence

app = Flask(__name__)
CORS(app)

@app.route('/get-signal/<symbol>')
def get_signal(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="1m")
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        df.rename(columns={'Volume': 'vol', 'Open': 'open', 'Close': 'close', 'Low': 'low'}, inplace=True)
        result = calculate_6_layer_confluence(df)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e), "signal": "ERROR"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
