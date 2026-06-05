# Inventory Order Management System

Full-stack inventory and order management app using FastAPI, React, PostgreSQL, Alembic, and Docker.

## Features

- Product CRUD with unique SKU validation
- Customer CRUD with unique email validation
- Order creation with inventory validation
- Automatic product stock reduction after successful order placement
- PostgreSQL schema migrations with Alembic
- Docker Compose for database, backend, and frontend
- Environment-variable based configuration

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Pydantic, Alembic
- Frontend: React, Vite, lucide-react
- Database: PostgreSQL
- Containers: Docker, Docker Compose

## Run With Docker

```bash
cp .env.example .env
docker compose up --build
```

Services:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

The backend container runs `alembic upgrade head` automatically before starting FastAPI.

## Run Locally Without Docker

Start PostgreSQL and create a database named `inventory_db`, then:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/inventory_db"
alembic upgrade head
uvicorn app.main:app --reload
```

In another terminal:

```bash
cd frontend
npm install
VITE_API_URL=http://localhost:8000/api npm run dev
```

## API Endpoints

- `GET /api/products/`
- `POST /api/products/`
- `GET /api/products/{product_id}`
- `PUT /api/products/{product_id}`
- `DELETE /api/products/{product_id}`
- `GET /api/customers/`
- `POST /api/customers/`
- `GET /api/customers/{customer_id}`
- `PUT /api/customers/{customer_id}`
- `DELETE /api/customers/{customer_id}`
- `GET /api/orders/`
- `POST /api/orders/`
- `GET /api/orders/{order_id}`

## Deployment

Free hosting option:

- Database: Render PostgreSQL or Neon
- Backend: Render Web Service using `backend/Dockerfile`
- Frontend: Vercel or Netlify from `frontend/`
- Docker image: push backend image to Docker Hub

Set these environment variables on the hosted services:

- Backend: `DATABASE_URL`, `BACKEND_CORS_ORIGINS`, `ENVIRONMENT`
- Frontend: `VITE_API_URL`

Submission placeholders:

- GitHub repository: add your GitHub repo URL
- Docker image: add your Docker Hub image URL
- Backend live URL: add your deployed API URL
- Frontend live URL: add your deployed frontend URL
