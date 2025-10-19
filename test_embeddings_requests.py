import os, requests, json

# --- Configuration ---
subscription_key = os.getenv("PSA_SUBSCRIPTION_KEY", "6e2b48cef6a1435280b629649f13e15a")
url = "https://psacodesprint2025.azure-api.net/openai/deployments/text-embedding-3-small/embeddings?api-version=2023-05-15"

headers = {
    "Content-Type": "application/json",
    # depending on gateway config, either of these may work:
    "api-key": subscription_key,  # try this one first
    # "Ocp-Apim-Subscription-Key": subscription_key,  # uncomment if needed
}

data = {
    "input": "Cloud Architecture and Automation"
}

response = requests.post(url, headers=headers, json=data)
print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2))





