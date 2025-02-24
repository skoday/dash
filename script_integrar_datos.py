import pandas as pd
import os

"""
Modificar las siguientes variables para el script
directorio: es el la ruta al directorio/folder donde se encuentran los csv para ser concatenados.
            Si es un solo archivo solo le pondra headers.
OUTPUT_FILE_NAME: Es el nombre del archivo resultante. Se guarda en el directorio raiz (Donde se ejecuto el script)
"""
directorio = "./new"
OUTPUT_FILE_NAME = 'ultimo_gps.csv'

# Definir los nombres de las columnas en orden
columnas = [
    "Timestamp_RTC", "UnixTime", "RTC_Temp_C", "GPS_UTC_Time", "GPS_Date",
    "GPS_Latitude", "GPS_Longitude", "GPS_Altitude_m", "GPS_Satellites",
    "GPS_HDOP", "GPS_SpeedKnots", "GPS_SpeedKmh", "GPS_TrackDegrees",
    "CycleID", "Hash", "SPS30_mc_1p0", "SPS30_mc_2p5", "SPS30_mc_4p0",
    "SPS30_mc_10p0", "SPS30_nc_0p5", "SPS30_nc_1p0", "SPS30_nc_2p5",
    "SPS30_nc_4p0", "SPS30_nc_10p0", "SPS30_ParticleSize",
    "AHT20_Temperature_C", "AHT20_Humidity_RH", "BMP280_Temperature_C",
    "BMP280_Pressure_Pa", "BMP280_Altitude_m"
]

# Lista para almacenar los DataFrames
dataframes = {}

# Recorre los archivos en el directorio
for archivo in os.listdir(directorio):
    if archivo.endswith(".csv"):  # Filtra solo archivos CSV
        ruta_completa = os.path.join(directorio, archivo)
        
        # Carga el CSV sin encabezados, permitiendo un número variable de columnas
        df = pd.read_csv(ruta_completa, header=None, names=columnas, engine='python')
        
        # Guarda el DataFrame con el nombre del archivo
        dataframes[archivo] = df

df_concatenado = pd.concat(dataframes, ignore_index=True)
df_concatenado.to_csv(OUTPUT_FILE_NAME, index=False)