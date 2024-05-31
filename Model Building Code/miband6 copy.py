import sqlite3
import pandas as pd
from datetime import datetime
import pytz

# Define the directory where the data are stored
in_dir = 'D:\GLYCELLE\THESIS FINAL OUTPUTS\System Code\Gadgetbridge.json'

# Function to read in the data
def read_gadgetbridge_data(in_dir_f, db_name_f):
    # Connect to the sqlite database
    con = sqlite3.connect(f"{in_dir_f}{db_name_f}")
    
    # Load the table with the Mi-Fit walking info
    # Select on HEART_RATE and RAW_INTENSITY to get non-missing observations
    query = '''
        SELECT * FROM MI_BAND_ACTIVITY_SAMPLE 
        WHERE HEART_RATE != -1 AND RAW_INTENSITY != -1
    '''
    raw_data_f = pd.read_sql_query(query, con)
    
    # Close the sql connection
    con.close()
    
    # Convert unix timestamp to proper datetime object
    # Make sure to set the timezone to your location!
    tz = pytz.timezone('Europe/Paris')
    raw_data_f['TIMESTAMP_CLEAN'] = pd.to_datetime(raw_data_f['TIMESTAMP'], unit='s').dt.tz_localize('UTC').dt.tz_convert(tz)
    
    # Format the date for later aggregation
    raw_data_f['hour'] = raw_data_f['TIMESTAMP_CLEAN'].dt.hour
    raw_data_f['date'] = raw_data_f['TIMESTAMP_CLEAN'].dt.strftime('%Y-%m-%d')
    
    return raw_data_f

# Load the raw data with the function
raw_data_df = read_gadgetbridge_data(in_dir, 'Gadgetbridge')