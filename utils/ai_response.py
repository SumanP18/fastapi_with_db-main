
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import datetime

load_dotenv()

endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def get_completion(user_message, system_message="You are a helpful assistant.", api_token=None, model_name=None):
    """
    Get a completion from the AI model.
    
    Args:
        user_message: The user's message
        system_message: The system prompt
        api_token: Optional API token to override environment
        model_name: Optional model name to override default
    
    Returns:
        tuple: (content, prompt_tokens, completion_tokens, total_tokens)
    """
    use_token = api_token or token
    use_model = model_name or model
    
    local_client = client
    if api_token:
        local_client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_token),
        )

    response = local_client.complete(
        messages=[
            SystemMessage(system_message),
            UserMessage(user_message),
        ],
        model=use_model
    )

    content = response.choices[0].message.content
    p_tokens = response.usage.prompt_tokens
    c_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    return content, p_tokens, c_tokens, total_tokens

def generate_image(prompt):
    """
    Generate an image from a prompt using Pollinations.ai (Free/Fast).
    Returns the URL of the generated image.
    """
    import urllib.parse
    encoded_prompt = urllib.parse.quote(prompt)
    # Using Pollinations.ai as a high-performance free alternative
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={datetime.datetime.now().timestamp()}"
    return image_url
