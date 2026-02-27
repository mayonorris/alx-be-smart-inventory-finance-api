# ALX BE – Smart Inventory and Financial Tracking API

## Overview

The **Smart Inventory and Financial Tracking API** is a modular Django REST Framework backend application designed to manage inventory operations while integrating core financial logic.

This project was built as part of the **ALX Backend Capstone Project**, with a focus on:

- Clean architecture
- Transaction-based stock management
- Financial accuracy
- Scalable design
- Real-world business logic implementation

The system connects operational inventory management with financial insights such as Cost of Goods Sold (COGS), inventory valuation, and profit tracking.

---

## Problem Statement

Small and medium-sized businesses often struggle to:

- Track real-time stock levels
- Prevent stockouts and overstocking
- Calculate accurate inventory valuation
- Determine profitability from sales transactions

This API addresses these challenges by implementing structured inventory transactions and financial computation logic.

---

## Key Features

### Authentication & Authorization

- JWT-based authentication
- Role-based permissions (Admin / Staff)

### Inventory Management

- Product & Category management
- Supplier & Customer management
- Stock quantity tracking
- Reorder level monitoring

### Transaction-Based Stock System

- Purchase (IN)
- Sale (OUT)
- Adjustment (ADJUST)
- Automatic stock updates
- Negative stock prevention

### Financial Logic

- Weighted Average Cost calculation
- Cost of Goods Sold (COGS)
- Inventory Valuation endpoint
- Profit reporting endpoint

### Reporting Endpoints

- Stock summary
- Inventory valuation
- Low stock alerts
- Profit report (date-range based)

---

## Architecture

The project follows a layered architecture:

### Django Apps Structure

| App          | Responsibility                   |
| ------------ | -------------------------------- |
| accounts     | Authentication & permissions     |
| inventory    | Products, categories, stock      |
| partners     | Suppliers & customers            |
| transactions | Stock movement & financial logic |
| reports      | Financial & inventory reporting  |

Financial rules are encapsulated within the **service layer**, ensuring separation of concerns and maintainability.

---

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL (or SQLite for development)
- SimpleJWT
- django-filter

---

## Database Design Highlights

- Normalized schema
- Indexed SKU field
- Transaction-based stock tracking
- Decimal-based financial fields
- Foreign key constraints
- Prevents negative inventory

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/alx-be-smart-inventory-finance-api.git
cd alx-be-smart-inventory-finance-api
```
