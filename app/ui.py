import gradio as gr
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.tools.ocr import extract_text
from app.tools.document import create_approval_note
import ollama


def generate_approval_note(extracted_text: str) -> str:
    today = datetime.now().strftime("%d %B %Y")
    ref_no = f"INS-{datetime.now().strftime('%Y%m%d')}-001"

    prompt = f"""
You are a senior inspection engineer at a petroleum refinery (MRPL).
Convert the following raw text into a formal Inspection Observation / Approval Note.

Strictly follow this structure:

Title: Inspection Observation / Approval Note
Date: {today}
Reference: {ref_no}

1. Background / Context
2. Key Findings
3. Observations
4. Recommendations
5. Conclusion

Rules:
- Use formal professional language
- Do not use markdown symbols like **, ###, etc.
- Keep it concise

Raw text:
{extracted_text}
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


def process_document(file):
    if file is None:
        return "Please upload a file.", None, None

    file_path = file.name

    # Step 1: OCR
    extracted_text = extract_text(file_path)
    if extracted_text.startswith("Error"):
        return extracted_text, None, None

    # Step 2: Generate Approval Note
    approval_note = generate_approval_note(extracted_text)

    # Step 3: Create Word File
    word_path = create_approval_note(approval_note)

    return extracted_text, approval_note, word_path


# ---------- Gradio Interface ----------
with gr.Blocks(title="SIH26117 - Sovereign AI Workbench", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🛢️ SIH26117 – Sovereign AI Workbench
    ### Fully Offline Inspection → Approval Note Generator
    **Motto:** Sovereign AI for Confidential Work — Nothing Leaves the Premises
    """)

    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload Scanned Document (PDF or Image)", file_types=[".pdf", ".png", ".jpg", ".jpeg"])
            submit_btn = gr.Button("Generate Approval Note", variant="primary")

        with gr.Column():
            status = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        extracted_output = gr.Textbox(label="Extracted Text (OCR)", lines=10)
        note_output = gr.Textbox(label="Generated Approval Note", lines=15)

    word_output = gr.File(label="Download Word File")

    submit_btn.click(
        fn=process_document,
        inputs=file_input,
        outputs=[extracted_output, note_output, word_output]
    )

    gr.Markdown("---\n**Note:** This system runs completely offline using local open-weight models.")

# Run the app
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
