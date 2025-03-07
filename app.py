from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from ats_scoring import extract_text_from_pdf, calculate_ats_score
from eligibility_check import check_eligibility
from save_results import save_to_excel
from email_service import send_email

app = Flask(__name__, template_folder="templates")
app.config["UPLOAD_FOLDER"] = "uploads"

# Ensure upload folder exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# API to Process Resume & Job Description
@app.route("/process", methods=["POST"])
def process_resume():
    if "resume" not in request.files or "job_desc" not in request.form:
        return jsonify({"message": "Resume and Job Description are required"}), 400

    resume_file = request.files["resume"]
    job_desc_text = request.form["job_desc"]  # Get job description from text input

    # Save uploaded resume
    resume_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(resume_file.filename))
    resume_file.save(resume_path)

    # Extract text from resume
    resume_text = extract_text_from_pdf(resume_path)

    # Calculate ATS Score based on entered Job Description
    ats_score = calculate_ats_score(resume_text, job_desc_text)

    # Get additional user inputs
    cgpa = float(request.form.get("cgpa", 0))
    email = request.form.get("email", "")
    name = request.form.get("name","")
    if not name:
        name = "Unknown"

        print(f" Debug: Received Name = '{name}'")
        # Check eligibility
    eligibility_status = check_eligibility(cgpa, ats_score)

    # Save results in Excel
    candidate_data = {
        "Name": name,  # Include Name
        "Email": email,
        "CGPA": cgpa,
        "ATS Score": ats_score,
        "Eligibility": eligibility_status
    }

    save_to_excel(candidate_data)

    # Send email to user
    subject = "Shortlisted!" if eligibility_status == "Eligible" else "Application Update"
    body = f"Dear Candidate,\n\nYour application has been processed.\nCGPA: {cgpa}\nATS Score: {ats_score}%\nStatus: {eligibility_status}\n\nBest Regards,\nHR Team"
    send_email(email, subject, body)

    return jsonify({"message": "Processing complete", "ATS Score": ats_score, "Eligibility": eligibility_status})

if __name__ == "__main__":
    app.run(debug=True)
