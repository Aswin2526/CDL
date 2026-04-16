# Pokhara Hub — Phase 2 Setup Guide

Authentication & user management with **Django REST Framework**, **JWT**, **XAMPP MySQL**, and **React**.

---

## Prerequisites

- XAMPP running (MySQL started in Control Panel)
- Python 3.11+ with project virtualenv
- Node.js 20+

---

## Step 1 — Create MySQL database (XAMPP)

**Run in:** Command Prompt or PowerShell (any folder)

```powershell
C:\xampp\mysql\bin\mysql.exe -u root -e "CREATE DATABASE IF NOT EXISTS PokharaHub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

Or use **phpMyAdmin** → SQL tab:

```sql
CREATE DATABASE IF NOT EXISTS PokharaHub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Credentials (in `backend/.env`):**

| Setting  | Value        |
| -------- | ------------ |
| HOST     | localhost    |
| PORT     | 3306         |
| USER     | root         |
| PASSWORD | *(empty)*    |
| DATABASE | PokharaHub   |

---

## Step 2 — Backend setup

**Run in:** `Pokhara Hub/backend/`

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy environment (if needed):

```powershell
copy .env.example .env
```

Ensure `.env` has `USE_MYSQL=True` and `DB_NAME=PokharaHub`.

**Run migrations:**

```powershell
python manage.py migrate
```

**Create admin superuser (interactive):**

```powershell
python manage.py createsuperuser
```

Or use the pre-created test admin:

- **Email:** `admin@pokharahub.com`
- **Password:** `Admin@12345`

**Start backend:**

```powershell
python manage.py runserver
```

- API: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## Step 3 — Frontend setup

**Run in:** `Pokhara Hub/frontend/`

```powershell
cd frontend
npm install
npm run dev
```

- App: http://localhost:5173/

---

## API Endpoints (Phase 2)

| Method | URL | Auth | Description |
| ------ | --- | ---- | ----------- |
| POST | `/api/users/register/` | No | Register customer or vendor |
| POST | `/api/users/login/` | No | Login (returns JWT) |
| POST | `/api/users/token/refresh/` | No | Refresh access token |
| POST | `/api/users/logout/` | Yes | Logout |
| GET/PATCH | `/api/users/profile/` | Yes | View/update profile |
| POST | `/api/users/profile/image/` | Yes | Upload profile image |

**Login body:**

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Register body (customer):**

```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "password": "securepass123",
  "role": "customer",
  "phone_number": "9800000000",
  "address": "Pokhara"
}
```

**Register body (vendor):**

```json
{
  "full_name": "Shop Owner",
  "email": "vendor@example.com",
  "password": "securepass123",
  "role": "vendor",
  "shop_name": "Lake Side Store",
  "address": "Lakeside, Pokhara"
}
```

---

## XAMPP / MariaDB 10.4 note

XAMPP ships MariaDB 10.4. The project uses a custom Django DB backend (`config.db`) so migrations work with XAMPP. Connection uses **PyMySQL** (same as mysqlclient for Django).

---

## Frontend routes

| Route | Role |
| ----- | ---- |
| `/login` | Public |
| `/register` | Public |
| `/admin/dashboard` | Admin |
| `/vendor/dashboard` | Vendor |
| `/customer/home` | Customer |

JWT tokens are stored in `localStorage` and sent via Axios `Authorization: Bearer` header.
