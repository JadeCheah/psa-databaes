import os, json, time, requests
import numpy as np

# PSA Code Sprint gateway config
BASE = "https://psacodesprint2025.azure-api.net"
DEPLOYMENT = "text-embedding-3-small"
API_VERSION = "2023-05-15"
ENDPOINT = f"{BASE}/openai/deployments/{DEPLOYMENT}/embeddings"

SUB_KEY = os.getenv("PSA_SUBSCRIPTION_KEY")

def _headers():
    if not SUB_KEY:
        raise RuntimeError("Set PSA_SUBSCRIPTION_KEY env var.")
    # Use the same header that worked in your test
    return {"Content-Type": "application/json", "api-key": SUB_KEY}

def embed_texts(texts, batch_size=16, sleep=0.0):
    """Embed a list of strings. Returns list[np.ndarray]."""
    out = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        r = requests.post(
            ENDPOINT,
            params={"api-version": API_VERSION},
            headers=_headers(),
            json={"input": batch},
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()["data"]
        out.extend([np.array(item["embedding"], dtype=np.float32) for item in data])
        if sleep: time.sleep(sleep)
    return out

def _emp_text(emp):
    """Concatenate the most informative fields per employee."""
    parts = []
    ei = emp.get("employment_info", {})
    parts += [ei.get("job_title",""), ei.get("department",""), ei.get("unit","")]
    parts += [s.get("skill_name","") for s in emp.get("skills",[])]
    parts += [c.get("name","") for c in emp.get("competencies",[])]
    parts += [p.get("description","") for p in emp.get("projects",[])]
    return " | ".join([p for p in parts if p])

def create_embedding_cache(profiles, out_path="data/embedding_cache.json"):
    """Build once and save. Other teams consume this cache."""
    ids  = [p["employee_id"] for p in profiles]
    texts = [_emp_text(p) for p in profiles]
    vecs = embed_texts(texts)

    payload = {
        "model": DEPLOYMENT,
        "dim": len(vecs[0]) if vecs else 0,
        "vectors": {emp_id: v.tolist() for emp_id, v in zip(ids, vecs)}
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f)

def load_embedding_cache(path="data/embedding_cache.json"):
    with open(path) as f:
        raw = json.load(f)
    vectors = {k: np.array(v, dtype=np.float32) for k, v in raw["vectors"].items()}
    return {"model": raw["model"], "dim": raw["dim"], "vectors": vectors}

def cosine_sim(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0: return 0.0
    return float(np.dot(a, b) / (na * nb))
