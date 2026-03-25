import requests
from datetime import datetime
from models.customer import Customer


def ingest_customers(db):
    page = 1
    limit = 10
    total_processed = 0

    while True:
        response = requests.get(
            f"http://mock-server:5000/api/customers?page={page}&limit={limit}"
        )

        if response.status_code != 200:
            raise Exception("Failed to fetch data from mock server")

        payload = response.json()
        customers = payload.get("data", [])

        if not customers:
            break

        for item in customers:
            existing_customer = db.query(Customer).filter_by(
                customer_id=item["customer_id"]
            ).first()

            if existing_customer:
                # update
                existing_customer.first_name = item["first_name"]
                existing_customer.last_name = item["last_name"]
                existing_customer.email = item["email"]
                existing_customer.phone = item.get("phone")
                existing_customer.address = item.get("address")
                existing_customer.date_of_birth = datetime.fromisoformat(item["date_of_birth"])
                existing_customer.account_balance = item["account_balance"]
                existing_customer.created_at = datetime.fromisoformat(item["created_at"])
            else:
                # insert
                new_customer = Customer(
                    customer_id=item["customer_id"],
                    first_name=item["first_name"],
                    last_name=item["last_name"],
                    email=item["email"],
                    phone=item.get("phone"),
                    address=item.get("address"),
                    date_of_birth=datetime.fromisoformat(item["date_of_birth"]),
                    account_balance=item["account_balance"],
                    created_at=datetime.fromisoformat(item["created_at"])
                )
                db.add(new_customer)

            total_processed += 1

        db.commit()
        print(f"[INGEST] Page {page} processed | Total records: {total_processed}")

        page += 1

    return total_processed