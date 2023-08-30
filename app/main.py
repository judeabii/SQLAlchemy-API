import psycopg2 as psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine
from app.routers import users, products

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
    conn = psycopg2.connect(host='localhost', database='crud', user='postgres', password='pass123',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful!")
except Exception as error:
    print("Failed to connect to database")
    print(f"Error: {error}")


app.include_router(users.router)
app.include_router(products.router)