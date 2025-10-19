import json, pandas as pd

def load_employee_profiles(path="data/Employee_Profiles.json"):
    with open(path, "r") as f:
        return json.load(f)

def load_skills_taxonomy(path="data/Functions & Skills.xlsx"):
    return pd.read_excel(path)
