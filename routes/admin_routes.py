
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import User, Conversation, ChatMessage, SystemSetting
from sqlalchemy import func
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

class SettingUpdate(BaseModel):
    key: str
    value: str

@router.get("/settings")
def get_settings(db: Session = Depends(get_db)):
    """Get all system settings."""
    return db.query(SystemSetting).all()

@router.post("/settings")
def update_setting(update: SettingUpdate, db: Session = Depends(get_db)):
    """Update or create a system setting."""
    setting = db.query(SystemSetting).filter(SystemSetting.key == update.key).first()
    if setting:
        setting.value = update.value
    else:
        setting = SystemSetting(key=update.key, value=update.value)
        db.add(setting)
    db.commit()
    return {"message": f"Setting {update.key} updated successfully"}

@router.get("/stats")
def get_usage_stats(db: Session = Depends(get_db)):
    """Get overall usage statistics for the admin dashboard."""
    total_users = db.query(User).count()
    total_conversations = db.query(Conversation).count()
    total_messages = db.query(ChatMessage).count()
    
    # Token usage per model (mocked or aggregated from history)
    total_tokens = db.query(func.sum(ChatMessage.tokens)).scalar() or 0
    
    return {
        "total_users": total_users,
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "total_tokens": total_tokens,
    }

@router.get("/recent_conversations")
def get_recent_conversations(db: Session = Depends(get_db), limit: int = 10):
    """Get list of most recent conversations."""
    conversations = db.query(Conversation).order_by(Conversation.created_at.desc()).limit(limit).all()
    return conversations

@router.get("/top_users")
def get_top_users(db: Session = Depends(get_db), limit: int = 5):
    """Get users with most conversations."""
    # Aggregation of users by conversation count
    top_users = db.query(User.email, func.count(Conversation.id).label("convo_count")).join(Conversation).group_by(User.id).order_by(func.count(Conversation.id).desc()).limit(limit).all()
    return [{"email": email, "convo_count": count} for email, count in top_users]
