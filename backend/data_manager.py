import os
import calendar
from dotenv import load_dotenv
from supabase import create_client, Client
from binance_engine import BinanceEngine

load_dotenv()

# Conexión independiente a la Bóveda para este módulo
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class DataManager:
    @staticmethod
    def get_or_fetch_month(symbol, year, month):
        """
        Verifica si el mes ya está en Supabase. Si no, lo descarga de Binance y lo guarda.
        """
        # Calcular el último día del mes solicitado
        _, last_day = calendar.monthrange(year, month)
        start_str = f"{year}-{month:02d}-01 00:00:00"
        end_str = f"{year}-{month:02d}-{last_day:02d} 23:59:59"

        print(f"\n[{symbol}] Verificando bóveda para {year}-{month:02d}...")
        
        # 1. Consultar si ya hay datos guardados para evitar gasto de red
        response = supabase.table('historical_klines') \
            .select('id') \
            .eq('symbol', symbol) \
            .eq('timeframe', '1h') \
            .gte('open_time', f"{year}-{month:02d}-01T00:00:00+00:00") \
            .lte('open_time', f"{year}-{month:02d}-{last_day:02d}T23:59:59+00:00") \
            .limit(1) \
            .execute()

        if len(response.data) > 0:
            print(f"[{symbol}] ÉXITO: Los datos ya existen en Supabase. Extracción omitida.")
            return True

        print(f"[{symbol}] Datos no encontrados. Descargando mes completo de Binance...")
        
        # 2. Si la bóveda está vacía para ese mes, descargar de Binance
        try:
            klines = BinanceEngine.fetch_klines(symbol, "1h", start_str, end_str)
            
            if klines:
                print(f"[{symbol}] Guardando {len(klines)} velas en la bóveda de forma permanente...")
                # 3. Guardar en Supabase (upsert previene duplicados)
                supabase.table('historical_klines').upsert(klines).execute()
                print(f"[{symbol}] Guardado exitoso.")
                return True
            else:
                print(f"[{symbol}] No se encontraron datos en Binance para este periodo.")
                return False
        except Exception as e:
            print(f"[{symbol}] Error durante la sincronización: {e}")
            return False

# --- BLOQUE DE PRUEBA DEL GESTOR ---
if __name__ == "__main__":
    print("Iniciando prueba de sincronización de Bóveda...")
    # Sincronizamos Enero 2025 para nuestro Token base y para Moneda Nacional
    DataManager.get_or_fetch_month("BTCUSDT", 2025, 1)
    DataManager.get_or_fetch_month("USDTMXN", 2025, 1)
