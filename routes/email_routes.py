from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db import get_db
from utils.email_sender import send_email

router = APIRouter()

@router.post("/send-email")
def send_email_route(receiver_email: str, subject: str, content: str,db:Session=Depends(get_db)):
    """send an email to the receiver with the given subject and content"""
    send_email(receiver_email, subject, content)
    return {"message": "Email sent successfully"}   
    