from metaflow.metaflow_config import SERVICE_HEADERS
from openai import OpenAI
import litellm
import os

### MODE 1: Use LiteLLM SDK
litellm.api_base = os.getenv("LITELLM_PROXY_URL")
response = litellm.completion(
    model="anthropic/claude-opus-4.1",
    messages = [
        {
            "role": "user",
            "content": "this is a test request, write a short poem"
        }
    ]
)
print(response)

### MODE 2: Use OpenAI SDK
client = OpenAI(
    api_key="dummy",
    base_url=os.getenv("LITELLM_PROXY_URL")
)

response2 = client.chat.completions.create(
    model="claude-opus-4.1",
    messages = [
        {
            "role": "user",
            "content": "this is a test request, write a short poem"
        }
    ],
    extra_headers = SERVICE_HEADERS
)

print(response2)