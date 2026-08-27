import ollama

def generate_approval_note(extracted_text: str) -> str:
    prompt = f"""
You are an assistant working in a petroleum refinery (MRPL style).
Your task is to convert the given inspection findings into a formal Approval / Observation Note.

Follow this exact structure:

Title: Inspection Observation / Approval Note
Date: [Today's Date]
Reference: [Generate a simple reference number]

1. Background / Context
2. Key Findings
3. Observations
4. Recommendations
5. Conclusion

Use formal and professional language suitable for refinery documentation.
Here are the raw findings:

{extracted_text}
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


# --------- Testing with dummy text ---------
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