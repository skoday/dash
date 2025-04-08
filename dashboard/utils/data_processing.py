import pandas as pd
import os
import geopandas as gpd
import numpy as np

FILES_PATH = None
FILE_PATH = None
COLUMNS = [
                "Timestamp", "Unix Time", "RTC Temp", "GPS UTC Time", "GPS Date", "GPS Latitude",
                "GPS Longitude", "GPS Altitude", "GPS Satellites", "GPS HDOP", "GPS Speed (Knots)",
                "GPS Speed (Km/h)", "GPS Track Degrees", "CycleID", "Hash", "SPS30 mc 1.0", "SPS30 mc 2.5",
                "SPS30 mc 4.0", "SPS30 mc 10.0", "SPS30 nc 0.5", "SPS30 nc 1.0", "SPS30 nc 2.5",
                "SPS30 nc 4.0", "SPS30 nc 10.0", "SPS30 Particle Size", "AHT20 Temperature", "AHT20 Humidity",
                "BMP280 Temperature", "BMP280 Pressure","BMP280 Altitude"
            ]


class DataProcessing:
    def __init__(self, file_path: str = None, files_path: str = None, is_object: False = None, objects: list = None):
        self.files_path = files_path
        self.file_path = file_path
        self.original_df = None
        self.final_df = None
        self.one_file = None
        self.is_object = is_object
        self.objects = None

        if not is_object:
            if not file_path and not files_path:
                raise ValueError("You must pass in a csv file path or a directory with csv files")

            if file_path and not os.path.exists(file_path):
                raise ValueError(f"The file path '{file_path}' does not exist.")
            elif files_path and not os.path.isdir(files_path):
                raise ValueError(f"The directory path '{files_path}' does not exist or is not a directory.")
            
            if file_path:
                self.one_file = True
            elif files_path:
                self.one_file = False
        else:
            if not objects:
                raise ValueError("There are no objects available")
            else:
                self.objects = objects
            
        

    def _is_data_row(self, row) -> bool:
        """Determine if a row looks like actual data instead of headers."""
        data_count = sum(
            str(val).replace('.', '', 1).isdigit() or isinstance(val, (int, float))
            for val in row
        )
        return data_count >= len(row) * 0.7
        

    def _read_csv_file(self, source: str | object = None, is_object: bool = False) -> pd.DataFrame:
        if is_object:
            first_row = pd.read_csv(source, nrows=1, header=None)
            source.seek(0)
        else:
            first_row = pd.read_csv(source, nrows=1, header=None)

        is_data_row = self._is_data_row(first_row.iloc[0])

        if is_data_row:
            print("This file doesnt contain column names")
            df = pd.read_csv(source, header=None, names=COLUMNS, index_col=False, usecols=range(len(COLUMNS)), engine='python', encoding='latin1', sep=",")
        else:
            df = pd.read_csv(source, encoding='latin1', engine='python')

        return df
    
    def _identify_files(self) -> list:
        if self.one_file:
            return [self.file_path]
        
        csv_files = [os.path.join(self.files_path, f) for f in os.listdir(self.files_path) 
                          if f.endswith('.csv') and os.path.isfile(os.path.join(self.files_path, f))]
        
        return csv_files
    
    def read_files(self) -> None:
        if not self.is_object:
            print("Reading csv files from path...")
            csv_path_list = self._identify_files()

            df_list = []
            for path in csv_path_list:
                print("Reading: ", path,"...")
                df = self._read_csv_file(path)
                df_list.append(df)
        
        else:
            print("Reading filed from objects...")

            df_list = []
            for obj in self.objects:
                print("Reading object ", obj)
                df = self._read_csv_file(obj, is_object=True)
                df_list.append(df)

        print("Merging dataframes")
        self.original_df = pd.concat(df_list, ignore_index=True)

    def find_timestamp(self) -> str:
        columns = self.final_df.columns    
        timestamp = None

        for column in columns:
            if "timestamp" in column.lower():
                timestamp = column
                break
                
        return timestamp
    
    def find_coordinates(self) -> list:
        columns = self.original_df.columns
        lon_col, lat_col = None, None

        for col in columns:
            col_lower = col.lower()
            if 'longitude' in col_lower or 'lon' in col_lower:
                lon_col = col
            if 'latitude' in col_lower or 'lat' in col_lower:
                lat_col = col
        return [lon_col, lat_col]
    
    def find_time_columns(self, timestamp_column_name):
        columns = self.original_df.columns
        time_columns = []
        for col in columns:
            if ('time' in col.lower() and col != timestamp_column_name) or 'date' in col.lower():
                time_columns.append(col)
        return time_columns
    
    def fix_timestamp(self) -> None:
        timestamp_column = self.find_timestamp()
        if not timestamp_column:
            print("There was no timestamp column")
            return
        
        self.final_df[timestamp_column] = pd.to_datetime(self.final_df[timestamp_column], errors="coerce")
        print("Timestamp was fixed")
        return
    
    def clean_gps_coordinates(self, valid_coordinates) -> None:
        """
        Clean GPS coordinates: if coordinates are not in the valid list, set to NaN.
        valid_coordinates should be a list of valid (latitude, longitude) tuples.
        """

        coordinates = self.find_coordinates()
        if not coordinates:
            raise ValueError("No coordinates were found")
        
        lon_col, lat_col = coordinates[0], coordinates[1]

        for index, row in self.final_df.iterrows():
            lat, lon = row[lat_col], row[lon_col]
            if (lat, lon) not in valid_coordinates:
                self.final_df.at[index, lat_col] = None
                self.final_df.at[index, lon_col] = None
        print("Done")

    def remove_useless_gps_coordinates(self, threshold=10) -> list:
        """
        Function to remove useless GPS coordinates and return only valid coordinates for filtering.
        """

        coordinates = self.find_coordinates()
        if not coordinates:
            raise ValueError("No coordinates were found")
        
        lon, lat = coordinates[0], coordinates[1]


        temp_df = self.final_df.copy()
        gps_data_clean = temp_df.dropna(subset=[lat, lon])

        # Load Mexico GeoJSON (or via API)
        mexico_geojson = "mexico.json"
        mexico_states = gpd.read_file(mexico_geojson)

        # Convert gps_data_clean to a GeoDataFrame
        gdf_points = gpd.GeoDataFrame(
            gps_data_clean,
            geometry=gpd.points_from_xy(gps_data_clean[lon], gps_data_clean[lat]),
            crs="EPSG:4326"  # WGS84 coordinate system
        )

        # Verify each coordinate fits into a state
        gdf_points_with_state = gpd.sjoin(gdf_points, mexico_states, how="left", predicate="within")

        # Determine states to take into account based on a threshold
        state_counts = gdf_points_with_state["NOM_ENT"].value_counts()
        states_to_include = state_counts[state_counts > threshold].index.tolist()

        # Filter the GeoDataFrame to include only states above the threshold
        filtered_points = gdf_points_with_state[gdf_points_with_state["NOM_ENT"].isin(states_to_include)]

        # Create a list of valid coordinates (latitude, longitude) tuples
        valid_coordinates = list(zip(filtered_points[lat], filtered_points[lon]))

        print(f"Valid coordinates extracted. Valid points: {len(valid_coordinates)}.")
        return valid_coordinates
    
    def clean_big_numbers(self) -> None:
    # Identify numeric columns, excluding 'lat' and 'lon'
        numeric_cols = self.final_df.select_dtypes(include=[np.number]).columns
        coordinates = self.find_coordinates()

        cols_to_clean = [col for col in numeric_cols if col not in ['Unix Time', ['UnixTime'], coordinates[0], coordinates[1]]]

        # Set values > 2,000,000 to NaN
        self.final_df[cols_to_clean] = self.final_df[cols_to_clean].map(
            lambda x: np.nan if x > 2_000_000 else x
        )
        
        
    
    def process_data(self):
        """Main function to process the data."""

        print("Creating final df")
        self.final_df = self.original_df.copy()


        self.fix_timestamp()
        print("-----------------------------------------------------------------------------------------")
        print("Identifying useful coordinate points")
        valid_coordinates = self.remove_useless_gps_coordinates()
        print("Removing bad coordinates")
        self.clean_gps_coordinates(valid_coordinates)

        print("Removing exagerated numnbers")
        self.clean_big_numbers( )
        print("Data processing complete.")

    def get_final_csv(self, file_name:str = None, save_file: bool = False) -> pd.DataFrame:
        if save_file:
            self.final_df.to_csv(file_name, index=False)
            return self.final_df
        return self.final_df


if __name__ == "__main__":

    pipeline = DataProcessing(file_path="/home/nestor/Documents/NuevosDatos/mar24.csv")
    pipeline.read_files()
    pipeline.process_data()
    pipeline.get_final_csv()
            
