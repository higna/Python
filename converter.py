import pytesseract
from PIL import Image
import pandas as pd
import os

def image_to_csv(image_path, output_csv):
    # Load the image
    image = Image.open(image_path)

    # Use Tesseract to extract text
    text = pytesseract.image_to_string(image)

    # Split text into lines and words
    lines = [line.split() for line in text.splitlines() if line]

    # Create a DataFrame
    df = pd.DataFrame(lines)

    # Save to CSV
    df.to_csv(output_csv, index=False, header=False)
    print(f"CSV file saved as {output_csv}")


image_path = './'  # Replace with the path to your image
output_csv = 'output.csv'
image_to_csv(image_path, output_csv)
