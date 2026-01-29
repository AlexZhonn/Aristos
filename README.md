# Aristos - Smart Calorie & Budget Manager

**Aristos** is an intelligent mobile application that helps users save money and maintain a healthy lifestyle by tracking grocery spending, comparing delivery vs home cooking options, managing a virtual pantry with expiration tracking, and providing personalized insights.

## 🌟 Features

### Core Features
- **📸 Receipt Scanning**: Use your phone camera to scan grocery receipts. OpenAI Vision API automatically extracts items, prices, and quantities
- **🏠 Virtual Pantry**: Track all your groceries with automatic expiration date estimation
- **⚖️ Delivery Comparison**: Compare the cost and nutrition of delivery food vs cooking at home
- **📊 Smart Analytics**: View spending trends, calorie consumption, food waste statistics, and savings over time
- **🔔 Smart Notifications**: Get alerts when items are about to expire or when you're approaching your budget limit

### Additional Capabilities
- Automatic nutrition data extraction for purchased items
- Expiration urgency indicators (red for expired, yellow for soon, green for fresh)
- Category-based pantry organization (produce, dairy, meat, pantry, frozen, etc.)
- Daily summary statistics for spending and nutrition
- Recipe suggestions based on available ingredients (coming soon)

## 🏗️ Architecture

### Tech Stack

**Frontend** (React Native/Expo):
- React Native with Expo Router for navigation
- TypeScript for type safety
- TailwindCSS via NativeWind for styling
- Expo Image Picker for receipt/photo capture
- Expo Notifications for push notifications
- React Native Gifted Charts for data visualization
- Firebase Authentication for user management

**Backend** (Python/FastAPI):
- FastAPI for REST API
- Firebase Admin SDK for Firestore and Auth
- OpenAI GPT-4 Vision for receipt OCR
- OpenAI GPT-4 for nutrition data and recommendations
- APScheduler for background notification tasks
- Expo Push Notification service

**Database**:
- Firestore for all data storage (users, receipts, pantry items, comparisons, notifications)

## 📁 Project Structure

```
Aristos/
├── backend/                  # Python FastAPI backend
│   ├── main.py              # Application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── models/              # Pydantic data models
│   ├── services/            # Business logic (OCR, nutrition, analytics, etc.)
│   ├── router/              # API endpoints
│   ├── middleware/          # Auth middleware
│   └── tasks/               # Background scheduled tasks
│
├── frontend/                # React Native (Expo) mobile app
│   ├── app/                 # Expo Router app directory
│   │   ├── (tabs)/         # Tab-based navigation
│   │   │   ├── index.tsx   # Home/Dashboard
│   │   │   ├── scanner.tsx # Receipt scanner
│   │   │   ├── pantry.tsx  # Virtual pantry
│   │   │   └── compare.tsx # Delivery comparison
│   │   └── _layout.tsx     # Root layout with notifications
│   ├── components/          # Reusable UI components
│   │   └── ui/             # Specific UI components
│   ├── services/            # API client & Firebase config
│   └── package.json         # Node dependencies
│
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Firebase project
- OpenAI API key
- Expo Go app (for mobile testing)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create `.env` file):
```bash
OPENAI_API_KEY=sk-your-openai-key
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_PROJECT_ID=your-firebase-project-id
JWT_SECRET=your-random-secret-key
EXPO_PUSH_ACCESS_TOKEN=your-expo-token (optional)
ENVIRONMENT=development
```

5. Set up Firebase:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project
   - Enable Firestore Database
   - Enable Authentication (Email/Password)
   - Download service account credentials (Project Settings > Service Accounts > Generate New Private Key)
   - Save as `firebase-credentials.json` in backend directory

6. Run the backend:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API Documentation: http://localhost:8000/docs

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file (copy from `.env.example`):
```bash
EXPO_PUBLIC_API_URL=http://YOUR_IP:8000
EXPO_PUBLIC_FIREBASE_API_KEY=your-firebase-api-key
EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
EXPO_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
EXPO_PUBLIC_FIREBASE_APP_ID=your-app-id
EXPO_PUBLIC_EXPO_PROJECT_ID=your-expo-project-id
```

4. Start Expo development server:
```bash
npm start
```

5. Scan QR code with Expo Go app (iOS/Android)

## 📱 Usage

### 1. Scan a Receipt
1. Navigate to the **Scanner** tab
2. Take a photo or choose from gallery
3. Wait for AI processing
4. Items are automatically added to your virtual pantry

### 2. View Your Pantry
1. Go to the **Pantry** tab
2. See all items sorted by expiration date
3. Filter by category (produce, dairy, meat, etc.)
4. Mark items as consumed or remove them

### 3. Compare Delivery vs Home Cooking
1. Navigate to the **Compare** tab
2. Enter the delivery item details (name, restaurant, price)
3. Optionally add a photo
4. Get instant comparison with home cooking alternative
5. See savings and nutrition differences

### 4. Track Your Progress
1. Home **Dashboard** shows:
   - Today's spending and remaining budget
   - Calories consumed today
   - 14-day spending trends
   - 14-day calorie trends
2. Pull to refresh for latest data

## 🔔 Notifications

The app sends smart notifications for:
- **Expiration Alerts**: Items expiring in 3 days, 1 day, or today
- **Budget Warnings**: When approaching daily/weekly budget limits
- **Meal Suggestions**: Based on ingredients expiring soon
- **Daily Summaries**: Evening recap of spending and nutrition

## 🛠️ Development

### API Endpoints

**Authentication**:
- `POST /api/auth/setup-profile` - Set up user profile
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/profile` - Update profile

