from openai import OpenAI

client = OpenAI()

# Read the OCR text
with open("extracted_text.txt", "r", encoding="utf-8") as file:
    ocr_text = file.read()

# Ask AI to correct OCR mistakes
prompt = f"""
Correct the OCR errors in this industrial equipment inspection report.

Rules:
1. Correct spelling and OCR mistakes.
2. Do not change the meaning.
3. Do not invent any information.
4. Keep all names, dates, numbers, measurements, machine IDs, and technical details unchanged.
5. Keep the original report structure.

OCR TEXT:
{ocr_text}
"""

response = client.responses.create(
    model="gpt-5",
    input=prompt
)

corrected_text = response.output_text

# Save corrected report
with open("corrected_report.txt", "w", encoding="utf-8") as file:
    file.write(corrected_text)

print("AI correction completed successfully!")
print("Corrected report saved to corrected_report.txt")