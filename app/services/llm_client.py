# app/services/llm_client.py
import os
from openai import AzureOpenAI

# Load env vars
AZURE_API_KEY = os.getenv("PSA_SUBSCRIPTION_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_APIM_BASE", "https://psacodesprint2025.azure-api.net")
AZURE_DEPLOYMENT = os.getenv("DEPLOYMENT_GPT", "gpt-4o-mini")  # check actual name
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

# Create AzureOpenAI client
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT
)

def llm_is_configured() -> bool:
    return all([AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, AZURE_DEPLOYMENT])

def call_llm(messages: list[dict], temperature: float = 0.2, max_tokens: int = 300) -> str:
    """Send a chat completion request to Azure OpenAI via APIM."""
    if not llm_is_configured():
        raise RuntimeError("LLM not configured — missing env vars or deployment name.")
    completion = client.chat.completions.create(
        model=AZURE_DEPLOYMENT,  # this must match your deployment name
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content
