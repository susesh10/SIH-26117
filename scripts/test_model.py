import ollama
from datetime import datetime

def generate_approval_note(extracted_text: str) -> str:
    today = datetime.now().strftime("%d %B %Y")

    prompt = f"""
You are an assistant working in a petroleum refinery (MRPL style).
Convert the given inspection findings into a formal Approval / Observation Note.

Follow this exact structure:

Title: Inspection Observation / Approval Note
Date: {today}
Reference: INS-{datetime.now().strftime("%Y%m%d")}-001

1. Background / Context
2. Key Findings
3. Observations
4. Recommendations
5. Conclusion

Use formal and professional language suitable for refinery documentation.

Raw findings:
{extracted_text}
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    dummy_findings = """
    During routine inspection of Heat Exchanger HE-204 in CDU unit, 
    slight leakage was observed near the channel head flange. 
    Bolts were found loose. No major corrosion noticed. 
    Thickness measurement is within acceptable limits. 
    Recommended to tighten the bolts and monitor for 48 hours.
    """

    note = generate_approval_note(dummy_findings)
    print(note)