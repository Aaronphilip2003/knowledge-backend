import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")

API_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}/pipeline/feature-extraction"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

def generate_embedding(text: str):
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

    embedding = response.json()

    # all-MiniLM returns nested list
    if isinstance(embedding, list) and isinstance(embedding[0], list):
        embedding = embedding[0]

    return embedding