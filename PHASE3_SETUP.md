# ChitraBazar — Phase 3 Setup Guide

Collector shopping: browse paintings, search, filter by style and medium, reviews, and wishlist.

---

## Backend (`backend/`)

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py seed_catalog --clear
python manage.py runserver
```

### Painting APIs (public)

| Method | URL | Description |
| ------ | --- | ----------- |
| GET | `/api/products/` | List + search/filter/sort/pagination |
| GET | `/api/products/<slug>/` | Artwork detail |
| GET | `/api/products/categories/` | All styles |
| GET | `/api/products/categories/<slug>/products/` | Paintings by style |
| GET | `/api/products/featured/` | Featured artworks |
| GET | `/api/products/latest/` | Latest arrivals |
| GET | `/api/products/top-rated/` | Top rated |

**Query params (listing):** `q`, `category`, `category_id`, `medium`, `vendor`, `min_price`, `max_price`, `min_rating`, `sort` (`latest`|`price_low`|`price_high`|`top_rated`), `page`

### Reviews

| Method | URL | Auth |
| ------ | --- | ---- |
| GET | `/api/reviews/product/<id>/` | No |
| POST | `/api/reviews/product/<id>/add/` | Yes |

### Wishlist

| Method | URL | Auth |
| ------ | --- | ---- |
| GET | `/api/customers/wishlist/` | Yes |
| POST | `/api/customers/wishlist/toggle/` | Yes |
| DELETE | `/api/customers/wishlist/<product_id>/` | Yes |

---

## Frontend (`frontend/`)

```powershell
cd frontend
npm install
npm run dev
```

### Routes

| Path | Page |
| ---- | ---- |
| `/` | Homepage |
| `/shop` | Gallery listing + filters |
| `/products/:slug` | Artwork detail + reviews |
| `/wishlist` | Saved artworks (login required) |

---

## Demo data

`python manage.py seed_catalog --clear` creates 5 painting styles and 12 sample artworks for the **ChitraBazar** single store.

Cart and checkout are **not** included (Phase 4).
