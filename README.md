# ChitraBazar

Online painting gallery and e-commerce platform — a single store for original artworks.

## Tech Stack

| Layer      | Technology                          |
| ---------- | ----------------------------------- |
| Backend    | Django, Django REST Framework       |
| Frontend   | React, Vite, Tailwind CSS           |
| Database   | MySQL (SQLite for local dev default) |
| API Client | Axios                               |
| Routing    | React Router                        |

## Project Structure

```
Foodie/
├── backend/          # Django API
├── frontend/         # React (Vite) client
└── README.md
```

## Prerequisites

- Python 3.11+
- Node.js 20+ and npm
- MySQL 8+ (optional — SQLite used by default)

---

## Backend Setup

**Run all commands from:** `backend/`

### 1. Create & activate virtual environment

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and update values (especially `DB_PASSWORD` when using MySQL).

### 4. Run migrations

```powershell
python manage.py migrate
```

### 5. Seed painting catalog (demo)

```powershell
python manage.py seed_catalog --clear
```

Creates landscape, portrait, abstract, still life, and contemporary categories with sample original paintings.

**Demo admin:** create via `python manage.py createsuperuser` (role: admin in Django admin)

### 6. Start development server

```powershell
python manage.py runserver
```

API base: `http://127.0.0.1:8000/`  
Admin: `http://127.0.0.1:8000/admin/`

---

## Frontend Setup

**Run all commands from:** `frontend/`

```powershell
cd frontend
npm install
npm run dev
```

App: `http://localhost:5173/`

---

## Features

| Area | Description |
| ---- | ----------- |
| Gallery | Browse paintings by style, medium, price, and rating |
| Artwork detail | Artist name, medium, dimensions, framing, year, reviews |
| Wishlist | Save artworks for later (authenticated collectors) |
| Roles | Collectors (customers) and admins |

### Painting-specific product fields

- `artist_name`, `medium` (oil, acrylic, watercolor, etc.)
- `dimensions`, `is_framed`, `year_created`

### API query params (listing)

`q`, `category`, `medium`, `min_price`, `max_price`, `min_rating`, `sort`, `page`

---

## Django Apps

| App        | Purpose                          |
| ---------- | -------------------------------- |
| users      | Authentication & profiles        |
| products   | Painting catalog                 |
| orders     | Order processing                 |
| carts      | Shopping cart                    |
| reviews    | Collector reviews & ratings      |
| analytics  | Reports & dashboards             |

## Frontend Routes

| Path | Page |
| ---- | ---- |
| `/` | Homepage (hero, styles, featured, new arrivals) |
| `/shop` | Gallery listing + filters |
| `/products/:slug` | Artwork detail + reviews |
| `/wishlist` | Saved artworks (login required) |

---

## License

Educational / internship project.
