from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import citizens, eligibility, policies
from app.infra.p3ai_client import get_p3ai_client

# Initialize FastAPI app
app = FastAPI(
    title="Policy Navigator API",
    description="Multi-agent AI system for government policy interpretation and benefit matching",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize P3AI client on startup
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    client = get_p3ai_client()
    print("=" * 60)
    print("🚀 Policy Navigator Backend Started")
    print("=" * 60)
    
    identity = client.get_identity()
    if identity:
        print(f"📋 Agent Identity: {identity.get('did', 'N/A')}")
        print(f"🌐 Network: {identity.get('network', client.network)}")
    
    print(f"✓ LLM Available: {client.llm is not None}")
    print(f"✓ P3AI Available: {client.is_available()}")
    print("=" * 60)

# Include routers
app.include_router(policies.router, prefix="/api/policies", tags=["Policies"])
app.include_router(eligibility.router, prefix="/api/eligibility", tags=["Eligibility"])
app.include_router(citizens.router, prefix="/api/citizens", tags=["Citizens"])

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "running",
        "service": "Policy Navigator API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Detailed health check."""
    client = get_p3ai_client()
    return {
        "status": "healthy",
        "llm_available": client.llm is not None,
        "p3ai_available": client.is_available(),
        "identity": client.get_identity()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)