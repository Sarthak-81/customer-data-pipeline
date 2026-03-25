from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")

# 🔥 Retry DB connection
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("✅ Database connected")
        break
    except Exception as e:
        print("⏳ Waiting for DB...")
        time.sleep(3)
else:
    raise Exception("❌ Could not connect to DB")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()