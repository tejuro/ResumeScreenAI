import os
import pandas as pd

# Function to save results in an Excel sheet
def save_to_excel(candidate_data, filename="results.xlsx"):
    # Check if the file already exists
    if os.path.exists(filename):
        df = pd.read_excel(filename)  # Read existing data
        df = pd.concat([df, pd.DataFrame([candidate_data])], ignore_index=True)  # Append new data
    else:
        df = pd.DataFrame([candidate_data])  # Create a new file if it doesn't exist

    df.to_excel(filename, index=False, engine="openpyxl")  # Save to Excel
    print(f"✅ Results saved to {filename}")

# Test saving data
if __name__ == "__main__":
    sample_data = {
        "Name": "John Doe",
        "Email": "john.doe@example.com",
        "Phone": "+1234567890",
        "CGPA": 8.2,
        "ATS Score": 75.5,
        "Eligibility": "Eligible"
    }
    save_to_excel(sample_data)
def check_eligibility(cgpa, ats_score, cgpa_threshold=7.0, ats_threshold=50.0):
    """
    Checks if a candidate meets eligibility criteria.

    Parameters:
    - cgpa (float): Candidate's CGPA
    - ats_score (float): AI-generated ATS Score
    - cgpa_threshold (float): Minimum CGPA required (default: 7.0)
    - ats_threshold (float): Minimum ATS Score required (default: 70.0)

    Returns:
    - str: '✅ Eligible' or '❌ Not Eligible'
    """
    return "✅ Eligible" if cgpa >= cgpa_threshold and ats_score >= ats_threshold else "❌ Not Eligible"
