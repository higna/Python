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
false_path = os.path.join(file_path, 'false.csv')

# Upload CSV
logging.info("Select CSV File")
og_path = filedialog.askopenfilename(title="Select the original CSV file", filetypes=[("CSV files", "*.csv")])
logging.info("CSV File Uploaded Succesfully")

# Delete false data
og = pd.read_csv(og_path, low_memory=False)
logging.info(f"CSV File loaded {og_path}")
false = pd.read_csv(false_path, low_memory=False)
logging.info("Deleting False Data...")
if og is not None and false is not None:
    ogx = og[~og["group_begin/Farmer_regid"].isin(false["ID"])]
    ogx.to_csv(os.path.join(file_path,'ogold.csv'), index=False)
    logging.info(f"Ogstep.csv created in {file_path}")
else:
    logging.error("File empty")

