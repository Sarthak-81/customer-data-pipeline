# Backend Data Pipeline Assessment

## Overview

This project implements a simple data pipeline using Flask, FastAPI, and PostgreSQL.

* Flask acts as a mock data provider (serves customer data from JSON)
* FastAPI handles ingestion and exposes APIs
* PostgreSQL stores the data
* Docker is used to run everything in a consistent environment

---

## Architecture

Flask (Mock API) → FastAPI (Ingestion Service) → PostgreSQL

---

## Getting Started

### Prerequisites

* Docker Desktop installed and running

### Run the project

```bash
docker compose up --build
```

---

## API Endpoints

### Mock Server (Flask)

* `GET /api/customers?page=1&limit=10`
* `GET /api/customers/{id}`
* `GET /api/health`

### Pipeline Service (FastAPI)

* `POST /api/ingest` → Fetches data from Flask and stores in DB
* `GET /api/customers` → Paginated data from DB
* `GET /api/customers/{id}` → Single customer

---

## How ingestion works

* Fetches data from Flask in pages
* Iterates through all records
* Inserts new customers
* Updates existing ones (upsert logic)

---

## Notes

* Data is loaded from a JSON file (not hardcoded)
* Pagination is supported in both services
* Basic error handling is included

---

## Tech Stack

* Python (Flask, FastAPI)
* PostgreSQL
* SQLAlchemy
* Docker & Docker Compose
