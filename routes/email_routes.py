
from fastapi import APIRouter, Query
from utils.email_sender import send_email

router = APIRouter()


@router.post("/send-email")
def send_email_route(
    email: str = Query(..., description="Receiver's email address"),
    subject: str = Query(..., description="Email subject"),
    content: str = Query(..., description="Email content")
):
    """Send an email to the receiver with the given subject and content."""
    send_email(email, subject, content)
    return {"message": "Email sent successfully"}
