from fastapi import FastAPI, HTTPException
import requests
from database import Base, engine, SessionLocal
from models.customer import Customer
from datetime import datetime
from services.ingestion import ingest_customers

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# Serializer 
def serialize(customer):
    return {
        "customer_id": customer.customer_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address,
        "date_of_birth": str(customer.date_of_birth),
        "account_balance": float(customer.account_balance),
        "created_at": str(customer.created_at)
    }


@app.get("/")
def home():
    return {"message": "FastAPI running"}


# INGEST DATA
@app.post("/api/ingest")
def ingest():
    db = SessionLocal()

    try:
        total = ingest_customers(db)
        return {
            "status": "success",
            "records_processed": total
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()

# GET ALL CUSTOMERS
@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    db = SessionLocal()

    offset = (page - 1) * limit

    customers = db.query(Customer).offset(offset).limit(limit).all()
    total = db.query(Customer).count()

    db.close()

    return {
        "data": [serialize(c) for c in customers],
        "total": total,
        "page": page,
        "limit": limit
    }


# GET SINGLE CUSTOMER
@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db = SessionLocal()

    customer = db.query(Customer).filter_by(
        customer_id=customer_id
    ).first()

    db.close()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return serialize(customer)
