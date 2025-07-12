from db_main.db_connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, BigInteger, Text
from sqlalchemy.dialects.postgresql import NUMERIC
from datetime import datetime

class SensorData(Base):
    __tablename__ = 'sensor_data'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Time fields
    timestamp = Column(DateTime)
    unix_time = Column(BigInteger)
    
    # Temperature and GPS basic
    rtc_temp = Column(NUMERIC(30, 15))
    gps_utc_time = Column(NUMERIC(30, 15))
    gps_date = Column(Date)
    
    # GPS coordinates and data
    gps_latitude = Column(NUMERIC(30, 15))
    gps_longitude = Column(NUMERIC(30, 15))
    gps_altitude = Column(NUMERIC(30, 15))
    gps_satellites = Column(Integer)
    gps_hdop = Column(NUMERIC(30, 15))
    gps_speed_knots = Column(NUMERIC(30, 15))
    gps_speed_kmh = Column(NUMERIC(30, 15))
    gps_track_degrees = Column(NUMERIC(30, 15))
    
    # Cycle and hash
    cycle_id = Column(String(50))
    hash = Column(String(100))
    
    # SPS30 sensor data - Mass concentration (mc)
    sps30_mc_1_0 = Column(NUMERIC(30, 15))
    sps30_mc_2_5 = Column(NUMERIC(30, 15))
    sps30_mc_4_0 = Column(NUMERIC(30, 15))
    sps30_mc_10_0 = Column(NUMERIC(30, 15))
    
    # SPS30 sensor data - Number concentration (nc)
    sps30_nc_0_5 = Column(NUMERIC(30, 15))
    sps30_nc_1_0 = Column(NUMERIC(30, 15))
    sps30_nc_2_5 = Column(NUMERIC(30, 15))
    sps30_nc_4_0 = Column(NUMERIC(30, 15))
    sps30_nc_10_0 = Column(NUMERIC(30, 15))
    
    # SPS30 particle size
    sps30_particle_size = Column(NUMERIC(30, 15))
    
    # AHT20 sensor data
    aht20_temperature = Column(NUMERIC(30, 15))
    aht20_humidity = Column(NUMERIC(30, 15))
    
    # BMP280 sensor data
    bmp280_temperature = Column(NUMERIC(30, 15))
    bmp280_pressure = Column(NUMERIC(30, 15))
    bmp280_altitude = Column(NUMERIC(30, 15))
    
    # CO level (your "Unknown" field)
    co_level = Column(NUMERIC(30, 15))
    
    # Campaign field
    campana = Column(Text)
    
    def __repr__(self):
        return f"<SensorData(id={self.id}, timestamp={self.timestamp}, campana={self.campana})>"
