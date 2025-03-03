from PIL import Image
import pytesseract
import os
import tkinter as tk
from tkinter import filedialog
import shutil
import pandas as pd
import logging

# Logging Initialization
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Tinker Initialization
root = tk.Tk()
root.withdraw()

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Paths
img_path = "./Attachments/Upload/"
save_path = "./Attachments/Extracted/"
if not img_path: 
    os.makedirs()

# Select Image 
file_path = filedialog.askopenfilename(title="Upload Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
logging.info("File Uploaded Succesfully")

# Upload image to folder
uploaded_file =  os.path.join(img_path, os.path.basename(file_path))
shutil.copy(file_path, uploaded_file)

# Load image
image = Image.open(uploaded_file)

# Extract text
text = pytesseract.image_to_string(image)
logging.info("Converting to Text...")

# Save to CSV
csv_path = os.path.join(save_path, "extracted.csv")

with open(csv_path, "w", newline='') as file:
    file.write("Extracted\n")
    file.write(text)
logging.info("File saved to: " + csv_path)