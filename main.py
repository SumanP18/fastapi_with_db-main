
from fastapi import FastAPI, Request
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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    print(f"Headers: {request.headers}")
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://fastapi-with-db-main.onrender.com",
        "https://chat-gpt-frontend.vercel.app",
        "https://chat-gpt-frontend-revx84gkr-sumanp18s-projects.vercel.app",
        "https://chat-gpt-frontend-nine-delta.vercel.app",
    ],
    allow_origin_regex="https://chat-gpt-frontend.*\.vercel\.app",
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
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
