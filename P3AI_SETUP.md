# Connecting to Real ZyndAI Network

## Quick Setup Guide

### 1. Create Your ZyndAI Agent

1. Visit **https://dashboard.zynd.ai**
2. Click "Get Started" and connect your MetaMask wallet
3. Navigate to "Agents" section and click "Create New Agent"
4. Fill in agent details:
   - Name: "Policy Navigator Agent"
   - Description: "AI agent for government policy interpretation and eligibility verification"
   - Capabilities: `policy_analysis, eligibility_verification, nlp, government_services`

### 2. Download Credentials

1. After creating the agent, view your agent's details
2. **Copy your Agent Seed** (secret seed phrase) - you'll need this for `.env`
3. Go to **Credentials tab** and **download the DID Document Credential**
4. Save it as `identity_credential.json` in the project root:
   ```
   policy-navigator/
   ├── identity_credential.json  ← Place here
   ├── backend/
   ├── frontend/
   └── .env
   ```

### 3. Update Environment Variables

Add to your `.env` file:

```env
# ZyndAI Network Credentials
AGENT_SEED=your_agent_seed_from_dashboard

# OpenAI API Key (for LLM features)
OPENAI_API_KEY=your_openai_api_key
```

⚠️ **Important**: The agent seed and DID credential must match - they are cryptographically linked!

### 4. Install ZyndAI Agent Package

```powershell
pip install zyndai-agent
```

### 5. Restart Backend Server

```powershell
cd policy-navigator
.\start-backend.ps1
```

You should see:
```
============================================================
✓ ZyndAI Agent Connected to Real Network
  Identity File: identity_credential.json
  Registry: https://registry.zynd.ai
  MQTT Broker: mqtt://registry.zynd.ai:1883
  Agent DID: did:polygonid:polygon:amoy:2qT...
============================================================
✓ LLM (GPT-4) connected to ZyndAI agent
```

## What You Get

### With Real ZyndAI Network:

✅ **Decentralized Identity (DID)** - Polygon ID-based verified identity
✅ **Agent Discovery** - ML-powered semantic matching to find agents by capabilities
✅ **Encrypted Communication** - End-to-end encrypted messages using ECIES (SECP256K1)
✅ **Verifiable Credentials** - Issue and verify credentials on blockchain
✅ **x402 Micropayments** - Built-in pay-per-use API support with automatic payment handling
✅ **Network Collaboration** - Connect to government agencies, credential issuers, etc.

### Features Available:

1. **Search for Agents**
   ```python
   client = get_p3ai_client()
   
   # Find credential issuers
   issuers = client.search_agents(
       capabilities=["credential_issuer", "income_verification"],
       match_score_gte=0.7,
       top_k=5
   )
   ```

2. **Connect to Agents**
   ```python
   # Connect to a discovered agent
   client.connect_to_agent(issuers[0])
   ```

3. **Send Encrypted Messages**
   ```python
   # Request credential verification
   result = client.send_message(
       message="Please verify income for citizen",
       message_type="query"
   )
   ```

4. **Read Incoming Messages**
   ```python
   # Check for responses
   messages = client.read_messages()
   ```

## Testing Connection

Test your P3AI connection:

```python
from app.infra.p3ai_client import get_p3ai_client

client = get_p3ai_client()

# Check status
status = client.get_connection_status()
print(status)
# Output:
# {
#     'p3ai_connected': True,
#     'llm_available': True,
#     'agent_instance': True,
#     'network_mode': 'Real P3AI Network'
# }

# Search for agents
agents = client.search_agents(
    capabilities=["policy_analysis"],
    match_score_gte=0.6,
    top_k=3
)

for agent in agents:
    print(f"Found: {agent['name']}")
    print(f"  DID: {agent['didIdentifier']}")
    print(f"  Match: {agent['matchScore']:.2f}")
```

## Troubleshooting

### "P3AI Agent - Running in Simulation Mode"

**Checklist:**
- [ ] `identity_credential.json` file exists in project root
- [ ] `AGENT_SEED` is set in `.env`
- [ ] File path is correct (check: `c:\Users\induj\Downloads\zynd\policy-navigator\identity_credential.json`)
- [ ] Agent seed matches the one from dashboard
- [ ] Agent seed and DID credential are cryptographically linked (created together)

### "Module not found: zyndai_agent"

```powershell
pip install zyndai-agent
```

### "Could not connect to registry"

- Check your internet connection
- Verify registry URL: `https://registry.zynd.ai`
- Check firewall settings (allow MQTT port 1883)

### "LLM features disabled"

Add OpenAI API key to `.env`:
```env
OPENAI_API_KEY=sk-...your_key
```

## Network Endpoints

**Production (Default):**
- Dashboard: `https://dashboard.zynd.ai`
- Registry: `https://registry.zynd.ai`
- MQTT Broker: `mqtt://registry.zynd.ai:1883`

**Local Development:**
- Registry: `http://localhost:3002`
- MQTT Broker: `mqtt://localhost:1883`

## Next Steps

Once connected to the real P3AI network:

1. **Discover Government Agents** - Find credential issuers for income, residence, student status
2. **Request Real Credentials** - Replace simulated credentials with blockchain-verified ones
3. **Collaborate with Other Agents** - Build multi-agent workflows
4. **Enable Advocacy Features** - Connect to support agents for application guidance

## Learn More

- **ZyndAI Documentation**: https://docs.zynd.ai
- **Agent SDK Repository**: https://github.com/zyndai/zyndai-agent
- **Dashboard**: https://dashboard.zynd.ai
- **Twitter**: [@ZyndAI](https://x.com/ZyndAI)
- **Email**: p3ainetwork@gmail.com

---

**Status Check Command:**

Add this endpoint to test ZyndAI connectivity from the frontend:

```python
# In backend/app/routers/citizens.py
@router.get("/p3ai-status")
async def get_p3ai_status():
    client = get_p3ai_client()
    return client.get_connection_status()
```

Visit: `http://localhost:8000/api/citizens/p3ai-status`

## Advanced: x402 Micropayments

ZyndAI includes built-in support for **x402 micropayments** - pay-per-use APIs with automatic payment handling!

### Example: Access Paid APIs

```python
from app.infra.p3ai_client import get_p3ai_client

client = get_p3ai_client()

# Make a paid API request (x402 handles payment automatically)
response = client.agent.x402_processor.post(
    url="https://api.premium-data.com/verify-income",
    json={"citizen_id": "123", "claimed_income": 100000}
)

result = response.json()
print(f"Verification: {result['verified']}")
print(f"Cost: {result['tokens_used']} tokens")
```

What x402 does automatically:
- ✅ Payment challenge/response flow
- ✅ Cryptographic signature generation  
- ✅ Automatic retry after payment verification
- ✅ Graceful error handling

This enables your agents to access premium government verification APIs, credential issuers, and data services with seamless micropayments!
