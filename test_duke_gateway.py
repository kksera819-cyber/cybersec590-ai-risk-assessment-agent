
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

token = os.getenv("LITELLM_TOKEN")
base_url = os.getenv(
    "DUKE_GATEWAY_URL",
    "https://litellm.oit.duke.edu/v1"
)

if not token:
    raise RuntimeError("LITELLM_TOKEN is missing")

client = OpenAI(
    api_key=token,
    base_url=base_url,
    timeout=30.0
)

print("Connecting to Duke AI Gateway...")

models = client.models.list()
model_ids = [model.id for model in models.data]

print("\nAvailable models:")
for model_id in model_ids:
    print("-", model_id)

print("\nConnection successful!")
