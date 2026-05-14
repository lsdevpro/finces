import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# --- ENDPOINTS DE COMPATIBILIDAD EXTERNA ---
# Rutas base para mantener el puente con el Frontend activo sin ejecutar lógica local.

@app.route('/api/precio', methods=['GET'])
def get_precio():
    return jsonify({})

@app.route('/api/market/global', methods=['GET'])
def get_market_global():
    return jsonify({})

@app.route('/api/market/coins', methods=['GET'])
def get_market_coins():
    try:
        cg_key = os.environ.get('COINGECKO_API_KEY')
        
        # 1. Definir la configuración base obligatoria
        default_args = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": "100",
            "page": "1",
            "sparkline": "false",
            "price_change_percentage": "24h"
        }

        # 2. Capturar lo que pide el frontend y fusionarlo sobre la base
        # Los parámetros del frontend sobrescriben o complementan a los por defecto
        args = {**default_args, **request.args.to_dict()}
        
        # URL base de CoinGecko
        base_url = "https://api.coingecko.com/api/v3/coins/markets"

        headers = {}
        if cg_key:
            headers['x-cg-demo-api-key'] = cg_key

        response = requests.get(base_url, params=args, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            print(f"[API Error] CoinGecko status {response.status_code}")
            return jsonify([])
            
    except Exception as e:
        print(f"[API Exception] Error en Proxy: {e}")
        return jsonify([])

@app.route('/api/market/usdt-mxn', methods=['GET'])
def get_usdt_mxn():
    # Tipo de cambio base provisional para la interfaz
    return jsonify({"price": "20.00"})

@app.route('/api/market/fng', methods=['GET'])
def get_market_fng():
    return jsonify({})

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({})

if __name__ == '__main__':
    print("Servidor Finces Activo (Proxy CoinGecko - Bug Fixed). Escuchando en el puerto 5000...")
    app.run(debug=True, port=5000)
