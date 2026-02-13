
from sqlalchemy.orm import Session
from db import SessionLocal
from models import SystemSetting

db = SessionLocal()
settings = db.query(SystemSetting).all()
for s in settings:
    print(f"Key: {s.key}, Value: '{s.value}'")
db.close()
