import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

def extract_text_from_image(image_path: str) -> str:
    """Extract text from a single image using Tesseract"""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF by converting pages to images"""
    pages = convert_from_path(pdf_path, dpi=200)
    
    all_text = []
    for i, page in enumerate(pages):
        temp_image = f"temp_page_{i}.jpg"
        page.save(temp_image, "JPEG")
        
        text = extract_text_from_image(temp_image)
        all_text.append(f"\n--- Page {i+1} ---\n{text}")
        
        if os.path.exists(temp_image):
            os.remove(temp_image)
    
    return "\n".join(all_text)


def extract_text(file_path: str) -> str:
    """
    Main function - automatically detects if file is image or PDF
    """
    if not os.path.exists(file_path):
        return "Error: File not found."

    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        return extract_text_from_image(file_path)
    
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    
    else:
        return "Error: Unsupported file format. Please use Image or PDF."