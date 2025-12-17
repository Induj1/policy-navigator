# Deployment Guide

## Prerequisites
1. GitHub account with repository created
2. Render account (https://render.com)
3. Vercel account (https://vercel.com)

## Step 1: Push to GitHub

```bash
# Initialize git if not already done
cd C:\Users\induj\Downloads\zynd
git init

# Add remote (replace YOUR_USERNAME/YOUR_REPO with your GitHub details)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push code
git push -u origin main
```

## Step 2: Deploy Backend to Render

1. Go to https://render.com and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select `policy-navigator/backend` as the root directory
5. Configure:
   - **Name**: policy-navigator-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key
7. Click "Create Web Service"
8. Wait for deployment (5-10 minutes)
9. Copy the deployed URL (e.g., https://policy-navigator-backend.onrender.com)

## Step 3: Deploy Website Frontend to Vercel

1. Go to https://vercel.com and sign in
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Select `policy-navigator/frontend` as the root directory
5. Configure:
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
6. Add environment variable:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your Render backend URL (from Step 2)
7. Click "Deploy"
8. Wait for deployment (3-5 minutes)
9. Your website will be live at https://your-project.vercel.app

## Step 4: Update Mobile App API URL

Edit `policy-navigator-mobile/lib/config/api_config.dart`:

```dart
class ApiConfig {
  static const String baseUrl = 'https://policy-navigator-backend.onrender.com';
}
```

Then rebuild and deploy your Flutter app to:
- **Web**: Deploy to Firebase Hosting or Vercel
- **Android**: Build APK and deploy to Play Store
- **iOS**: Build IPA and deploy to App Store

## Environment Variables Summary

### Backend (Render)
- `OPENAI_API_KEY`: Your OpenAI API key
- `PORT`: Auto-set by Render

### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL`: Your backend URL from Render

## Testing

After deployment:
1. Visit your Vercel URL
2. Test all features: Eligibility Check, Benefits, Policy Interpretation, Chat, Impact Prediction
3. Change language to verify translations work
4. Open mobile app and verify it connects to deployed backend

## Troubleshooting

### Backend Issues
- Check Render logs for errors
- Verify OPENAI_API_KEY is set correctly
- Ensure `requirements.txt` has all dependencies

### Frontend Issues
- Check Vercel deployment logs
- Verify `NEXT_PUBLIC_API_URL` points to correct backend
- Enable CORS on backend if needed

### Mobile App Issues
- Verify `baseUrl` in `api_config.dart` is correct
- Check if backend is accessible from mobile network
- Review Flutter console for API errors
