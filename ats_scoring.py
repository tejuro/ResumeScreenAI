import subprocess
import sys

# Function to install missing packages
def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"⚠ {package} is missing. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install spaCy if missing
install_package("spacy")

import spacy
nlp = spacy.load("en_core_web_sm")  # Load NLP model after installation

import os
import spacy
import re
import fitz  # PyMuPDF

import sys
sys.path.append(r"C:\Users\Tejaswini.S\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages")

import spacy



nlp = spacy.load("en_core_web_sm")


# Function to get the latest uploaded resume
def get_latest_resume(directory="uploads"):
    pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]
    if not pdf_files:
        return None
    latest_file = max(pdf_files, key=lambda f: os.path.getctime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        return f"⚠ Error: File '{pdf_path}' not found!"

    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text("text") + "\n"
        return text.strip()


# Function to clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text


# Function to extract keywords from Job Description
def extract_keywords(jd_text):
    doc = nlp(jd_text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return list(set(keywords))  # Remove duplicates


# Function to calculate ATS Score
def calculate_ats_score(resume_text, jd_text):
    resume_text = clean_text(resume_text)
    jd_keywords = extract_keywords(jd_text)

    # Match keywords
    matched_keywords = [word for word in jd_keywords if word in resume_text]
    keyword_match_score = (len(matched_keywords) / len(jd_keywords)) * 100 if jd_keywords else 0

    # Resume structure check (Presence of key sections)
    sections = ["education", "experience", "skills", "projects", "certifications"]
    structure_score = sum(1 for section in sections if section in resume_text) / len(sections) * 100

    # Final ATS Score (Weighted calculation)
    final_score = (keyword_match_score * 0.6) + (structure_score * 0.4)

    return round(final_score, 2)


# Run ATS Scoring with the latest resume
if __name__ == "__main__":
    resume_path = get_latest_resume()

    if resume_path:
        print(f"🔹 Processing latest resume: {resume_path}")
        resume_text = extract_text_from_pdf(resume_path)

        # Example Job Description
        job_description = """We are looking for a Python Developer with experience in Machine Learning, SQL, and Web Development using Flask or Django."""

        ats_score = calculate_ats_score(resume_text, job_description)
        print(f"ATS Score for {resume_path}: {ats_score}%")
    else:
        print("No PDF files found in 'uploads/'!")
