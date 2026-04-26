from flask import Flask, jsonify, request
from flask_cors import CORS
from data_manager import DataManager
from math_engine import MathEngine
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/precio', methods=['GET'])
def get_precio():
    try:
        # Recibimos la moneda solicitada o usamos bitcoin por defecto
        moneda = request.args.get('moneda', 'bitcoin')
        api_key = os.getenv('COINGECKO_API_KEY')
        
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={moneda}&vs_currencies=usd'
        
        headers = {"accept": "application/json"}
        if api_key:
            headers["x-cg-demo-api-key"] = api_key
            
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        datos = response.json()
        
        # Extraemos dinámicamente el valor
        if moneda in datos and 'usd' in datos[moneda]:
            precio = datos[moneda]['usd']
            return jsonify({'moneda': moneda, 'precio': precio})
        else:
            return jsonify({'error': 'Moneda no encontrada en CoinGecko'}), 404
            
    except Exception as e:
        print(f"Error en servidor: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        'supabaseUrl': os.getenv('SUPABASE_URL'),
        'supabaseAnonKey': os.getenv('SUPABASE_KEY')
    })

@app.route('/api/analysis/monthly', methods=['POST'])
def analyze_monthly_data():
    try:
        # 1. Recibir las instrucciones de la pantalla
        payload = request.json
        symbol = payload.get('symbol', 'BTCUSDT')
        fiat_symbol = payload.get('fiat_symbol', 'USDTMXN')
        year = int(payload.get('year', 2025))
        month = int(payload.get('month', 1))

        # 2. Sincronizar la Bóveda (Asegurar que los datos existan)
        DataManager.get_or_fetch_month(symbol, year, month)
        DataManager.get_or_fetch_month(fiat_symbol, year, month)

        # 3. Encender el Motor Matemático y cruzar los datos
        analysis_results = MathEngine.process_daily_extremes(symbol, fiat_symbol, year, month)

        # 4. Devolver la inteligencia empaquetada a la pantalla
        return jsonify({
            "status": "success",
            "symbol": symbol,
            "fiat": fiat_symbol,
            "period": f"{year}-{month:02d}",
            "data": analysis_results
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Servidor Finces Iniciado. Escuchando en el puerto 5000...")
    app.run(debug=True, port=5000)
