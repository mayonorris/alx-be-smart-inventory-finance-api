# Smart Inventory & Financial Tracking API

A Django REST Framework backend for managing inventory operations with integrated financial logic.

Built as the **ALX Backend Capstone Project** by **Norris KADANGA**.

---

## What It Does

Small businesses struggle to track stock levels, prevent stockouts, and calculate profitability accurately. This API solves that by combining inventory management with financial computation:

- Track products, categories, suppliers, and customers
- Record stock movements (purchases, sales, adjustments)
- Automatically calculate **Weighted Average Cost** on every purchase
- Prevent negative inventory on sales
- Generate financial reports: inventory valuation, COGS, gross profit, profit margin

---

## Tech Stack

- Python 3.10
- Django 5.x
- Django REST Framework
- PostgreSQL
- SimpleJWT (JWT authentication)
- django-filter
- drf-spectacular (Swagger docs)
- django-cors-headers

---

## Project Structure

```
├── smart_inventory_api/   # Django config (settings, urls, wsgi)
├── accounts/              # Custom user model, JWT auth, role permissions
├── inventory/             # Products & categories
├── partners/              # Suppliers & customers
├── transactions/          # Stock movements + financial service layer
├── reports/               # Financial & inventory reporting
├── manage.py
├── requirements.txt
└── .env.example
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/mayonorris/alx-be-smart-inventory-finance-api.git
cd alx-be-smart-inventory-finance-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL

```bash
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE smart_inventory_db;"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'yourpassword';"
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your DB credentials
```

### 5. Run migrations

```bash
python3 manage.py migrate
```

### 6. Seed the database with sample data

```bash
python3 manage.py seed_data
```

This creates 8 products, 2 suppliers, 2 customers, and sample transactions.
Demo credentials: `admin@example.com / password123`

### 7. Start the server

```bash
python3 manage.py runserver
```

---

## API Documentation

Interactive Swagger docs available at:

```
http://127.0.0.1:8000/api/docs/
```

Click **Authorize** and paste your JWT access token to test endpoints directly in the browser.

---

## API Endpoints

### Authentication

| Method | Endpoint            | Auth   | Description           |
| ------ | ------------------- | ------ | --------------------- |
| POST   | /api/auth/register/ | Public | Create new account    |
| POST   | /api/auth/login/    | Public | Login, get JWT tokens |
| POST   | /api/auth/refresh/  | Public | Refresh access token  |
| GET    | /api/auth/me/       | Auth   | Current user profile  |

### Inventory

| Method         | Endpoint            | Auth        | Description               |
| -------------- | ------------------- | ----------- | ------------------------- |
| GET/POST       | /api/products/      | Staff/Admin | List or create products   |
| GET/PUT/DELETE | /api/products/{id}/ | Staff/Admin | Product detail            |
| GET/POST       | /api/categories/    | Staff/Admin | List or create categories |

### Partners

| Method   | Endpoint        | Auth        | Description              |
| -------- | --------------- | ----------- | ------------------------ |
| GET/POST | /api/suppliers/ | Staff/Admin | List or create suppliers |
| GET/POST | /api/customers/ | Staff/Admin | List or create customers |

### Transactions

| Method | Endpoint           | Auth        | Description              |
| ------ | ------------------ | ----------- | ------------------------ |
| POST   | /api/transactions/ | Staff/Admin | Record IN / OUT / ADJUST |
| GET    | /api/transactions/ | Staff/Admin | List with filters        |

Filters: `?type=IN`, `?date_from=2026-01-01`, `?date_to=2026-12-31`

### Reports

| Method | Endpoint                          | Auth        | Description                   |
| ------ | --------------------------------- | ----------- | ----------------------------- |
| GET    | /api/reports/stock-summary/       | Staff/Admin | Stock per product             |
| GET    | /api/reports/inventory-valuation/ | Staff/Admin | Total inventory value         |
| GET    | /api/reports/low-stock/           | Staff/Admin | Products below reorder level  |
| GET    | /api/reports/profit/              | Admin only  | Profit report with date range |

---

## Key Financial Logic

### Weighted Average Cost (WAC)

Every purchase (IN transaction) recalculates the unit cost:

```
new_avg = (current_stock × current_cost + new_qty × new_cost)
          ÷ (current_stock + new_qty)
```

### Gross Profit

```
Revenue = Σ (quantity × unit_price) for all sales
COGS    = Σ (quantity × unit_cost)  for all sales
Profit  = Revenue - COGS
Margin  = (Profit / Revenue) × 100
```

### Stock Status

- **ok** — stock > reorder_level × 1.5
- **warning** — stock ≤ reorder_level × 1.5
- **critical** — stock ≤ reorder_level

---

## Roles & Permissions

| Action                        | Admin | Staff |
| ----------------------------- | ----- | ----- |
| Register/Login                | ✅    | ✅    |
| View products, stock, reports | ✅    | ✅    |
| Create transactions           | ✅    | ✅    |
| Create/edit products          | ✅    | ❌    |
| Delete suppliers/customers    | ✅    | ❌    |
| Access profit report          | ✅    | ❌    |

---

## Running Tests

```bash
python3 manage.py test
```

40 tests across all apps — WAC calculations, stock mutations, permissions, and API behavior.

---

## Author

**Norris KADANGA**
Backend Developer | ALX Backend Program — Capstone Project
EOF
