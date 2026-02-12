from pydantic import BaseModel

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."

class AIResponse(BaseModel):
    response: str

class ImageRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"

class ImageResponse(BaseModel):
    image_url: str