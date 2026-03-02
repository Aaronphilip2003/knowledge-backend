import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")

API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}/pipeline/feature-extraction"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
}


def generate_embedding(text: str):
    if not text.strip():
        return []

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": text,
            "options": {"wait_for_model": True}
        },
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"HF Error: {response.text}")

    data = response.json()

    # Handle nested output from sentence-transformers
    if isinstance(data, list) and isinstance(data[0], list):
        embedding = data[0]
    else:
        embedding = data

    # Safety check
    if not isinstance(embedding, list):
        raise Exception(f"Unexpected HF response format: {data}")

    return embedding