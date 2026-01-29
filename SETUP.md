# Aristos Setup Guide

Complete step-by-step guide to get Aristos running on your local machine.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Firebase Setup](#firebase-setup)
3. [OpenAI Setup](#openai-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Testing](#testing)
7. [Deployment](#deployment)

---

## Prerequisites

### Required Software
- **Node.js** 18+ and npm: [Download](https://nodejs.org/)
- **Python** 3.9+: [Download](https://www.python.org/downloads/)
- **Git**: [Download](https://git-scm.com/)
- **Expo Go** app on your phone: [iOS](https://apps.apple.com/app/expo-go/id982107779) | [Android](https://play.google.com/store/apps/details?id=host.exp.exponent)

### Accounts Needed
- **Firebase** account (free): [Sign up](https://console.firebase.google.com/)
- **OpenAI** account with API access: [Sign up](https://platform.openai.com/)
- **Expo** account (optional, for push notifications): [Sign up](https://expo.dev/)

---

## Firebase Setup

### Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"**
3. Enter project name: `aristos` (or your preferred name)
4. Disable Google Analytics (optional)
5. Click **"Create project"**

### Step 2: Enable Firestore Database

1. In Firebase Console, go to **"Build" > "Firestore Database"**
2. Click **"Create database"**
3. Select **"Start in test mode"** (for development)
4. Choose your preferred location
5. Click **"Enable"**

### Step 3: Enable Authentication

1. Go to **"Build" > "Authentication"**
2. Click **"Get started"**
3. Click on **"Email/Password"** provider
4. Enable both toggles
5. Click **"Save"**

### Step 4: Get Firebase Configuration

#### For Backend (Service Account):
1. Go to **"Project Settings"** (gear icon) > **"Service accounts"**
2. Click **"Generate new private key"**
3. Click **"Generate key"**
4. Save the JSON file as `firebase-credentials.json`
5. Move it to `backend/` directory

#### For Frontend (Web Config):
1. Go to **"Project Settings"** > **"General"**
2. Scroll to **"Your apps"** section
3. Click the **Web icon** (</>)
4. Register app with nickname: `aristos-web`
5. Copy the configuration values:
   - apiKey
   - authDomain
   - projectId
   - storageBucket
   - messagingSenderId
   - appId

---

## OpenAI Setup

### Step 1: Get API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create account
3. Go to **"API keys"** section
4. Click **"Create new secret key"**
5. Name it `aristos-key`
6. Copy the key (starts with `sk-`)
7. **Important**: Store it securely, you won't see it again

### Step 2: Add Credits (if needed)

1. Go to **"Billing"** > **"Payment methods"**
2. Add a payment method
3. Set spending limits (recommended: $10/month for testing)

### Step 3: Verify Model Access

1. Ensure you have access to `gpt-4o` (GPT-4 Vision)
2. If not, you may need to:
   - Add payment method
   - Make initial payment
   - Wait for approval (usually instant)

---

## Backend Setup

### Step 1: Clone Repository & Navigate

```bash
cd Aristos/backend
```

### Step 2: Create Virtual Environment

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
# OpenAI
OPENAI_API_KEY=sk-your-actual-key-here

# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_PROJECT_ID=your-firebase-project-id

# Security
JWT_SECRET=your-random-secret-key-here

# Expo Push (optional)
EXPO_PUSH_ACCESS_TOKEN=

# Environment
ENVIRONMENT=development
```

**Generate JWT Secret**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 5: Place Firebase Credentials

Ensure `firebase-credentials.json` is in the `backend/` directory (from Firebase Setup Step 4).

### Step 6: Test Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs to see API documentation.

**Expected output**:
```
🚀 Aristos API starting up...
📱 Backend ready to serve requests
```

---

## Frontend Setup

### Step 1: Navigate to Frontend

```bash
cd ../frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Configure Environment Variables

Create `.env` file in `frontend/` directory:

```bash
# Backend API (use your computer's local IP, not localhost)
EXPO_PUBLIC_API_URL=http://192.168.1.100:8000

# Firebase Config (from Firebase Setup Step 4)
EXPO_PUBLIC_FIREBASE_API_KEY=your-api-key
EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
EXPO_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
EXPO_PUBLIC_FIREBASE_APP_ID=your-app-id

# Expo Project (optional, for push notifications)
EXPO_PUBLIC_EXPO_PROJECT_ID=your-expo-project-id
```

**Find Your Local IP**:
- **macOS/Linux**: `ifconfig | grep "inet " | grep -v 127.0.0.1`
- **Windows**: `ipconfig` (look for IPv4 Address)

### Step 4: Start Expo Development Server

```bash
npm start
```

### Step 5: Run on Device

1. Open **Expo Go** app on your phone
2. Scan the QR code shown in terminal
3. Wait for app to build and load

**Troubleshooting**:
- Ensure phone and computer are on same WiFi network
- If QR doesn't work, choose **"Tunnel"** mode in Expo

---

## Testing

### Test Backend API

1. **Health Check**:
```bash
curl http://localhost:8000/health
```

2. **Test Receipt Upload** (requires auth):
   - Use Swagger UI: http://localhost:8000/docs
   - Click "Authorize", enter Firebase ID token
   - Test endpoints interactively

### Test Frontend

1. **Registration/Login**:
   - Should be handled via Firebase Auth SDK
   - Create test account in Firebase Console

2. **Receipt Scanning**:
   - Take photo of a grocery receipt
   - Should process and show extracted items
   - Items should appear in Pantry tab

3. **Pantry Management**:
   - View items in Pantry tab
   - Mark items as consumed
   - Check expiration indicators

4. **Delivery Comparison**:
   - Go to Compare tab
   - Enter delivery item details
   - Should show cost and calorie comparison

5. **Push Notifications** (physical device only):
   - Grant notification permissions
   - Send test notification via API

---

## Deployment

### Backend Deployment Options

#### Option 1: Google Cloud Run

```bash
# Build Docker image
docker build -t aristos-backend .

# Push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/aristos-backend

# Deploy to Cloud Run
gcloud run deploy aristos-backend \
  --image gcr.io/YOUR_PROJECT_ID/aristos-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Option 2: Railway

1. Go to [Railway.app](https://railway.app/)
2. Click **"New Project" > "Deploy from GitHub repo"**
3. Select your repository
4. Set environment variables
5. Railway will auto-deploy

#### Option 3: Heroku

```bash
heroku create aristos-backend
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set FIREBASE_PROJECT_ID=...
# ... set other env vars
git push heroku main
```

### Frontend Deployment

#### Expo EAS Build (Recommended)

1. Install EAS CLI:
```bash
npm install -g eas-cli
```

2. Login to Expo:
```bash
eas login
```

3. Configure build:
```bash
eas build:configure
```

4. Build for iOS and Android:
```bash
eas build --platform all
```

5. Submit to stores:
```bash
eas submit --platform ios
eas submit --platform android
```

---

## Common Issues

### Firebase Connection Error
**Error**: `Firebase initialization error`

**Solution**:
- Check `firebase-credentials.json` is in correct location
- Verify Firebase project ID matches
- Ensure Firestore is enabled

### OpenAI Rate Limit
**Error**: `Rate limit exceeded`

**Solution**:
- Check OpenAI account has credits
- Add payment method
- Wait a few minutes and retry

### Cannot Connect to Backend from Phone
**Error**: `Network request failed`

**Solution**:
- Use local IP address, not `localhost`
- Ensure phone and computer on same network
- Check firewall settings
- Try using Expo tunnel mode

### Receipt Processing Fails
**Error**: `Failed to process receipt`

**Solution**:
- Ensure good lighting for photos
- Check OpenAI API key is valid
- Verify you have GPT-4 Vision access
- Check backend logs for specific error

---

## Next Steps

After setup is complete:

1. ✅ Test all features thoroughly
2. ✅ Set up production Firebase security rules
3. ✅ Configure production environment variables
4. ✅ Set up monitoring and logging
5. ✅ Create app store listings
6. ✅ Submit for review

---

## Need Help?

- 📖 Check the main [README.md](README.md)
- 🐛 Open an issue on GitHub
- 💬 Contact the development team

**Happy building! 🚀**
