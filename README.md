# DriftDater — INFO3180 Group Project

A full-stack dating web application built with Vue 3 and Flask.

---

## Team Members & Roles

| Name | Role |
|------|------|
| *Hector Riettie (620161458)* | Project Manager |
| *Jordan Graham (620172528)* | Backend Lead |
| *Nicole Johnson (620156645)* | Frontend Lead |
| *Ruth-Ann Allen (620161125)* | QA/Testing Lead |
| *Alexander Waite (620165566)* | Deployment Lead |

---

## Features

- User registration and secure login (bcrypt password hashing)
- Detailed profile creation with photo upload, interests, and preferences
- Matching algorithm based on location, age range, shared interests, and gender preference
- Like / Dislike / Superlike swipe interface
- Mutual match detection with in-app notifications
- Real-time messaging between matched users (4-second polling)
- Search and discovery with filters (location, age, interests, keyword)
- Bookmark/save favourite profiles
- Dark mode support
- Profile visibility controls (public/private)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3, Vite, Pinia, Vue Router, Tailwind CSS |
| Backend | Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS |
| Database | PostgreSQL (production), SQLite (testing) |
| Auth | Flask sessions + bcrypt |
| Deployment | Render |

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (or use SQLite for local dev)

### Backend

```bash
# 1. Clone the repository
git clone https://github.com/Godsminion777/INFO3180_Group_Project.git
cd INFO3180_Group_Project

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment variables
cp .env.sample .env
# Edit .env — set DATABASE_URL and SECRET_KEY

# 5. Run database migrations
flask --app app db upgrade

# 6. Start backend (runs on http://localhost:8080)
flask --app app --debug run --port 8080
```

### Frontend

```bash
# In a separate terminal
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

---

## Environment Variables

Copy `.env.sample` to `.env` and fill in:

```
FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8080
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/driftdater
CORS_ORIGINS=http://localhost:5173
```

---

## API Documentation

### Authentication — `/api/auth`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login | No |
| POST | `/api/auth/logout` | Logout | No |
| GET | `/api/auth/me` | Get current user | Yes |

**Register payload:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password",
  "first_name": "Jane",
  "last_name": "Doe",
  "age": 25,
  "gender": "female",
  "looking_for": "any",
  "bio": "Optional bio",
  "location": "Kingston, Jamaica",
  "occupation": "Engineer",
  "relationship_goal": "long-term"
}
```

---

### Profiles — `/api/profiles`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/profiles` | Get all public profiles | Yes |
| GET | `/api/profiles/:id` | Get profile by ID | Yes |
| PUT | `/api/profiles/:id` | Update profile | Yes (owner) |
| POST | `/api/profiles/:id/photo` | Upload profile photo | Yes (owner) |

**Update profile payload (all optional):**
```json
{
  "first_name": "Jane",
  "age": 26,
  "bio": "Updated bio",
  "location": "Bridgetown, Barbados",
  "interests": ["hiking", "music", "cooking"],
  "is_public": true,
  "preferred_age_min": 22,
  "preferred_age_max": 35,
  "distance_preference_km": 50
}
```

---

### Matches — `/api/matches`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/matches` | Get mutual matches | Yes |
| GET | `/api/matches/potential` | Get scored potential matches | Yes |
| POST | `/api/matches/action` | Like/Dislike/Superlike a user | Yes |

**Action payload:**
```json
{ "receiver_id": 5, "action": "like" }
```
Actions: `like`, `dislike`, `superlike`

**Potential matches response includes `match_score`** (0–100) based on:
- Age range match (+30)
- Shared interests (+10 each)
- Gender preference match (+20)
- Same location (+20)

---

### Messages — `/api/messages`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/messages/conversations` | List all conversations | Yes |
| GET | `/api/messages/:user_id` | Get conversation with user | Yes |
| POST | `/api/messages` | Send a message | Yes |

**Send message payload:**
```json
{ "receiver_id": 5, "content": "Hello!" }
```
Note: both users must be mutual matches to message each other.

---

## Database Schema

### Tables

| Table | Description |
|-------|-------------|
| `users` | Auth credentials (email, username, password_hash) |
| `profiles` | User profile data (age, bio, location, preferences) |
| `interests` | Interest tags (normalized) |
| `profile_interests` | Many-to-many: profiles ↔ interests |
| `matches` | Like/dislike actions between users |
| `messages` | Messages between matched users |

### Key Relationships
- `users` → `profiles`: one-to-one
- `profiles` ↔ `interests`: many-to-many via `profile_interests`
- `users` → `matches`: one-to-many (as sender and receiver)
- `users` → `messages`: one-to-many (as sender and receiver)

---

## Running Tests

```bash
# From project root with venv activated
pip install pytest
pytest test/ -v
```

---

## Deployed Application

- **Backend API:** *(Add Render URL here)*
- **Frontend:** *(Add deployed URL here)*

---

## Known Issues / Limitations

- Message updates use polling (4s interval) rather than WebSockets
- Search/discovery filtering is client-side (fetches all public profiles)
- Photo uploads stored locally on server (not cloud storage)
- SSL required for PostgreSQL connections on Render (automatic); SQLite used for local testing bypasses SSL

---

## Git Branch Structure

| Branch | Purpose |
|--------|---------|
| `main` | Stable releases |
| `dev/backend` | Flask API development |
| `dev/frontend` | Vue 3 frontend development |
| `dev/deployment` | Render deployment configuration |
| `qa/testing` | Test suite |
