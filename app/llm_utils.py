import os
import requests
import httpx
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AIPROXY_TOKEN"),  # Set API key
    base_url="http://aiproxy.sanand.workers.dev/openai/v1" # Set base URL
)

# Email extraction or other llm tasks
def chat_completion(prompt: str, model: str = "gpt-4o-mini"):
    url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# Embeddings
def get_embeddings(inputs: list, model: str = "text-embedding-3-small"):
    url = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}"
    }
    data = {
        "model": model,
        "input": inputs
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['data']

# Function calling 
def query_gpt(user_input: str, tools: list[Dict[str, Any]]) -> Dict[str, Any]:
    response = requests.post(
        "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": user_input}],
            "tools": tools,
            "tool_choice": "auto",
        },
    )
    return response.json()["choices"][0]["message"]

# Image extraction
def image_extraction(base64_image):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the numbers from this image",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    choices = response.choices[0]
    return choices.message.content