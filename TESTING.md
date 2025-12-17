# Testing the Policy Navigator System

## Quick Start

### 1. Start Backend
```powershell
cd backend
.\start-backend.ps1
```

### 2. Start Frontend
```powershell
cd frontend
npm run dev
```

### 3. Open Application
Navigate to: http://localhost:3000

## System Status Dashboard

The home page now displays a **System Status** widget showing:

### Connection Indicators
- **Green dot (Connected)**: Real ZyndAI network connection active
- **Yellow dot (Offline)**: Running in simulation mode

### Network Information (when connected)
- Mode: Real Network / Simulation
- Registry URL: https://registry.zynd.ai
- MQTT Broker: registry.zynd.ai:1883
- Agent DID: Your unique decentralized identifier
- Identity Verified: Credential authentication status

### Features Status
Shows which features are available:
- ✓ **Policy Interpretation**: Always available
- ✓ **Eligibility Checking**: Always available
- ✓ **Benefit Matching**: Always available
- ✓ **Credential Issuance**: Requires network connection
- ✓ **Agent Discovery**: Requires network connection
- ✓ **Encrypted Communication**: Requires network connection

## Testing Scenarios

### Scenario 1: Simulation Mode (Default)
**Setup**: No ZyndAI credentials configured

**Expected Status**:
```
ZyndAI Network: Offline
Mode: Simulation
Running in simulation mode - No network credentials configured
```

**Features**:
- Policy interpretation ✓
- Eligibility checking ✓
- Benefit matching ✓ (uses hardcoded policies)
- Credential issuance ○ (disabled)
- Agent discovery ○ (disabled)
- Encrypted communication ○ (disabled)

### Scenario 2: Real Network Mode
**Setup**: 
1. Create agent at https://dashboard.zynd.ai
2. Download `identity_credential.json` → place in `backend/`
3. Add `AGENT_SEED=your_seed` to `backend/.env`
4. Restart backend

**Expected Status**:
```
ZyndAI Network: Connected
Mode: Real Network
Registry: registry.zynd.ai
Agent DID: did:polygonid:polygon:mumbai:2q...
```

**Features**:
- All features enabled ✓

### Scenario 3: Dynamic Policy Fetching

#### Test Network Policy Discovery
```bash
curl http://localhost:8000/api/policies/sample
```

**Simulation Mode Response**:
```json
{
  "source": "hardcoded",
  "count": 4,
  "policies": [...]
}
```

**Network Mode Response**:
```json
{
  "source": "network",
  "count": 15,
  "agents_discovered": 3,
  "policies": [...]
}
```

#### Test State-Specific Policies
```bash
curl http://localhost:8000/api/policies/by-state/Maharashtra
```

#### Force Policy Refresh
```bash
curl -X POST http://localhost:8000/api/policies/refresh
```

**Response**:
```json
{
  "status": "refreshed",
  "source": "network",
  "policies_fetched": 15,
  "agents_contacted": 3,
  "cache_cleared": true
}
```

## API Endpoints for Testing

### System Status
```bash
curl http://localhost:8000/api/citizens/status
```

Returns system health and network status.

### Policy Endpoints
```bash
# Get all policies (network or hardcoded)
GET http://localhost:8000/api/policies/sample

# Get policies by state
GET http://localhost:8000/api/policies/by-state/{state}

# Force refresh from network
POST http://localhost:8000/api/policies/refresh

# Interpret policy text
POST http://localhost:8000/api/policies/interpret
```

### Eligibility Endpoints
```bash
# Check if citizen meets requirements
POST http://localhost:8000/api/eligibility/check

# Match citizen with benefits
POST http://localhost:8000/api/eligibility/match-benefits
```

### Credential Endpoints
```bash
# Issue verifiable credential (requires network)
POST http://localhost:8000/api/citizens/issue-credential
```

## Frontend Testing

### 1. Check Eligibility Flow
1. Navigate to "Check Eligibility"
2. Fill in citizen details:
   - Name: Test User
   - Age: 25
   - State: Maharashtra
   - Income: 15000
   - Disability: 50%
3. Click "Check Eligibility"
4. View matched benefits and eligibility status

### 2. Policy Interpretation Flow
1. Navigate to "Understand Policies"
2. Paste policy text:
   ```
   Maharashtra Disability Support 2024
   
   Eligibility:
   - Disability percentage must be at least 40%
   - Must be a permanent resident of Maharashtra
   - Annual income should not exceed ₹200,000
   ```
3. Click "Interpret Policy"
4. Review extracted rules

### 3. Browse Benefits Flow
1. Navigate to "Browse Benefits"
2. Fill in profile:
   - Age: 30
   - State: Karnataka
   - Income: 20000
   - Disability: 0
3. Click "Find My Benefits"
4. View matched benefits with eligibility scores

## Monitoring Logs

### Backend Logs
Watch for these indicators:

**Simulation Mode**:
```
⚠ Running in SIMULATION mode - agent features disabled
  Missing ZyndAI network credentials
```

**Network Mode**:
```
✓ ZyndAI agent initialized successfully!
  DID: did:polygonid:polygon:mumbai:2q...
  Registry: https://registry.zynd.ai
✓ LLM (GPT-4) connected to ZyndAI agent
```

**Policy Fetching**:
```
🔍 Discovering policy agents on ZyndAI network...
✓ Found 3 policy agents
📡 Fetching policies from agent: did:polygonid:...
✓ Received 15 policies from network
```

**Fallback**:
```
⚠ No policy agents found on network
ℹ Using 4 hardcoded fallback policies
```

## Troubleshooting

### Status Shows "Offline" but credentials configured
1. Check `.env` file has `AGENT_SEED=...`
2. Verify `identity_credential.json` exists in `backend/`
3. Check file permissions
4. Restart backend completely

### Policies not refreshing from network
1. Click "Refresh" button in UI
2. Call POST `/api/policies/refresh` endpoint
3. Check backend logs for agent discovery
4. Verify network connectivity to registry.zynd.ai

### Features showing as disabled
1. Check system status widget
2. If "Offline", configure ZyndAI credentials
3. If "Connected", check backend logs for errors
4. Verify OpenAI API key for LLM features

## Performance Metrics

### Expected Response Times

**Simulation Mode**:
- Policy fetching: < 100ms (hardcoded)
- Eligibility check: 2-3 seconds (LLM)
- Benefit matching: 3-4 seconds (LLM)

**Network Mode**:
- Policy discovery: 5-10 seconds (first time)
- Policy fetching: 2-3 seconds (cached after first fetch)
- Credential issuance: 3-5 seconds (network + crypto)

## Next Steps

After testing in simulation mode:

1. **Get ZyndAI Credentials**:
   - Visit https://dashboard.zynd.ai
   - Create your agent
   - Download credentials

2. **Deploy Policy Agent** (optional):
   - Create your own policy-serving agent
   - Register on ZyndAI network
   - Test full network flow

3. **Production Setup**:
   - Configure environment variables
   - Set up proper credential storage
   - Enable x402 micropayments
   - Add monitoring/logging

## Resources

- **ZyndAI Dashboard**: https://dashboard.zynd.ai
- **Setup Guide**: See P3AI_SETUP.md
- **API Docs**: http://localhost:8000/docs (when backend running)
- **Frontend**: http://localhost:3000
