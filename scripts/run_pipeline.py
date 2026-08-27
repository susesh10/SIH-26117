import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.tools.ocr import extract_text
from app.tools.document import create_approval_note
import ollama
from datetime import datetime


def generate_approval_note(extracted_text: str) -> str:
    today = datetime.now().strftime("%d %B %Y")
    ref_no = f"INS-{datetime.now().strftime('%Y%m%d')}-001"

    prompt = f"""
You are a senior inspection engineer at a petroleum refinery (MRPL).
Convert the following raw text into a formal Inspection Observation / Approval Note.

Strictly follow this structure and do not add extra sections:

Title: Inspection Observation / Approval Note
Date: {today}
Reference: {ref_no}

1. Background / Context
(Write 2-3 lines)

2. Key Findings
(Use bullet points)

3. Observations
(Use bullet points)

4. Recommendations
(Use numbered points)

5. Conclusion
(Write 2-3 lines)

Rules:
- Use formal professional language
- Do not use markdown symbols like **, ###, etc.
- Do not repeat Date or Title
- Keep it concise and useful for management approval

Raw text:
{extracted_text}
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

def run_pipeline(file_path: str):
    print("\n========== Starting Pipeline ==========\n")

    # Step 1: OCR
    print("1. Extracting text using OCR...")
    extracted_text = extract_text(file_path)
    
    if extracted_text.startswith("Error"):
        print(extracted_text)
        return

    print("\n----- Extracted Text -----\n")
    print(extracted_text[:1000])  # print only first 1000 characters
    print("\n--------------------------\n")

    # Step 2: Generate Approval Note using Local Model
    print("2. Generating Approval Note using local model...")
    approval_note = generate_approval_note(extracted_text)

    print("\n----- Generated Approval Note -----\n")
    print(approval_note)
    print("\n-----------------------------------\n")

    # Step 3: Create Word Document
    print("3. Creating Word document...")
    output_path = create_approval_note(approval_note)

    print(f"\n✅ Success! Word file saved at:\n{output_path}")
    print("\n========== Pipeline Completed ==========\n")


if __name__ == "__main__":
    # Change this path to your sample document
    sample_file = "data/sample_docs/Safety_SOP.pdf"   # ← Change this
    
    if not os.path.exists(sample_file):
        print(f"Sample file not found: {sample_file}")
        print("Please put a sample PDF or Image in data/sample_docs/ and update the path.")
    else:
        run_pipeline(sample_file)
