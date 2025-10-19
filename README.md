# psa-databaes
## Person C (Recommenders & Analytics)
`/recommenders` module: contains the logic layer for generating AI-based recommendations. Includes:
- `recommenders/recommendation_engine.py` - Core script for recommendation logic
    - `recommend_training()` - finds missing or upskilling skills.
    - `recommend_team_collabs()` - suggests mentors or collaborators using embedding similarity.
    - `recommend_leadership()` - computes leadership potential based on competencies.
- `recommenders/test_recommenders.py` - Simple test file that runs all three functions with sample employee data to verify they execute without errors and return structured results.



