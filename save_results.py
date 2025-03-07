import pandas as pd
import os

file_path = "results.xlsx"

def save_to_excel(data):
    # Load existing data or create a new DataFrame
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
        except PermissionError:
            print("Error: Cannot open results.xlsx. Please close it if open.")
            return
    else:
        df = pd.DataFrame(columns=["Name", "Email", "CGPA", "ATS Score", "Eligibility"])

    # Append new data correctly
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    # Save back to Excel
    try:
        df.to_excel(file_path, index=False, engine="openpyxl")  # Use openpyxl to avoid permission errors
        print(f"Data saved successfully! Candidate: {data['Name']}")
    except PermissionError:
        print("Error: Unable to save results.xlsx. Check file permissions or close Excel.")
