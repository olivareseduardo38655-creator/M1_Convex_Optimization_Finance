import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Tuple  # <--- ESTA LINEA ES LA CLAVE DEL ERROR

# Configuración de Activos
ASSETS_TICKERS = ["SPY", "TLT", "EEM", "VNQ", "GLD"]

def download_market_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    print(f"⬇️  Descargando datos para: {tickers}...")
    try:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False, auto_adjust=True)
        
        if data.empty:
            raise ValueError("Datos vacíos.")

        # Manejo de estructura de datos según versión de yfinance
        if "Close" in data.columns:
            prices = data["Close"]
        elif "Adj Close" in data.columns:
            prices = data["Adj Close"]
        else:
            prices = data

        if prices.isnull().values.any():
            prices = prices.fillna(method="ffill").dropna()
            
        print("✅ Descarga completada.")
        return prices
    except Exception as e:
        raise ConnectionError(f"Error descarga: {e}")

def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna()

def get_financial_metrics(returns: pd.DataFrame) -> Tuple[pd.Series, pd.DataFrame]:
    expected_returns = returns.mean() * 252
    covariance_matrix = returns.cov() * 252
    return expected_returns, covariance_matrix

if __name__ == "__main__":
    # Prueba rápida
    try:
        p = download_market_data(ASSETS_TICKERS, "2020-01-01", "2023-01-01")
        r = calculate_returns(p)
        print("Datos cargados correctamente. Filas:", len(p))
        # Guardado preventivo
        try:
            p.to_csv("../data/adjusted_prices.csv")
            r.to_csv("../data/returns.csv")
        except:
            pass 
    except Exception as e:
        print(f"Error: {e}")
