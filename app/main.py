import sqlite3, os
from typing import Optional

import psycopg2 as psycopg2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Students(BaseModel):
    name: str
    grade: int
    email: str
    graduated: Optional[bool] = True


class Product(BaseModel):
    name: str
    price: int
    is_sale: Optional[bool] = False


try:
    conn = psycopg2.connect(host='localhost', database='crud', user='postgres', password='pass123',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful!")
except Exception as error:
    print("Failed to connect to database")
    print(f"Error: {error}")


@app.get("/products/{prod_id}")
def get_product(prod_id, response: Response):
    cursor.execute("SELECT * FROM products where id = %s", [prod_id])
    product = cursor.fetchone()
    print(product)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The student with the id: {prod_id} was not found')
    return product


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    """cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()"""
    products = db.query(models.Products).all()
    return products


@app.get("/testing")
def test(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products


'''list_accumulator = []
    for item in values:
        list_accumulator.append({k: item[k] for k in item.keys()})
    return list_accumulator
    '''

'''@app.post("/student")
def write(payload: dict = Body(...)):   # Can use a list here too
    name = payload['Name']
    grade = payload['Grade']
    email = payload['Email']
    print(f"{name} {grade} {email}")
    conn = sqlite3.connect("sample.db")

    conn.execute("insert into Student (Name,Grade,Email) Values(?,?,?)", (name, grade, email))
    conn.commit()

    conn.close()
    return "Succesfully created"
'''


@app.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(product: Product, db: Session = Depends(get_db)):
    new_product = models.Products(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    '''data = product.dict()
    name = data['name']
    price = data['price']
    is_sale = data['is_sale']
    cursor.execute("INSERT INTO products (name,price,is_sale) Values(%s,%s,%s) RETURNING *", (name, price, is_sale))
    new_product = cursor.fetchone()
    conn.commit()'''
    return new_product


@app.delete('/products/{prod_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(prod_id: int):
    cursor.execute("DELETE FROM products where id = %s RETURNING *", [str(prod_id)])
    product = cursor.fetchone()
    print(product)
    conn.commit()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The student with the id: {prod_id} was not found')
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/products/{prod_id}', status_code=status.HTTP_200_OK)
def update_product(prod_id: int, product: Product):
    name = product.name
    price = product.price
    is_sale = product.is_sale

    cursor.execute("UPDATE products SET name = %s, Price = %s, is_sale= %s where ID = %s RETURNING *",
                   (name, price, is_sale, str(prod_id)))
    value = cursor.fetchone()
    conn.commit()
    if value is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The student with the id: {prod_id} was not found')
    else:
        return {'message': 'successfully updated'}
