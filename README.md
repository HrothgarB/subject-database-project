# Subject Database Project (MVP)

Secure internal subject-management platform with:
- **Flutter mobile app** (offline-first queue + encrypted local cache)
- **FastAPI backend** (RBAC, JWT auth, audit logging)
- **PostgreSQL schema** (subjects, encounters, photos, users, audits)
- **Encrypted object storage integration point** for photos

## Architecture Overview

### Backend (`backend/`)
- `app/main.py`: FastAPI bootstrap and middleware wiring.
- `app/api/routes/`: Auth, subjects/search, encounter, and photo upload endpoints.
- `app/api/deps.py`: OAuth2 token parsing and permission checks.
- `app/models/entities.py`: SQLAlchemy models.
- `app/middleware/audit.py`: Audit logging for create/read/update/export related paths.
- `app/services/crypto.py`: SSN field encryption placeholder (replace with KMS envelope encryption).
- `alembic/versions/20260318_0001_initial_schema.py`: Initial migration.
- `scripts/seed_data.py`: Seed admin + sample subject.

### Mobile (`flutter_app/`)
- Screens: login, subject list/search, subject detail, subject create/edit, encounter entry.
- `LocalSyncService`: encrypted local storage (Hive AES box) + sync queue.
- `SubjectApiService`: API client scaffolding.
- `AuthService`: secure token storage with `flutter_secure_storage`.

## Security-Minded Defaults
- JWT bearer auth with role-based permissions (`admin`, `analyst`, `officer`).
- Explicit permission checks (`subject:read`, `subject:write`, etc.).
- Restricted SSN stored only as encrypted/ciphertext derivative.
- Audit logs capture path, method, actor, action, and status.
- Object storage access represented via generated object keys (designed for least-privilege service accounts).
- Assumes TLS termination in internal infrastructure.

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

## PostgreSQL Schema
Implemented through Alembic migration with these tables:
- `users`
- `subjects`
- `subject_photos`
- `encounters`
- `audit_logs`

## Local Development Setup

### 1) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` (optional):
```env
SUBJECT_DATABASE_URL=postgresql+psycopg://subject:subject@localhost:5432/subjectdb
SUBJECT_JWT_SECRET=replace-this
```

Run migrations + seed:
```bash
alembic upgrade head
python -m scripts.seed_data
```

Run API:
```bash
uvicorn app.main:app --reload --port 8000
```

### 2) Flutter app
```bash
cd flutter_app
flutter pub get
flutter run
```

## Production Notes / Next Steps
- Replace SSN hashing placeholder with audited field-level encryption using KMS + key rotation.
- Implement refresh-token rotation, revocation lists, and device binding.
- Add object storage signed-upload endpoint and malware/image validation pipeline.
- Expand admin module for user/device management and policy enforcement.
- Add integration tests (API + mobile sync conflict handling).
