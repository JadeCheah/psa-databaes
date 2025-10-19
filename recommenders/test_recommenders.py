"""
test_recommenders.py
Simple local test runner for recommendation functions.
"""

from recommenders.recommendation_engine import (
    recommend_training,
    recommend_team_collabs,
    recommend_leadership,
)
from core import load_employee_profiles


def run_tests():
    profiles = load_employee_profiles()
    if not profiles:
        print("⚠️  No profiles found! Check Employee_Profiles.json path.")
        return

    sample_emp = profiles[0]["employee_id"]
    print(f"Testing recommendations for: {sample_emp}\n")

    print("📘 Training Suggestions:")
    print(recommend_training(sample_emp))

    print("\n👥 Collaboration / Mentorship:")
    print(recommend_team_collabs(sample_emp))

    print("\n🏆 Leadership Ranking:")
    print(recommend_leadership(sample_emp))


if __name__ == "__main__":
    run_tests()
