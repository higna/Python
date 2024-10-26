import pandas as pd
import os

# Folder paths
folder_path = "./"
master_file_path = "./.gitignore/master.csv"
processed_file_path = "./.gitignore/processed.csv"

# Clear the existing processed.csv file if it exists
if os.path.exists(processed_file_path):
    # Overwrite with an empty DataFrame to clear all rows and columns
    pd.DataFrame().to_csv(processed_file_path, index=False)

data_sample = pd.read_csv(master_file_path)
print("Available columns in master.csv:", data_sample.columns.tolist())

# Load specified columns from master CSV
columns_to_import = [
    "field_no", 
    "organization", 
    "city_field", 
    "state", 
    "_sec1_coordinates_latitude", 
    "_sec1_coordinates_longitude", 
    "Year_of_production", 
    "var_name", 
    "grp_field/sec2_area", 
    "grp_field/sec2_area_unit", 
    "sec1_seedpurpose"
]
data = pd.read_csv(master_file_path, usecols=columns_to_import)

# Concatenation
data["Location"] = data["_sec1_coordinates_latitude"].astype(str) + "," + data["_sec1_coordinates_longitude"].astype(str)

# Rename columns
column_renames = {
    "field_no": "Field Id",
    "organization": "Organization",
    "city_field": "City",
    "state": "State",
    "_sec1_coordinates_latitude": "Latitude",
    "_sec1_coordinates_longitude": "Longitude",
    "Year_of_production": "Prod Year",
    "var_name": "Variety",
    "sec1_seedpurpose": "Seed Class",
    "grp_field/sec2_area": "Area",
    "grp_field/sec2_area_unit": "Area Unit" 
}
data = data.rename(columns=column_renames)

# Remove empty spaces from specified columns
columns_to_trim = ["Organization", "City", "State", "Variety", "Seed Class"]
for column in columns_to_trim:
    data[column] = data[column].str.strip()

# Capitalize the first letter of each word in the 'State' column
columns_to_capitalize = ["State", "City"]
for column in columns_to_capitalize:
    data[column] = data[column].str.title()

# Extract the first word from the Organization column and create a new column
data["Organization Modified"] = data["Organization"].str.split().str[0]

# Rename variables in the Seed Class column
seed_class_renames = {
    "Commercial_seed": "Certified Seed",
    "breeder": "Breeder Seed",
    "Foundation": "Foundation Seed"
}

# Replace values in the Seed Class column
data["Seed Class"] = data["Seed Class"].replace(seed_class_renames)

# Rename Varieties
def modify_variety(variety):
    if variety in ["NR8082", "NR87184", "TMS 01/1371", "TMS-IBA010040", "TMS-IBA011368", "TMS-IBA011412", "TMS-IBA070539", "TMS-IBA30572", "TMS-IBA9702205", "TMS-IBA980510", "TMS-IBA980581"]:
        return "Others"  # New name for specific varieties
    elif variety == "Farmers_Pride":
        return "Farmer's Pride"  
    elif variety == "Obasanjo_2":
        return "Obasanjo 2"  
    elif variety == "Baba70":
        return "Baba 70"  
    else:
        return variety  # Retain old name

# Create the new 'Variety Modified' column
data["Variety Modified"] = data["Variety"].apply(modify_variety)

# Save processed data to the processed file
data.to_csv(processed_file_path, index=False)

print("Data processing and concatenation complete. Processed data saved to 'processed.csv'.")
