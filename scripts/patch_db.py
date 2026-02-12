
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL not found!")
    exit(1)

# Ensure it's using the correct scheme for newer sqlalchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def patch_database():
    with engine.connect() as conn:
        print("Checking for 'role' column in 'users' table...")
        try:
            # Check if role column exists
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name='role';"))
            if not result.fetchone():
                print("Adding 'role' column...")
                conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user';"))
                conn.commit()
                print("'role' column added successfully.")
            else:
                print("'role' column already exists.")
        except Exception as e:
            print(f"Error checking/adding role column: {e}")

        print("\nEnsuring other tables exist...")
        # Since Base.metadata.create_all(engine) should handle missing tables, 
        # we can just import the models and call it here too.
        from models import Base
        Base.metadata.create_all(engine)
        print("Table synchronization complete.")

if __name__ == "__main__":
    patch_database()
