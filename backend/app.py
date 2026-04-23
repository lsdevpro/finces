from flask import Flask, jsonify, request
from flask_cors import CORS
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)