**Receipts**:
- `POST /api/receipts/upload` - Upload and process receipt
- `GET /api/receipts` - List all receipts
- `GET /api/receipts/{id}` - Get specific receipt
- `PUT /api/receipts/{id}` - Update receipt
- `DELETE /api/receipts/{id}` - Delete receipt

**Pantry**:
- `GET /api/pantry` - List pantry items
- `GET /api/pantry/expiring` - Get items expiring soon
- `POST /api/pantry` - Add item manually
- `PUT /api/pantry/{id}` - Update item
- `POST /api/pantry/{id}/consume` - Mark as consumed
- `DELETE /api/pantry/{id}` - Delete item

**Comparisons**:
- `POST /api/compare/analyze` - Analyze delivery item
- `GET /api/compare/history` - Get comparison history
- `GET /api/compare/{id}` - Get specific comparison

**Analytics**:
- `GET /api/analytics/spending` - Spending trends
- `GET /api/analytics/calories` - Calorie trends
- `GET /api/analytics/waste` - Food waste statistics
- `GET /api/analytics/savings` - Total savings
- `GET /api/analytics/today` - Today's summary

**Notifications**:
- `GET /api/notifications` - List notifications
- `PUT /api/notifications/{id}/read` - Mark as read
- `POST /api/notifications/register-token` - Register push token
- `POST /api/notifications/test` - Send test notification

## 🎯 Future Features

- [ ] AI-powered recipe generator from pantry items
- [ ] Social features (share recipes, group pantries)
- [ ] Shopping list generator
- [ ] Gamification (streaks, achievements, leaderboards)
- [ ] Smart meal planning (weekly meal plans)
- [ ] Barcode scanner for quick item addition
- [ ] Voice commands integration
- [ ] AR fridge visualization

## 🐛 Troubleshooting

### Backend Issues

**Firebase Connection Error**:
- Verify `firebase-credentials.json` exists and is valid
- Check Firebase project ID matches in `.env`
- Ensure Firestore is enabled in Firebase Console

**OpenAI API Errors**:
- Verify API key is correct
- Check account has credits
- Ensure you have access to GPT-4 Vision (gpt-4o model)

### Frontend Issues

**Cannot Connect to Backend**:
- Use your computer's local IP instead of `localhost`
- Ensure backend is running and accessible
- Check firewall settings

**Push Notifications Not Working**:
- Must use physical device (not simulator)
- Ensure you've granted notification permissions
- Register token via Settings (if needed)

**Receipt Processing Fails**:
- Ensure good lighting and clear image
- Check backend logs for OCR errors
- Verify OpenAI API key is working

## 📄 License

MIT License - Feel free to use this project for personal or educational purposes.

## 🙏 Acknowledgments

- OpenAI for GPT-4 Vision and GPT-4 APIs
- Firebase for backend services
- Expo team for amazing React Native tooling
- React Native community for excellent libraries

## 📧 Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Made with ❤️ for helping people save money and eat healthier**
