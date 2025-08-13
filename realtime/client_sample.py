from metaflow.metaflow_config import SERVICE_HEADERS
from openai import OpenAI
import os

client = OpenAI(
    api_key="dummy",
    base_url=os.getenv("LITELLM_PROXY_URL")
)

response = client.chat.completions.create(
    model="claude-opus-4.1",
    messages = [
        {
            "role": "user",
            "content": "this is a test request, write a short poem"
        }
    ],
    extra_headers = SERVICE_HEADERS
)

print(response)