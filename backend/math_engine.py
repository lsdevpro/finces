import os
from dotenv import load_dotenv
from supabase import create_client, Client
from collections import defaultdict
from datetime import datetime

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class MathEngine:
    @staticmethod
    def process_daily_extremes(symbol, fiat_symbol, year, month):
        """
        Extrae los datos de la bóveda, cruza el token con la moneda nacional,
        y agrupa los datos por día extrayendo máximos, mínimos y sus horas exactas.
        """
        # 1. Extraer datos del Token (ej. BTCUSDT)
        token_data = supabase.table('historical_klines') \
            .select('*') \
            .eq('symbol', symbol) \
            .gte('open_time', f"{year}-{month:02d}-01T00:00:00+00:00") \
            .lte('open_time', f"{year}-{month:02d}-31T23:59:59+00:00") \
            .execute()
            
        # 2. Extraer datos de la Moneda Nacional (ej. USDTMXN)
        fiat_data = supabase.table('historical_klines') \
            .select('*') \
            .eq('symbol', fiat_symbol) \
            .gte('open_time', f"{year}-{month:02d}-01T00:00:00+00:00") \
            .lte('open_time', f"{year}-{month:02d}-31T23:59:59+00:00") \
            .execute()

        if not token_data.data or not fiat_data.data:
            return {"error": "Faltan datos en la bóveda para este mes."}

        # 3. Crear un diccionario rápido para el tipo de cambio por hora
        fiat_map = {row['open_time']: row['close_price'] for row in fiat_data.data}

        daily_summary = defaultdict(lambda: {
            'max_price_mxn': 0, 'max_time': None,
            'min_price_mxn': float('inf'), 'min_time': None
        })

        # 4. Procesar hora por hora y agrupar por día
        for row in token_data.data:
            hour_str = row['open_time']
            day_str = hour_str.split('T')[0] # Extraer solo la fecha (YYYY-MM-DD)
            
            # Si no hay tipo de cambio exacto para esa hora, usamos 1 (o podríamos manejar el error)
            tasa_mxn = fiat_map.get(hour_str, 1) 
            
            # Fórmula: Valor_USDT * Tasa_USDT/MXN
            high_mxn = row['high_price'] * tasa_mxn
            low_mxn = row['low_price'] * tasa_mxn

            # Evaluar el Máximo del día
            if high_mxn > daily_summary[day_str]['max_price_mxn']:
                daily_summary[day_str]['max_price_mxn'] = high_mxn
                daily_summary[day_str]['max_time'] = hour_str
                
            # Evaluar el Mínimo del día
            if low_mxn < daily_summary[day_str]['min_price_mxn']:
                daily_summary[day_str]['min_price_mxn'] = low_mxn
                daily_summary[day_str]['min_time'] = hour_str

        return dict(daily_summary)

# --- BLOQUE DE PRUEBA ---
if __name__ == "__main__":
    print("Iniciando Motor Matemático...")
    resultados = MathEngine.process_daily_extremes("BTCUSDT", "USDTMXN", 2025, 1)
    
    print("\n--- Análisis del 1 de Enero de 2025 ---")
    dia_1 = resultados.get("2025-01-01")
    if dia_1:
        print(f"Máximo en MXN: ${dia_1['max_price_mxn']:,.2f} (Ocurrió a las: {dia_1['max_time']})")
        print(f"Mínimo en MXN: ${dia_1['min_price_mxn']:,.2f} (Ocurrió a las: {dia_1['min_time']})")
