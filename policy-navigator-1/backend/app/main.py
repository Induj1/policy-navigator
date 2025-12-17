from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import policies, eligibility, benefits
from app.config import settings

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(policies.router)
app.include_router(eligibility.router)
app.include_router(benefits.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Policy Navigator API"}