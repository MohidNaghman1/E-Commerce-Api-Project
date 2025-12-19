# E-Commerce API Project

## Overview

A full-featured, asynchronous E-Commerce backend built with FastAPI and SQLAlchemy. This project demonstrates scalable architecture using repository and service layers, dependency injection, and modular route organization. It supports core e-commerce operations, analytics, and is ready for production deployment.

## Features

- **User Management**: Create, update, retrieve, and delete users (no registration/authentication implemented)
- **Product Management**: CRUD, filtering, category association
- **Order Management**: Create, update, view, and delete orders
- **Cart System**: Add, update, and remove cart items
- **Reviews**: Product reviews with rating constraints
- **Categories**: Many-to-many product-category relationships
- **Analytics**: Admin endpoints for top-selling products and more
- **Async SQLAlchemy**: High-performance, non-blocking DB operations
- **Repository & Service Pattern**: Clean separation of concerns
- **Dependency Injection**: For database/session management
- **Alembic Migrations**: Versioned schema management

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL (recommended)
- Alembic

## Project Structure

```
E-Commerce_API_Project/
├── models/           # SQLAlchemy ORM models
├── schema/           # Pydantic schemas for validation/response
├── Repositories/     # Data access layer
├── services/         # Business logic layer
├── routes/           # FastAPI routers (endpoints)
├── database/         # DB setup and session
├── dependencies/     # Dependency injection
├── alembic/          # Migrations
├── main.py           # FastAPI app entrypoint
└── README.md         # Project documentation
```

## Database Models

- **User**: id, name, email, hashed_password, role
- **Product**: id, name, price, stock, average_rating
- **Order**: id, user_id, total, status, created_at
- **OrderItem**: id, order_id, product_id, quantity, price
- **Category**: id, name, description
- **Review**: id, product_id, user_id, rating, comment
- **CartItem**: id, user_id, product_id, quantity

## API Endpoints (Examples)

- `/users/` - Create, update, get, delete users
- `/products/` - CRUD, filter products
- `/orders/` - Create, update, get, delete orders
- `/cart/` - Add, update, remove cart items
- `/reviews/` - CRUD reviews, get by product/user
- `/categories/` - CRUD categories
- `/admin/analytics/top-selling-products` - Get top-selling products

## Getting Started

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables** in `.env` (DB credentials, etc.)
4. **Run migrations**:
   ```bash
   alembic upgrade head
   ```
5. **Start the API server**:
   ```bash
   uvicorn main:app --reload
   ```
6. **Access docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Deployment

- Production-ready for Docker, cloud, or bare metal
- Use Alembic for schema migrations
- Environment variables for secrets/configuration
