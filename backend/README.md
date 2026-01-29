# Aristos Backend API

Smart Calorie & Budget Manager Backend built with FastAPI.

## Setup

### Prerequisites
- Python 3.9+
- Firebase project with Firestore
- OpenAI API key

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add:
- `OPENAI_API_KEY`: Your OpenAI API key
- `FIREBASE_CREDENTIALS_PATH`: Path to Firebase credentials JSON
- `FIREBASE_PROJECT_ID`: Your Firebase project ID
- `JWT_SECRET`: Random secret key for JWT
- `EXPO_PUSH_ACCESS_TOKEN`: Expo push notification token (optional)

4. Set up Firebase:
- Go to [Firebase Console](https://console.firebase.google.com/)
- Create a new project or use existing one
- Enable Firestore Database
- Enable Authentication (Email/Password)
- Download service account credentials:
  - Go to Project Settings > Service Accounts
  - Click "Generate New Private Key"
  - Save as `firebase-credentials.json` in backend directory

### Running the Server

Development mode:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Production mode:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

API documentation will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/setup-profile` - Set up user profile
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/profile` - Update profile

### Receipts
- `POST /api/receipts/upload` - Upload receipt
- `GET /api/receipts` - List receipts
- `GET /api/receipts/{id}` - Get receipt
- `PUT /api/receipts/{id}` - Update receipt
- `DELETE /api/receipts/{id}` - Delete receipt

### Pantry
- `GET /api/pantry` - List pantry items
- `GET /api/pantry/expiring` - Get expiring items
- `POST /api/pantry` - Add item
- `PUT /api/pantry/{id}` - Update item
- `POST /api/pantry/{id}/consume` - Mark consumed
- `DELETE /api/pantry/{id}` - Delete item

### Comparisons
- `POST /api/compare/analyze` - Analyze delivery item
- `GET /api/compare/history` - Get comparison history
- `GET /api/compare/{id}` - Get comparison

### Analytics
- `GET /api/analytics/spending` - Spending trends
- `GET /api/analytics/calories` - Calorie trends
- `GET /api/analytics/waste` - Waste statistics
- `GET /api/analytics/savings` - Savings data
- `GET /api/analytics/today` - Today's summary

### Notifications
- `GET /api/notifications` - List notifications
- `PUT /api/notifications/{id}/read` - Mark as read
- `POST /api/notifications/register-token` - Register push token
- `POST /api/notifications/test` - Send test notification

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── models/             # Pydantic models
│   ├── user.py
│   ├── receipt.py
│   ├── ingredient.py
│   ├── comparison.py
│   └── notification.py
├── services/           # Business logic
│   ├── firebase_service.py
│   ├── ocr_service.py
│   ├── nutrition_service.py
│   ├── expiration_service.py
│   ├── notification_service.py
│   ├── analytics_service.py
│   ├── delivery_analyzer.py
│   └── recipe_matcher.py
├── router/             # API endpoints
│   ├── auth.py
│   ├── receipts.py
│   ├── pantry.py
│   ├── comparison.py
│   ├── analytics.py
│   └── notifications.py
├── middleware/         # Custom middleware
│   └── auth.py
└── tasks/             # Background tasks
    └── scheduled_tasks.py
```

## Features

- 📸 **Receipt OCR**: Scan receipts with OpenAI Vision API
- 🥗 **Nutrition Tracking**: Automatic nutrition data extraction
- 🏠 **Virtual Pantry**: Track ingredients with expiration dates
- ⚖️ **Delivery Comparison**: Compare delivery vs home cooking
- 📊 **Analytics**: Spending, calories, waste, and savings tracking
- 🔔 **Smart Notifications**: Expiration alerts and budget warnings
- 🔐 **Firebase Auth**: Secure authentication and data storage

## Development

### Adding New Endpoints

1. Create model in `models/` if needed
2. Add business logic to `services/`
3. Create router in `router/`
4. Register router in `main.py`

### Testing

```bash
# Install dev dependencies
pip install pytest httpx

# Run tests
pytest
```

## Deployment

### Using Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t aristos-backend .
docker run -p 8000:8000 --env-file .env aristos-backend
```

### Cloud Deployment

- **Google Cloud Run**: Native FastAPI deployment
- **AWS Lambda**: Use Mangum adapter
- **Heroku**: Add `Procfile` with uvicorn command
- **Railway/Render**: Auto-deploy from GitHub

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| OPENAI_API_KEY | OpenAI API key | Yes |
| FIREBASE_CREDENTIALS_PATH | Path to Firebase credentials | Yes |
| FIREBASE_PROJECT_ID | Firebase project ID | Yes |
| JWT_SECRET | Secret for JWT tokens | Yes |
| EXPO_PUSH_ACCESS_TOKEN | Expo push notification token | No |
| ENVIRONMENT | development/production | No |

## Troubleshooting

### Firebase Connection Issues
- Verify credentials file exists and is valid
- Check Firebase project ID matches
- Ensure Firestore is enabled in Firebase Console

### OpenAI API Errors
- Verify API key is correct
- Check account has credits
- Ensure you have access to GPT-4 Vision

### CORS Issues
- Update CORS origins in `main.py`
- Add your frontend URL to allowed origins

## License

MIT
