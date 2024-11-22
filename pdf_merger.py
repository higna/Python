from PyPDF2 import PdfMerger

# List of PDF files to merge
pdf_files = ["file1.pdf", "file2.pdf", "file3.pdf"]

# Initialize the PdfMerger
merger = PdfMerger()

# Loop through and append files
for pdf in pdf_files:
    merger.append(pdf)

# Write to a new PDF file
merger.write("merged.pdf")
merger.close()

print("PDFs merged successfully into 'merged.pdf'")