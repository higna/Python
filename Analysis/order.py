import os
import shutil
import logging
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize Tinker
root = tk.Tk()
root.withdraw()

# Paths
file_path = './csv/'
old_path = os.path.join(file_path, 'old.csv')
new_path = os.path.join(file_path, 'new.csv')
combined_path = os.path.join(file_path, 'ogstep.csv')
false_path = os.path.join(file_path, 'false.csv')

# Main execution
def main():
    try:
        logging.info("Select Old and New CSV File")
        old_csv = filedialog.askopenfilename(title="Select the Old CSV file", filetypes=[("CSV files", "*.csv")])
        new_csv = filedialog.askopenfilename(title="Select the New CSV file", filetypes=[("CSV files", "*.csv")])
        logging.info("CSV Files Uploaded Succesfully")

        # Compare CSV
        old_df = pd.read_csv(old_csv)
        new_df = pd.read_csv(new_csv)
        false_df = pd.read_csv(false_path)
        logging.info("CSV File Loaded Succesfully")

        # Delete False Data
        def delete_false(new_df, false_df):
            return new_df[~new_df["group_begin/Farmer_regid"].isin(false_df["ID"])]
        logging.info("Deleting False Data...")
        new_df = delete_false(new_df, false_df)
        logging.info("False Data Deleted")
        new_df.to_csv(new_path, index=False)
        old_df.to_csv(old_path, index=False)
        logging.info("CSV Files Saved Succesfully")
        # Combine all latitude and longitude fields into one location column
        def combine_location(df):
            latitude_fields = [
                "group_Farmer/group_geographic/_GPS_latitude",
                "group_Agro_Marketer/_Agro_GPS_latitude",
                "group_offtaker/_offtaker_GPS_latitude",
                "group_inputdealer/_inputdealer_GPS_latitude",
                "group_processor/_processor_GPS_latitude",
                "group_extension/_extension_GPS_latitude",
                "group_busdev/_busdev_GPS_latitude",
                "group_agrilogistic/_agrilogisic_GPS_latitude",
                "group_mechanization/_mechanization_GPS_latitude"
            ]
            longitude_fields = [
                "group_Farmer/group_geographic/_GPS_longitude",
                "group_Agro_Marketer/_Agro_GPS_longitude",
                "group_offtaker/_offtaker_GPS_longitude",
                "group_inputdealer/_inputdealer_GPS_longitude",
                "group_processor/_processor_GPS_longitude",
                "group_extension/_extension_GPS_longitude",
                "group_busdev/_busdev_GPS_longitude",
                "group_agrilogistic/_agrilogisic_GPS_longitude",
                "group_mechanization/_mechanization_GPS_longitude",
            ]

            # Ensure the columns exist in the dataframe before attempting to combine
            existing_lat_fields = [field for field in latitude_fields if field in df.columns]
            existing_lon_fields = [field for field in longitude_fields if field in df.columns]

            logging.info(f"Existing latitude fields: {existing_lat_fields}")
            logging.info(f"Existing longitude fields: {existing_lon_fields}")

            if not existing_lat_fields or not existing_lon_fields:
                logging.warning("No latitude or longitude fields found in the dataset.")
                df["location"] = None
            else:
                # Combine columns, prioritizing non-null values
                df.loc[:, 'latitude'] = df[existing_lat_fields].bfill(axis=1).iloc[:, 0]
                df.loc[:, 'longitude'] = df[existing_lon_fields].bfill(axis=1).iloc[:, 0]

                logging.info(f"DataFrame columns after combining: {df.columns}")

                # Ensure the combined columns exist before creating the Location field
                if 'latitude' in df.columns and 'longitude' in df.columns:
                    df['Location'] = df['latitude'].astype(str) + ',' + df['longitude'].astype(str)
                    logging.info("Location field created successfully")
                else:
                    logging.error("Combined latitude or longitude column not found")

                # Drop the original latitude and longitude fields
                df = df.drop(columns = existing_lat_fields + existing_lon_fields)

            return df
        old_df = combine_location(old_df)
        new_df = combine_location(new_df)
        # Rename Columns
        old_df = old_df.rename(columns={
            "group_enum/Date_of_collection": "Date",
            "primary_category": "Category", "group_fild/group_biography/Age": "Age", "group_fild/group_biography/Sex": "Gender",
            "group_fild/group_biography/Education_Status": "Education Status", "group_fild/group_biography/Marital_Status" : "Marital Status",
            "group_fild/group_biography/Household_Size": "Household Size", "group_fild/group_contact/group_address/LGA_origin": "Local Government Area",
            "group_Farmer/group_income/group_enterprise_crops/Farm_size_under_cultivation": "Crop farm size", "group_Farmer/group_geographic/Data_collection_location": "Collection location",
            "group_Farmer/group_income/Type_of_Farming":"Farming Type", "group_Farmer/group_income/Primary_purpose_of_farming" : "Farming Purpose", 
            "group_Farmer/group_income/group_enterprise_crops/Are_you_producing_seed": "Seed Production",
            "group_Farmer/group_income/group_enterprise_livestocks/Total_farmsize_livestock": "Livestock farm size",
            "group_Farmer/group_income/group_enterprise_livestocks/Select_types_of_livestoc_farming": "Livestock Reared",
            "group_Farmer/group_income/group_enterprise_crops/Select_Crops_being_farmed": "Crop Cultivated",
            "group_Farmer/group_farmincome/Crops_income": "Crop Income", "group_Farmer/group_farmincome/Livestock_income": "Livestock Income",
            "group_Farmer/group_income/Farmland_ownership": "Farmland Ownership", "group_Farmer/group_benefits/Access_to_Government_land_for_farming": "Access to Government Land",
            "group_coopmember/Membership":"Cooperative Membership", "group_tools/info_medium": "Information Medium", "group_tools/proficiency" : "Proficiency",
            "group_Farmer/group_farmincome/Total_revenue": "Total Revenue", "group_Farmer/group_farmincome/Total_Expenditure": "Total Expenditure"
            })
                    
        new_df = new_df.rename(columns={
            "group_enum/Date_of_collection": "Date",
            "primary_category": "Category", "group_fild/group_biography/Age": "Age", "group_fild/group_biography/Sex": "Gender",
            "group_fild/group_biography/Education_Status": "Education Status", "group_fild/group_biography/Marital_Status" : "Marital Status",
            "group_fild/group_biography/Household_Size": "Household Size", "group_fild/group_contact/group_address/LGA_origin": "Local Government Area",
            "group_Farmer/group_income/group_enterprise_crops/Total_farmsize_crops": "Crop farm size", "group_Farmer/group_geographic/Data_collection_location": "Collection location",
            "group_Farmer/group_income/Type_of_Farming": "Farming Type", "group_Farmer/group_income/Primary_purpose_of_farming" : "Farming Purpose",
            "group_Farmer/group_income/group_enterprise_crops/Are_you_producing_seed": "Seed Production",
            "group_Farmer/group_income/group_enterprise_livestocks/Total_farmsize_livestock":"Livestock farm size",
            "group_Farmer/group_income/group_enterprise_livestocks/Select_types_of_livestoc_farming":"Livestock Reared",
            "group_Farmer/group_income/group_enterprise_crops/Select_Crops_being_farmed":"Crop Cultivated",
            "group_Farmer/group_farmincome/Crops_income": "Crop Income", "group_Farmer/group_farmincome/Livestock_income": "Livestock Income",
            "group_Farmer/group_income/Farmland_ownership": "Farmland Ownership", "group_Farmer/group_benefits/Access_to_Government_land_for_farming": "Access to Government Land",
            "group_coopmember/Membership":"Cooperative Membership", "group_tools/info_medium": "Information Medium", "group_tools/proficiency" : "Proficiency",
            "group_Farmer/group_farmincome/Total_revenue": "Total Revenue", "group_Farmer/group_farmincome/Total_Expenditure": "Total Expenditure"
            })
        
        order = ["Date","Category", "Age", "Gender", "Education Status", "Marital Status", "Household Size", "Local Government Area",
                 "Location", "Collection location", "Farming Type","Farming Purpose", "Crop Cultivated", "Livestock Reared", "Seed Production", "Farming Type", 
                 "Farming Purpose", "Crop Income", "Livestock Income", "Farmland Ownership", "Access to Government Land", "Cooperative Membership",
                 "Information Medium", "Proficiency", "Livestock farm size", "Crop farm size", "Total Revenue", "Total Expenditure"]
        old_df = old_df[order]
        new_df = new_df[order]
        new_df.to_csv(new_path, index=False)
        old_df.to_csv(old_path, index=False)
        logging.info("CSV Files Saved Succesfully")

        combined = pd.concat([old_df, new_df], ignore_index=True)
        combined.to_csv(combined_path, index=False)
        logging.info(f"Combined CSV Files to {combined_path}")
    except Exception as e:
        logging.error(f"Error Uploading CSV File: {e}")

# Execute main
if __name__=="__main__":
    main()