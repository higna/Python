from PIL import Image
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Folder containing the images
image_folder = "images/uploads"
converted_folder = "images/converted"

# Ensure the folders exists
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
    logging.info("Image folder Created Succefully")
if not os.path.exists(converted_folder):
    os.makedirs(converted_folder)
    logging.info("Converted folder Created Succefully")

# List all image files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png") 
               or f.endswith(".gif") or f.endswith(".JPG") or f.endswith(".JPEG") or f.endswith(".PNG") or f.endswith(".GIF")]
logging.info("Found %d image files in the folder", len(image_files))

# Loop through and convert files
for file in image_files:
    # Open the image file
    image_path = os.path.join(image_folder, file)
    image = Image.open(image_path)
    # Convert the image to PDF
    pdf_path = os.path.join(converted_folder, os.path.splitext(file)[0] + ".pdf")
    image.save(pdf_path, "PDF")
    logging.info("Converted %s to PDF", file)

logging.info("Images converted successfully")
print(f"Images converted successfully into '{converted_folder}'")

