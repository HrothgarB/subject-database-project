# Subject Database Project (MVP)

Secure internal subject-management platform with:
- Flutter mobile app with offline-first queueing and encrypted local cache
- FastAPI backend with RBAC, JWT auth, and audit logging
- PostgreSQL schema for subjects, encounters, photos, users, and audits
- Encrypted object-storage integration point for photos

## What You Need First

- Android Studio with the Flutter and Dart plugins installed
- Flutter SDK 3.3+ on your PATH
- Python 3.11+ for the backend
- PostgreSQL 15+ running locally or on your network

## Repository Layout

- `backend/`: FastAPI API, migrations, and seed script
- `flutter_app/`: Flutter mobile app

## Android Studio Setup

This repo includes the Flutter app source and the generated Android platform folder. If you ever need to regenerate the Android files, run this once inside `flutter_app/`:

```bash
flutter create --platforms=android .
```

After that, open `flutter_app/` in Android Studio and let it index the project. You can then run the app on an emulator or connected Android device.

Android Studio run tips:

- Emulator: keep `SUBJECT_API_BASE_URL` set to `http://10.0.2.2:8000/api`.
- Physical device: point `SUBJECT_API_BASE_URL` at your computer's LAN IP, such as `http://192.168.1.20:8000/api`.
- In the Run/Debug Configuration, add the same value under additional Dart defines if you are launching from Android Studio instead of the terminal.
- If you import the bundled IDE configs, use `main.dart` for emulator runs and `physical-device` for a phone or tablet on your Wi-Fi network.

## Local Development Setup

### 1) Start the backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `backend/.env` if you want to override defaults:

```env
SUBJECT_DATABASE_URL=postgresql+psycopg://subject:subject@localhost:5432/subjectdb
SUBJECT_JWT_SECRET=replace-this
```

Run migrations and seed the initial user/data set:

```bash
alembic upgrade head
python -m scripts.seed_data
```

Start the API:

```bash
uvicorn app.main:app --reload --port 8000
```

### 2) Open and run the Flutter app

```bash
cd flutter_app
flutter pub get
flutter run
```

For Android emulators, the app defaults to:

```bash
http://10.0.2.2:8000/api
```

If you need to override the API URL, pass a Dart define when launching:

```bash
flutter run --dart-define=SUBJECT_API_BASE_URL=http://10.0.2.2:8000/api
```

For a physical Android device, use your machine or server IP instead of `10.0.2.2`.
You can also launch the same Flutter target from Android Studio after opening `flutter_app/`.

## First Login / User Setup

The seed script creates a default admin account and sample subject so the app has something to log into on first run.

Default login:

- Email: `admin@agency.local`
- Password: `Password!123`

The login screen is prefilled with those values. After signing in, you should land on the subject list screen.

If you want a different initial user, update `backend/scripts/seed_data.py` and rerun the seed step:

```bash
python -m scripts.seed_data
```

## API Endpoints (MVP)

### Auth

- `POST /api/auth/login`

### Subjects + Search

- `POST /api/subjects`
- `GET /api/subjects?q=<query>&case_number=<id>&intel_number=<id>`
- `GET /api/subjects/{subject_id}`
- `PATCH /api/subjects/{subject_id}`
- `GET /api/subjects/{subject_id}/export`

### Encounters

- `POST /api/subjects/{subject_id}/encounters`
- `GET /api/subjects/{subject_id}/encounters`

### Photos

- `POST /api/photos/subjects/{subject_id}`

## Architecture Overview

### Backend (`backend/`)

- `app/main.py`: FastAPI bootstrap and middleware wiring
- `app/api/routes/`: Auth, subjects/search, encounter, and photo upload endpoints
- `app/api/deps.py`: OAuth2 token parsing and permission checks
- `app/models/entities.py`: SQLAlchemy models
- `app/middleware/audit.py`: Audit logging for create/read/update/export related paths
- `app/services/crypto.py`: SSN field encryption placeholder
- `alembic/versions/20260318_0001_initial_schema.py`: Initial migration
- `scripts/seed_data.py`: Seeds the admin user and sample subject

### Mobile (`flutter_app/`)

- Screens for login, subject list/search, subject detail, subject create/edit, and encounter entry
- `LocalSyncService`: encrypted local storage with Hive AES boxes plus sync queue
- `SubjectApiService`: API client for subject retrieval and creation
- `AuthService`: secure token storage with `flutter_secure_storage`

## Security-Minded Defaults

- JWT bearer auth with role-based permissions (`admin`, `analyst`, `officer`)
- Explicit permission checks like `subject:read` and `subject:write`
- Restricted SSN stored only as encrypted ciphertext
- Audit logs capture path, method, actor, action, and status
- Object-storage access is designed around generated object keys and least-privilege service accounts
- Assumes TLS termination in internal infrastructure

## PostgreSQL Schema

Implemented through Alembic migration with these tables:

- `users`
- `subjects`
- `subject_photos`
- `encounters`
- `audit_logs`

## Production Notes / Next Steps

- Replace SSN hashing placeholder with audited field-level encryption using KMS and key rotation
- Implement refresh-token rotation, revocation lists, and device binding
- Add object-storage signed-upload endpoint and malware/image validation pipeline
- Expand admin tooling for user/device management and policy enforcement
- Add integration tests for API behavior and mobile sync conflict handling
