
from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.ai_response_routes import router as ai_response_router
from routes.email_routes import router as email_router
from routes.admin_routes import router as admin_router
from db import engine
from models import Base
from fastapi.middleware.cors import CORSMiddleware
from utils.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# Rate Limiter setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(ai_response_router)
app.include_router(email_router)
app.include_router(admin_router)

if engine:
    Base.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Chat Architecture API v2.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
