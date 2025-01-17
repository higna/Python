import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

file_path = './csv'
old_path = os.path.join(file_path, 'old.csv')
new_path = os.path.join(file_path, 'new.csv')
false_path = os.path.join(file_path, 'false.csv')
output_path = os.path.join(file_path, 'check.csv') 

# Ensure the directory exists
if not os.path.exists(file_path):
    os.makedirs(file_path)

# Load the data from the CSV files
def load_data():
    try:
        old = pd.read_csv(old_path, low_memory=False)
        new = pd.read_csv(new_path, low_memory=False)
        false = pd.read_csv(false_path, low_memory=False)
        logging.info("Data loaded successfully")
        return old, new, false
    except FileNotFoundError as e:
        logging.error("File not found: %s", e)
        return None, None, None

# Remove false data using ID
def clean_new(new, false):
    if new is not None and false is not None:
        newx = new[~new["ID"].isin(false["ID"])]
        logging.info("False data removed successfully")
        newx.to_csv(os.path.join(file_path, 'newx.csv'), index=False)
        return newx
    else:
        logging.error("Data not found")
        return new

# Combine all latitude and longitude fields into one location column
def combine_location(df):
    latitude_fields = [
        "latitude",
        "agro latitude",
        "off latitude",
        "input latitude",
        "processor latitude",
        "ext latitude",
        "busdev latitude",
        "agrilog latitude",
        "mech latitude"
    ]
    longitude_fields = [
        "longitude",
        "agro longitude",
        "off longitude",
        "input longitude",
        "processor longitude",
        "ext longitude",
        "busdev longitude",
        "agrilog longitude",
        "mech longitude",
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
        df = df.drop(columns=existing_lat_fields + existing_lon_fields)

    return df

# Combine the newx and old
def ogfims(newx, old):
    # Drop ID from newx
    newx = newx.drop(columns=['ID'], errors='ignore')

    combined = pd.concat([old, newx], ignore_index=True)
    logging.info("Data Combined Successfully")
    
    return combined

# Main function to process the data
def main():
    old, new, false = load_data()

    if old is not None and new is not None and false is not None:
        logging.info(f"Old DataFrame columns: {old.columns}")
        logging.info(f"New DataFrame columns: {new.columns}")

        old = combine_location(old)
        newx = clean_new(new, false)
        newx = combine_location(newx)

        ogstep = ogfims(newx, old)
        ogstep.to_csv(os.path.join(file_path, 'ogfims.csv'), index=False)
        logging.info("ogfims.csv Created successfully")
    else:
        print("Failed to load data.")

def second():
    csv_file = "./csv/ogfims.csv"
    df = pd.read_csv(csv_file, low_memory=False)
    # Capitalize function
    def capital(value):
            if pd.isna(value):
                return value
            return value.capitalize()
    
    # Transfornm Function
    def transform(value):
        if pd.isna(value):
            return value
        return value.replace('_',' ')
    
    # Currency Function
    def currency(value):
        if pd.isna(value):
            return value
        return value.replace(' â€“ ', '-')
    
    # Adding Index
    try:
        df['Index'] = df.index
        print(df['Index'])
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # Explode columns
    explode_col = ['Category', 'Crop Cultivated', 'Livestock Reared']
    for column in explode_col:
            if column in df.columns:
                # Split the column into lists and explode into rows
                df = df.assign(**{column: df[column].str.split(r'\s+')}).explode(column)

                # Strip extra spaces in the column
                df[column] = df[column].str.strip()

                logging.info(f"Processed column '{column}' for splitting and exploding.")
            else:
                logging.warning(f"Column '{column}' not found in the DataFrame.")

    # Capitalize Columns
    capital_col = ['Education Status', 'Farming type', 'Crop Cultivated', 'Marital Status', 'Local Government Area', 'Category', 'Gender', 'Livestock Reared', 'Farming Purpose']
    for col in capital_col:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(capital).apply(transform)
            logging.info(f"Transformed column '{col}'.")
        else:
            logging.warning(f"Column '{col}' not found in the DataFrame.")

    # Currency Change
    currency_col = ['Total Expenditure', 'Total Revenue']
    for col in currency_col:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(currency)
            logging.info(f"Transformed column '{col}'.")
        else:
            logging.warning(f"Column '{col}' not found in the DataFrame.")

    # Age Range
    try:
        if "Age" not in df.columns:
            logging.error("The 'Age' column is missing from the CSV file.")
            return df
        
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        df = df.dropna(subset=['Age'])

        bins = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, float('inf')]
        labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100', '100+']

        df['Age Range'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False, include_lowest=True)
        print(df[['Age', 'Age Range']])

        logging.info("Age ranges assigned successfully.")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except pd.errors.EmptyDataError:
        logging.error("The CSV file is empty.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # Column Arrangement and Save
    order = ['Index', 'Date', 'Category', 'Age Range', 'Gender', 'Education Status', 
             'Marital Status', 'Local Government Area', 'Location', 'Farming type', 
             'Farming Purpose', 'Crop Cultivated', 'Livestock Reared', 'Crop Income', 
             'Livestock Income', 'Total Expenditure', 'Total Revenue']

    try:
        df = df[order]
        df = df.rename(columns={
            'Farming type': 'Farming Type'
        }) 
        df.to_csv(output_path, index=False)
        logging.info(f"Data saved to '{output_path}'.") 
    except KeyError as e:
        logging.error(f"One or more columns are missing: {e}")
    except Exception as e:
        logging.error(f"An error occurred during column reordering or saving: {e}")
    
    return df
if __name__ == "__main__":
    #main()
    second()
