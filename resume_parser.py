import os
import fitz  # PyMuPDF

# Get the latest uploaded resume
uploads_folder = "uploads"
resume_files = [f for f in os.listdir(uploads_folder) if f.endswith(".pdf")]

if resume_files:
    latest_resume = os.path.join(uploads_folder, resume_files[-1])  # Pick the last uploaded file
    print(f"Processing: {latest_resume}")

    def extract_text_from_pdf(pdf_path):
        try:
            with fitz.open(pdf_path) as pdf:
                text = ""
                for page in pdf:
                    text += page.get_text("text") + "\n"
                return text.strip()
        except Exception as e:
            return f"Error reading PDF: {e}"

    pdf_text = extract_text_from_pdf(latest_resume)
    print("Extracted Resume Text:\n", pdf_text)
else:
    print("No resume files found in uploads/")
