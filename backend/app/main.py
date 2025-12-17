from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import citizens, eligibility, policies, documents, translation, chat, impact, simple_eligibility, policy_interpretation
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
    allow_origins=["*"],  # Allow all origins for development
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
    
    if client.agent and client.is_connected:
        try:
            agent_did = getattr(client.agent, 'did', 'N/A')
            print(f"📋 Agent DID: {agent_did}")
            print(f"🌐 Network: Connected to ZyndAI")
        except Exception as e:
            print(f"⚠ Could not get agent details: {e}")
    else:
        print("⚠ Running in simulation mode")
    
    print(f"✓ LLM Available: {client.llm is not None}")
    print(f"✓ ZyndAI Available: {client.is_p3ai_available()}")
    print("=" * 60)

# Include routers
app.include_router(policies.router, prefix="/api/policies", tags=["Policies"])
app.include_router(eligibility.router, prefix="/api/eligibility", tags=["Eligibility"])
app.include_router(simple_eligibility.router, prefix="/api/eligibility", tags=["Simple Eligibility"])
app.include_router(policy_interpretation.router, prefix="/api/policies", tags=["Policy Interpretation"])
app.include_router(citizens.router, prefix="/api/citizens", tags=["Citizens"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(translation.router, prefix="/api", tags=["Translation"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(impact.router, prefix="/api", tags=["Impact Prediction"])

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
    try:
        client = get_p3ai_client()
        return {
            "status": "healthy",
            "llm_available": client.is_llm_available(),
            "p3ai_available": client.is_p3ai_available(),
            "connection_status": client.get_connection_status()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "llm_available": False,
            "p3ai_available": False
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)