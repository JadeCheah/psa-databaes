from core.data_loader import load_employee_profiles
from core.embedding_utils import create_embedding_cache, load_embedding_cache

print("Loading employee profiles...")
profiles = load_employee_profiles()
print("Loaded", len(profiles), "profiles")

print("Creating embedding cache...")
create_embedding_cache(profiles)
print("✅ Embedding cache created successfully!")

cache = load_embedding_cache()
print("model:", cache["model"])
print("dim:", cache["dim"])
print("employees:", len(cache["vectors"]))



