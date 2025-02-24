import base64
import io
import pandas as pd
import geopandas as gpd

def process_file(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df

def find_timestamp(columns):    
    timestamp = None
    for column in columns:
        if "timestamp" in column.lower():
            timestamp = column
            break
            
    return timestamp

def find_coordinates(columns):
    lon_col, lat_col = None, None
    for col in columns:
        col_lower = col.lower()
        if 'longitude' in col_lower or 'lon' in col_lower:
            lon_col = col
        if 'latitude' in col_lower or 'lat' in col_lower:
            lat_col = col
    return [lon_col, lat_col]

def find_time_columns(columns, timestamp_column_name):
    time_columns = []
    for col in columns:
        if ('time' in col.lower() and col != timestamp_column_name) or 'date' in col.lower():
            time_columns.append(col)
    return time_columns

def fix_timestamp(df, timestamp_column_name):
    dft = df.copy()
    # Try to convert the timestamp column to datetime
    dft[timestamp_column_name] = pd.to_datetime(dft[timestamp_column_name], errors='coerce')

    # Replace any NaT (Not a Time) with a valid zero datetime
    dft[timestamp_column_name].fillna(pd.Timestamp(0))
    
    return dft

def remove_useless_gps_coordinates(df, threshold = 10):
        gps_data_clean = df.dropna(subset=["GPS_Latitude", "GPS_Longitude"])

        # 2. Load Mexico GeoJSON (or via API)
        # Replace 'path_to_mexico_geojson' with the actual path or URL to the GeoJSON file
        mexico_geojson = "mexico.json"
        mexico_states = gpd.read_file(mexico_geojson)

        # Convert gps_data_clean to a GeoDataFrame
        gdf_points = gpd.GeoDataFrame(
            gps_data_clean,
            geometry=gpd.points_from_xy(gps_data_clean["GPS_Longitude"], gps_data_clean["GPS_Latitude"]),
            crs="EPSG:4326"  # WGS84 coordinate system
        )

        # 3. Verify each coordinate fits into a state
        gdf_points_with_state = gpd.sjoin(gdf_points, mexico_states, how="left", predicate="within")

        # 4. Determine states to take into account based on a threshold
        state_counts = gdf_points_with_state["NOM_ENT"].value_counts()
        states_to_include = state_counts[state_counts > threshold].index.tolist()

        # Filter the GeoDataFrame to include only states above the threshold
        filtered_points = gdf_points_with_state[gdf_points_with_state["NOM_ENT"].isin(states_to_include)]

        # 5. Create a new DataFrame keeping the original fields
        final_df = filtered_points.drop(columns=["geometry", "index_right", "CVEGEO", "CVE_ENT", "CVE_MUN", "COV_", "COV_ID", "AREA", "PERIMETER"])

        return final_df