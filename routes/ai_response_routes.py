
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from db import get_db
from utils.ai_response import get_completion, generate_image
from schemas.ai_response_schemas import AIRequest, AIResponse, ImageRequest, ImageResponse
from models import Conversation, ChatMessage, User, SystemSetting
from utils.auth_utils import get_current_user
from utils.limiter import limiter

router = APIRouter(tags=["AI"])

@router.post("/ai_response", response_model=AIResponse)
@limiter.limit("5/minute")
def ask_ai(request: Request, ai_request: AIRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get response from AI model with rate limiting, DB settings, and persistence."""
    try:
        # Fetch System Settings
        settings = db.query(SystemSetting).all()
        settings_dict = {s.key: s.value for s in settings}
        
        api_token = settings_dict.get("GITHUB_TOKEN")
        model_name = settings_dict.get("AI_MODEL")

        # Determine Title
        title = ai_request.message[:50]
        
        # Get Completion with Token Usage
        content, p_tokens, c_tokens, total_tokens = get_completion(
            ai_request.message, 
            ai_request.system_prompt,
            api_token=api_token,
            model_name=model_name
        )
        
        # Persistence Logic
        # 1. Ensure a conversation exists for this interaction
        # We'll create one for now as a new "Session"
        convo = Conversation(title=title, user_id=current_user.id)
        db.add(convo)
        db.commit()
        db.refresh(convo)
        
        # 2. Save User Message
        user_msg = ChatMessage(
            conversation_id=convo.id,
            role="user",
            content=ai_request.message,
            tokens=p_tokens
        )
        db.add(user_msg)
        
        # 3. Save Assistant Message
        assistant_msg = ChatMessage(
            conversation_id=convo.id,
            role="assistant",
            content=content,
            tokens=c_tokens
        )
        db.add(assistant_msg)
        
        db.commit()
        
        return AIResponse(response=content)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate_image", response_model=ImageResponse)
def get_image(request: Request, image_req: ImageRequest, current_user: User = Depends(get_current_user)):
    """Generate an image from a prompt."""
    try:
        url = generate_image(image_req.prompt)
        return {"image_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

