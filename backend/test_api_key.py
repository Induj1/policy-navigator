"""
OpenAI API Key Tester and Setup Helper
Run this to verify your OpenAI API key before starting the application.
"""

import os
from dotenv import load_dotenv

def test_openai_key():
    print("=" * 60)
    print("OpenAI API Key Tester")
    print("=" * 60)
    
    # Load .env file
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No OPENAI_API_KEY found in .env file")
        print("\n📝 To fix this:")
        print("1. Go to: https://platform.openai.com/api-keys")
        print("2. Create a new API key (or use existing)")
        print("3. Add to backend/.env file:")
        print("   OPENAI_API_KEY=sk-your-key-here")
        return False
    
    print(f"✓ API key found: {api_key[:20]}...{api_key[-4:]}")
    
    # Try to use the API
    try:
        print("\n🔑 Testing API key with OpenAI...")
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        # First check account status
        print("\n📊 Checking account status...")
        try:
            # Try to list models to verify access
            models = client.models.list()
            print(f"✓ Account is active (found {len(models.data)} models)")
        except Exception as e:
            print(f"⚠ Could not check models: {e}")
        
        # Test with a simple completion
        print("\n💬 Testing chat completion...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API key works!'"}],
            max_tokens=10
        )
        
        print("✅ SUCCESS! API key is valid and working")
        print(f"   Response: {response.choices[0].message.content}")
        print(f"   Model: {response.model}")
        
        # Check usage
        print(f"\n📊 Token usage: {response.usage.total_tokens} tokens")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ API Key Test FAILED: {error_msg}")
        
        if "429" in error_msg:
            print("\n🚫 Rate Limit / Quota Exceeded")
            
            if "insufficient_quota" in error_msg:
                print("   Issue: INSUFFICIENT QUOTA")
                print("\n   For PAID accounts, this means:")
                print("   - Monthly spending limit has been reached")
                print("   - Hard limit is set too low")
                print("   - Billing issue (expired card, etc.)")
                print("\n   Solutions for PAID accounts:")
                print("   1. Check billing: https://platform.openai.com/account/billing")
                print("      - Verify payment method is valid")
                print("      - Check if card expired or declined")
                print("   2. Check usage limits: https://platform.openai.com/account/limits")
                print("      - Increase hard limit if set too low")
                print("      - Default is $120/month, increase if needed")
                print("   3. View current usage: https://platform.openai.com/usage")
                print("      - See how much you've spent this month")
                print("   4. If just hit limit, increase it immediately in settings")
            else:
                print("   - Rate limit: Too many requests too fast")
                print("   - Wait 1 minute and try again")
                print("   - Or check: https://platform.openai.com/account/limits")
            
        elif "401" in error_msg or "invalid" in error_msg.lower():
            print("\n🔑 Invalid API Key")
            print("   Solutions:")
            print("   1. Generate new key at: https://platform.openai.com/api-keys")
            print("   2. Copy the FULL key (starts with sk-)")
            print("   3. Update .env file with new key")
            
        elif "403" in error_msg:
            print("\n🚫 Access Denied")
            print("   Your account may not have access to this API")
            print("   Check: https://platform.openai.com/account/limits")
            
        else:
            print("\n   Check your OpenAI account for more details:")
            print("   https://platform.openai.com/account")
        
        return False

if __name__ == "__main__":
    success = test_openai_key()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Ready to start the application!")
        print("   Run: .\\start-backend.ps1")
    else:
        print("❌ Fix the API key issue before starting")
        print("   Then run this script again to verify")
    print("=" * 60)
