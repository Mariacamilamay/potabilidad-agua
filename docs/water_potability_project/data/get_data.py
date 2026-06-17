"""
Script opcional para descargar o generar datos de potabilidad del agua.
"""
import pandas as pd
from pathlib import Path

def download_water_data():
    """Descarga o carga el dataset de potabilidad del agua."""
    data_path = Path(__file__).parent / 'water_potability.csv'
    if data_path.exists():
        print(f"✓ El archivo ya existe: {data_path}")
        df = pd.read_csv(data_path)
        print(f"Filas: {len(df)}, Columnas: {len(df.columns)}")
        return df
    else:
        print("⚠️ El archivo no existe. Por favor descarga el dataset manualmente.")
        print("URL sugerida: https://www.kaggle.com/datasets/adityakadiwal/water-potability")
        return None

if __name__ == "__main__":
    download_water_data()