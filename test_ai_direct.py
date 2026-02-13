
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

try:
    token = os.environ["GITHUB_TOKEN"]
    print(f"Token found: {token[:10]}...")
except KeyError:
    print("GITHUB_TOKEN not found in environment!")
    exit(1)

endpoint = "https://models.github.ai/inference"
model_name = "gpt-4o-mini"

print(f"Connecting to {endpoint} with model {model_name}...")

try:
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
        credential_scopes=["https://models.github.ai/inference/.default"],
        timeout=10 # 10 seconds timeout
    )
    print("Client created.")

    print("Sending request...")
    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("Hello!"),
        ],
        model=model_name
    )
    print("Response received!")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")
