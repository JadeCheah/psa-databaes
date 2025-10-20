import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # <-- add this line

from core.data_loader import load_employee_profiles
from core.embedding_utils import create_embedding_cache

def main():
    profiles = load_employee_profiles("data/Employee_Profiles.json")
    print(f"Loaded {len(profiles)} profiles; creating embedding cache…")
    create_embedding_cache(profiles, out_path="data/embedding_cache.json")
    print("✅ Wrote data/embedding_cache.json")

if __name__ == "__main__":
    main()