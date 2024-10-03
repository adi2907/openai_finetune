import pytesseract
from pdf2image import convert_from_path
from docx import Document
import os

# Function to convert PDF to Word
def pdf_to_word(pdf_path, output_word_path):
    # Step 1: Convert PDF to images
    pages = convert_from_path(pdf_path)

    # Step 2: Perform OCR on each image
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)

    # Step 3: Create a new Word document
    doc = Document()
    doc.add_paragraph(text)

    # Step 4: Save the Word document
    doc.save(output_word_path)

    print(f"Conversion complete. Word document saved as {output_word_path}")

# Directory paths
input_dir = "judgements"
output_dir = "converted"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all the PDF files in the 'judgements' directory
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(input_dir, filename)
        output_word_path = os.path.join(output_dir, filename.replace(".pdf", ".docx"))
        
        # Convert PDF to Word
        pdf_to_word(pdf_path, output_word_path)
