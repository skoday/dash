import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from db_main.db_model import SensorData
from typing import List

class DBOperations:
    def __init__(self, db_session: Session):
        self.db = db_session

    def _clean_integer_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean integer fields to prevent overflow - now with proper NaT handling"""
        df_clean = df.copy()
        
        # Clean unix_time - PostgreSQL BIGINT max is ~9.22e18
        BIGINT_MAX = 9223372036854775807
        if 'Unix Time' in df_clean.columns:
            df_clean.loc[df_clean['Unix Time'] > BIGINT_MAX, 'Unix Time'] = None
            df_clean['Unix Time'] = pd.to_numeric(df_clean['Unix Time'], errors='coerce')
        
        # GPS Satellites - your existing solution that works
        if 'GPS Satellites' in df_clean.columns:
            df_clean['GPS Satellites'] = pd.to_numeric(df_clean['GPS Satellites'], errors='coerce')
            df_clean.loc[df_clean['GPS Satellites'] > 1000000, 'GPS Satellites'] = 0
            df_clean.loc[df_clean['GPS Satellites'] < 0, 'GPS Satellites'] = 0
            df_clean['GPS Satellites'] = df_clean['GPS Satellites'].fillna(0)
        
        # GPS HDOP - your existing code
        if 'GPS HDOP' in df_clean.columns:
            df_clean['GPS HDOP'] = pd.to_numeric(df_clean['GPS HDOP'], errors='coerce')
            df_clean.loc[df_clean['GPS HDOP'] > 1000000, 'GPS HDOP'] = None
            df_clean.loc[df_clean['GPS HDOP'] < 0, 'GPS HDOP'] = None
        
        # GPS Date - convert strings to proper dates or None
        if 'GPS Date' in df_clean.columns:
            df_clean['GPS Date'] = pd.to_datetime(df_clean['GPS Date'], errors='coerce')
            # Convert to date objects for the DATE field in PostgreSQL
            df_clean['GPS Date'] = df_clean['GPS Date'].dt.date
        
        #GPS Track Degrees
        if 'GPS Track Degrees' in df_clean.columns:
            df_clean['GPS Track Degrees'] = pd.to_numeric(df_clean['GPS Track Degrees'], errors='coerce')

        # GPS UTC Time - convert strings to numbers or None
        if 'GPS UTC Time' in df_clean.columns:
            df_clean['GPS UTC Time'] = pd.to_numeric(df_clean['GPS UTC Time'], errors='coerce')
        
        return df_clean

    def insert_df_to_db(self, df: pd.DataFrame, campana: str) -> str:
        """Insert DataFrame into database with proper NaT handling"""
        
        # STEP 1: Clean the data first
        df_clean = self._clean_integer_fields(df)
        
        # STEP 2: Handle missing CO column (your existing code)
        if 'Unknown' not in df_clean.columns and 'co_level' not in df_clean.columns:
            df_clean['co_level'] = None
        elif 'Unknown' in df_clean.columns:
            df_clean['co_level'] = df_clean['Unknown']
        
        # STEP 3: Add campaign column
        df_clean['campana'] = campana
        
        # STEP 4: Convert DataFrame rows to SensorData objects
        records = []
        for _, row in df_clean.iterrows():
            
            # Handle timestamp properly - convert NaT to None
            timestamp_value = row.get('Timestamp')
            if pd.isna(timestamp_value):
                timestamp_value = None
            else:
                timestamp_value = pd.to_datetime(timestamp_value, errors='coerce')
                if pd.isna(timestamp_value):  # If conversion failed, set to None
                    timestamp_value = None
            
            # Handle GPS Date properly - convert NaT to None
            gps_date_value = row.get('GPS Date')
            if pd.isna(gps_date_value):
                gps_date_value = None
            
            record = SensorData(
                timestamp=timestamp_value,  # Now properly handles NaT
                unix_time=row.get('Unix Time'),
                rtc_temp=row.get('RTC Temp'),
                gps_utc_time=row.get('GPS UTC Time'),
                gps_date=gps_date_value,  # Now properly handles NaT
                gps_latitude=row.get('GPS_Latitude'),
                gps_longitude=row.get('GPS_Longitude'),
                gps_altitude=row.get('GPS Altitude'),
                gps_satellites=row.get('GPS Satellites'),
                gps_hdop=row.get('GPS HDOP'),
                gps_speed_knots=row.get('GPS Speed (Knots)'),
                gps_speed_kmh=row.get('GPS Speed (Km/h)'),
                gps_track_degrees=row.get('GPS Track Degrees'),
                cycle_id=row.get('CycleID'),
                hash=row.get('Hash'),
                sps30_mc_1_0=row.get('SPS30 mc 1.0'),
                sps30_mc_2_5=row.get('SPS30 mc 2.5'),
                sps30_mc_4_0=row.get('SPS30 mc 4.0'),
                sps30_mc_10_0=row.get('SPS30 mc 10.0'),
                sps30_nc_0_5=row.get('SPS30 nc 0.5'),
                sps30_nc_1_0=row.get('SPS30 nc 1.0'),
                sps30_nc_2_5=row.get('SPS30 nc 2.5'),
                sps30_nc_4_0=row.get('SPS30 nc 4.0'),
                sps30_nc_10_0=row.get('SPS30 nc 10.0'),
                sps30_particle_size=row.get('SPS30 Particle Size'),
                aht20_temperature=row.get('AHT20 Temperature'),
                aht20_humidity=row.get('AHT20 Humidity'),
                bmp280_temperature=row.get('BMP280 Temperature'),
                bmp280_pressure=row.get('BMP280 Pressure'),
                bmp280_altitude=row.get('BMP280 Altitude'),
                co_level=row.get('co_level'),
                campana=campana
            )
            records.append(record)
        
        # STEP 5: Bulk insert
        self.db.bulk_save_objects(records)
        self.db.commit()
        
        return f"✅ Inserted {len(records)} records for campaign '{campana}'"


    def get_all_campaigns(self) -> List[str]:
        """Get all distinct campaign names from database"""
        campaigns = self.db.query(SensorData.campana).distinct().all()
        campaign_list = [c[0] for c in campaigns if c[0] is not None]
        return sorted(campaign_list)

    def get_data_by_campaign(self, campana: str) -> pd.DataFrame:
        """Get all data for a specific campaign as DataFrame"""
        rows = self.db.query(SensorData).filter(SensorData.campana == campana).all()
        
        if not rows:
            return pd.DataFrame()
        
        # Convert to DataFrame (same as before)
        data = []
        for row in rows:
            row_dict = {
                'id': row.id,
                'timestamp': row.timestamp,
                'unix_time': row.unix_time,
                'rtc_temp': row.rtc_temp,
                'gps_utc_time': row.gps_utc_time,
                'gps_date': row.gps_date,
                'gps_latitude': row.gps_latitude,
                'gps_longitude': row.gps_longitude,
                'gps_altitude': row.gps_altitude,
                'gps_satellites': row.gps_satellites,
                'gps_hdop': row.gps_hdop,
                'gps_speed_knots': row.gps_speed_knots,
                'gps_speed_kmh': row.gps_speed_kmh,
                'gps_track_degrees': row.gps_track_degrees,
                'cycle_id': row.cycle_id,
                'hash': row.hash,
                'sps30_mc_1_0': row.sps30_mc_1_0,
                'sps30_mc_2_5': row.sps30_mc_2_5,
                'sps30_mc_4_0': row.sps30_mc_4_0,
                'sps30_mc_10_0': row.sps30_mc_10_0,
                'sps30_nc_0_5': row.sps30_nc_0_5,
                'sps30_nc_1_0': row.sps30_nc_1_0,
                'sps30_nc_2_5': row.sps30_nc_2_5,
                'sps30_nc_4_0': row.sps30_nc_4_0,
                'sps30_nc_10_0': row.sps30_nc_10_0,
                'sps30_particle_size': row.sps30_particle_size,
                'aht20_temperature': row.aht20_temperature,
                'aht20_humidity': row.aht20_humidity,
                'bmp280_temperature': row.bmp280_temperature,
                'bmp280_pressure': row.bmp280_pressure,
                'bmp280_altitude': row.bmp280_altitude,
                'co_level': row.co_level,
                'campana': row.campana
            }
            data.append(row_dict)
        
        return pd.DataFrame(data)

    def delete_campaign(self, campana: str) -> str:
        """
        Delete all records for a specific campaign
        Returns confirmation of deletion
        """
        try:
            # First, check if the campaign exists and count records
            record_count = self.db.query(SensorData).filter(SensorData.campana == campana).count()
            
            if record_count == 0:
                return f"❌ Campaign '{campana}' not found or already empty"
            
            # Delete all records for this campaign
            deleted_count = self.db.query(SensorData).filter(SensorData.campana == campana).delete(synchronize_session=False)
            
            # Commit the transaction
            self.db.commit()
            
            return f"🗑️ Deleted {deleted_count} records from campaign '{campana}'"
            
        except Exception as e:
            # Rollback in case of error
            self.db.rollback()
            return f"❌ Error deleting campaign '{campana}': {str(e)}"
