
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Conversation, User
import datetime

db = SessionLocal()
try:
    # Ensure we have a user
    user = db.query(User).filter(User.email == "newuser@example.com").first()
    if not user:
        print("User not found, cannot test conversation write.")
        exit(1)
    
    print(f"Found user: {user.email} (ID: {user.id})")
    
    # Try creating a conversation
    convo = Conversation(title="Test Convo", user_id=user.id, created_at=datetime.datetime.utcnow())
    db.add(convo)
    db.commit()
    db.refresh(convo)
    print(f"Successfully created conversation ID: {convo.id}")

    # Clean up
    db.delete(convo)
    db.commit()
    print("Successfully deleted test conversation.")
    
except Exception as e:
    print(f"Database write error: {e}")
finally:
    db.close()
