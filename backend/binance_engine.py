import requests
from datetime import datetime, timezone

class BinanceEngine:
    BASE_URL = "https://api.binance.com/api/v3/klines"

    @staticmethod
    def fetch_klines(symbol, interval, start_str, end_str):
        """
        Descarga datos históricos de Binance.
        :param symbol: str, ej. 'BTCUSDT' o 'USDTMXN'
        :param interval: str, ej. '1h', '1d'
        :param start_str: str, formato 'YYYY-MM-DD HH:MM:SS'
        :param end_str: str, formato 'YYYY-MM-DD HH:MM:SS'
        :return: list de diccionarios con datos limpios
        """
        # Convertir strings de fecha a timestamps en milisegundos (UTC)
        start_ts = int(datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp() * 1000)
        end_ts = int(datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp() * 1000)

        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_ts,
            "endTime": end_ts,
            "limit": 1000  # Máximo permitido por Binance
        }

        response = requests.get(BinanceEngine.BASE_URL, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Error Binance API: {response.text}")
            
        data = response.json()
        clean_data = []
        
        for row in data:
            # Estructuramos la respuesta para que coincida con nuestra base de datos
            clean_data.append({
                "symbol": symbol,
                "timeframe": interval,
                # Convertimos el timestamp de Binance a formato datetime
                "open_time": datetime.fromtimestamp(row[0] / 1000, tz=timezone.utc).isoformat(),
                "open_price": float(row[1]),
                "high_price": float(row[2]),
                "low_price": float(row[3]),
                "close_price": float(row[4]),
                "volume": float(row[5])
            })
            
        return clean_data

# --- BLOQUE DE PRUEBA INTERNA ---
if __name__ == "__main__":
    print("Iniciando motor de prueba Binance...")
    try:
        # Prueba: Extraer 24 horas del 1 de Enero de 2025 para BTC/USDT
        datos = BinanceEngine.fetch_klines("BTCUSDT", "1h", "2025-01-01 00:00:00", "2025-01-01 23:59:59")
        print(f"Éxito: Se extrajeron {len(datos)} velas de 1 hora.")
        print("\n--- Datos de la Primera Vela (Apertura del día) ---")
        print(datos[0])
        print("\n--- Datos de la Última Vela (Cierre del día) ---")
        print(datos[-1])
    except Exception as e:
        print(f"Error en la prueba: {e}")
