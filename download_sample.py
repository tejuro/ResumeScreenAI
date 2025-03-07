import requests
import os

# Ensure uploads folder exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# URL of a working sample resume
resume_url = "https://www.jobscan.co/sample-resume.pdf"
response = requests.get(resume_url)

# Save the resume
resume_path = "uploads/sample_resume.pdf"
with open(resume_path, "wb") as file:
    file.write(response.content)

print(f"Sample resume saved at: {resume_path}")
