import pymupdf
import pytesseract
from PIL import Image

# Open the PDF
pdf = pymupdf.open("Industrial Equipment Inspection Report.pdf")

# Store all extracted text
all_text = ""

# Process each page
for page_number, page in enumerate(pdf):

    # Convert PDF page to image
    image = page.get_pixmap()
    image_path = f"page_{page_number + 1}.png"
    image.save(image_path)

    # Open the image
    img = Image.open(image_path)

    # Extract text using Tesseract OCR
    text = pytesseract.image_to_string(img)

    # Display extracted text
    print(f"\n--- Page {page_number + 1} ---")
    print(text)

    # Store the text
    all_text += f"\n--- Page {page_number + 1} ---\n{text}"

# Close PDF
pdf.close()

# Save extracted text
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(all_text)

print("\nPDF converted and OCR completed successfully!")
print("Extracted text saved to output.txt")