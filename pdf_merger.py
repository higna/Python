from PyPDF2 import PdfMerger
import os

# Folder containing the PDF files
pdf_folder = "pdf_files"

# List all PDF files in the folder
pdf_files = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.endswith(".pdf")]

# Initialize the PdfMerger
merger = PdfMerger()

# Loop through and append files
for pdf in pdf_files:
    merger.append(pdf)

# Write to a new PDF file
output_file = "merged.pdf"
merger.write(output_file)
merger.close()

print(f"PDFs merged successfully into '{output_file}'")
