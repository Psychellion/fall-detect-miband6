import subprocess
import json
import pandas as pd

# Function to send an Intent to Gadgetbridge and capture the response
def export_gadgetbridge_data():
    try:
        # Send the Intent using adb shell
        result = subprocess.run(
            ["adb", "shell", "am", "broadcast", "-a", "nodomain.freeyourgadget.gadgetbridge.daogen.GBDaoGenerator"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error sending Intent: {result.stderr}")
            return None
        
        # Extract data from Gadgetbridge export location
        result = subprocess.run(
            ["adb", "pull", "/storage/emulated/0/Gadgetbridge/Gadgetbridge.json", "."],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"Error pulling file: {result.stderr}")
            return None
        
        # Read the JSON file
        with open("Gadgetbridge.json", "r") as file:
            data = json.load(file)
        
        return data
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to convert the exported data to a pandas DataFrame
def convert_to_dataframe(data):
    if data is None:
        return None
    
    try:
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        print(f"An error occurred while converting data to DataFrame: {e}")
        return None

# Main execution
data = export_gadgetbridge_data()
if data:
    df = convert_to_dataframe(data)
    if df is not None:
        print(df.head())
    else:
        print("Failed to convert data to DataFrame")
else:
    print("Failed to export data from Gadgetbridge")
