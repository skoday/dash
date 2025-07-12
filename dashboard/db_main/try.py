import os
import pandas as pd
from db_connection import SessionLocal
from db_operations import DBOperations

def extract_campaign_name(file_path):
    """Extract campaign name from folder structure"""
    # Get the parent directory name (e.g., "27 de marzo 2025")
    parent_dir = os.path.basename(os.path.dirname(file_path))
    
    # Clean it up to make it database-friendly
    campaign_name = parent_dir.replace(' ', '_').replace('/', '_')
    
    return campaign_name

def load_all_sensor_data():
    """Load all mis_datos.csv files from the directory structure"""
    
    # Base directory to search
    base_dir = '/home/nestor/Downloads/Datos ordenados con README/Datos ordenados/'
    
    # Find all mis_datos.csv files recursively
    csv_files = []
    
    print("🔍 Searching for mis_datos.csv files...")
    
    for root, dirs, files in os.walk(base_dir):
        if 'mis_datos.csv' in files:
            full_path = os.path.join(root, 'mis_datos.csv')
            csv_files.append(full_path)
    
    if not csv_files:
        print("❌ No mis_datos.csv files found in the directory structure")
        return
    
    print(f"✅ Found {len(csv_files)} CSV files to process")
    
    # Create database session
    session = SessionLocal()
    db_ops = DBOperations(session)
    
    # Process each file
    success_count = 0
    error_count = 0
    
    for i, csv_file in enumerate(csv_files, 1):
        try:
            print(f"\n📂 Processing file {i}/{len(csv_files)}: {csv_file}")
            
            # Extract campaign name from folder structure
            campaign_name = extract_campaign_name(csv_file)
            print(f"📝 Campaign name: {campaign_name}")
            
            # Load CSV
            df = pd.read_csv(csv_file)
            print(f"📊 Loaded {len(df)} rows from CSV")
            
            # Insert into database
            result = db_ops.insert_df_to_db(df, campaign_name)
            print(f"✅ {result}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {csv_file}: {str(e)}")
            error_count += 1
            continue
    
    # Close session
    session.close()
    
    # Final summary
    print(f"\n🎉 BATCH LOADING COMPLETE!")
    print(f"✅ Successfully loaded: {success_count} files")
    print(f"❌ Errors: {error_count} files")
    print(f"📈 Total files processed: {len(csv_files)}")

# Run the batch loading
if __name__ == "__main__":
    load_all_sensor_data()
