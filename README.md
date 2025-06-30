# Geo-Dashboard para microdatos móviles de medio ambiente

Este es un geo-dashboard elaborado en el framework Dash de python para vizualizar cualquier tipo de datos numericos, no obstante, para lllenar todos los graficos y poder vizualizar un mapa de rutas junto con sus filtros las columnas longitud, latitud y timestamp deben existir.

Para el correcto funcionamiento el dashboard se recomienda que el archivo que se cargue tenga definidas los nombres de las columnas.

El dashboard tiene dos vertientes de funcionamiento

* Ingresar un csv con columnas definidas
* Ingresar alrchivos csv sin columnas definidas


Si las columnas no estan definidas dentro del csv cargado y se cargan varios, el dashboard supondra que se cargaron archvos cuya estructura es la siguiente:

```python
columnas = [
    "Timestamp", "Unix Time", "RTC Temp", "GPS UTC Time", "GPS Date", "GPS_Latitude",
    "GPS_Longitude", "GPS Altitude", "GPS Satellites", "GPS HDOP", "GPS Speed (Knots)",
    "GPS Speed (Km/h)", "GPS Track Degrees", "CycleID", "Hash", "SPS30 mc 1.0", "SPS30 mc 2.5",
    "SPS30 mc 4.0", "SPS30 mc 10.0", "SPS30 nc 0.5", "SPS30 nc 1.0", "SPS30 nc 2.5",
    "SPS30 nc 4.0", "SPS30 nc 10.0", "SPS30 Particle Size", "AHT20 Temperature", "AHT20 Humidity",
    "BMP280 Temperature", "BMP280 Pressure","BMP280 Altitude"
]
``` 

Esta estructura que se supone esta destinada a poder cargar los archivos crudos del sensor de datos moviles, no obstante, errores pueden existir debido a la forma en que el framework dash serializa los archivos al cargalors.

Debido a esto, para el caso del sensor movil se recomienda extraer los datos y unirlos con el notebook llamado **Unificador.ipynb** en el directorio raíz del documento.


Para uso general, para un uso general se recomienda que se carguen archivos con header ya definidos, y si se desea llenar todos los graficos y mapas, entonces las columnas, lat, lon y timestamp deben existir.



# Para ejecutar el dashboard

Antes de seguir con los pasos para ejecutar se necesita descargar y colocar el archivo mexico.json en el directorio raiz, este archivo se puede obtener en: https://drive.google.com/file/d/1Tls6ao1wZVzR11JdMqYab_zpPfbzlF2c/view?usp=sharing


Para ejecutar este dashboard tenemos dos casos:
* Ejecutarlo directamente con python localmente
* Desplegarlo con docker para su funcionamiento como proceso del sistema con acceso desde la red local (recomendado)

## Ejecutarlo con python
Se asume que se encuentra en el directorio raiz:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python dashboard/app.py
``` 

# Ejecutarlo con docker
Solo se necesita tener instalado docker y estar en el directorio raiz
```bash
docker build -t dash:latest .
docker run -p 8050:8050 -d --restart always dash:latest
``` 
El ultimo comando correra el dashboard en el baground y se reiniciara con el sistema, para acceder a el basta con usar la ip de la computadora host en el puerto 8050, es visible para toda la red.
