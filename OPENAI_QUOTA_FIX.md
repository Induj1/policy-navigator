# How to Fix "OpenAI API Quota Exceeded" Error

## Problem
Your OpenAI API key has exceeded its quota:
- Free trial credits ($5) have been used up
- Or you hit the rate limit
- Error: `insufficient_quota`

## Solutions

### ✅ Solution 1: Add Payment Method (Best Option)

1. **Go to OpenAI Billing Page**
   - Visit: https://platform.openai.com/account/billing
   - Login with your OpenAI account

2. **Add Payment Method**
   - Click "Add payment method"
   - Enter credit card details
   - Set up usage limits (optional)

3. **Your API Key Works Immediately**
   - No need to generate new key
   - Current key in `.env` will work
   - GPT-3.5-turbo costs ~$0.002 per 1K tokens (very cheap)

4. **Expected Costs**
   - Light usage: $1-5/month
   - Medium usage: $5-20/month
   - This application uses GPT-3.5-turbo (cheapest option)

### ✅ Solution 2: Get New Free Trial (Temporary)

If you want to test without payment:

1. **Create New OpenAI Account**
   - Use different email address
   - Go to: https://platform.openai.com/signup
   - New accounts get $5 free credits

2. **Generate New API Key**
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the full key (starts with `sk-`)

3. **Update Your .env File**
   ```bash
   # Open backend/.env
   # Replace the line:
   OPENAI_API_KEY=sk-your-new-key-here
   ```

4. **Save and Restart Backend**

### ✅ Solution 3: Use Existing Paid Account

If you have another OpenAI account with credits:

1. Login to that account
2. Generate new API key (or use existing)
3. Update `backend/.env` with that key

## After Fixing

### Test Your New API Key
```powershell
cd backend
python test_api_key.py
```

You should see:
```
✅ SUCCESS! API key is valid and working
```

### Restart the Backend
```powershell
cd c:\Users\induj\Downloads\zynd\policy-navigator
.\start-backend.ps1
```

### Verify in Browser
Open: http://localhost:3000

The AI features should now work!

## Check Your Usage

Monitor your OpenAI usage at:
- https://platform.openai.com/usage

Set spending limits at:
- https://platform.openai.com/account/limits

## Cost Optimization

Our application uses **GPT-3.5-turbo** (cheapest model):
- Policy interpretation: ~500 tokens = $0.001
- Eligibility check: ~300 tokens = $0.0006
- Benefit matching: ~800 tokens = $0.0016

**Total cost per user session: ~$0.003** (less than 1 cent)

## Alternative: Run Without OpenAI

If you don't want to use OpenAI, you can:

1. **Remove API Key**
   - Delete `OPENAI_API_KEY` from `.env`
   - Application will run in limited mode

2. **Limited Features**
   - ❌ AI policy interpretation disabled
   - ❌ Smart eligibility checking disabled
   - ❌ Benefit matching disabled
   - ✅ Policy browsing still works
   - ✅ Manual rule checking works

## Need Help?

- OpenAI API Docs: https://platform.openai.com/docs
- Pricing: https://openai.com/pricing
- Support: https://help.openai.com

## Quick Commands Reference

```powershell
# Test API key
cd backend
python test_api_key.py

# Check current quota
# Visit: https://platform.openai.com/usage

# Start application
cd ..
.\start-backend.ps1

# In new terminal
cd frontend
npm run dev
```
