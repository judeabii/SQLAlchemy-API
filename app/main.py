import sqlite3, os
from typing import List

import psycopg2 as psycopg2
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db

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


@app.get("/products/{prod_id}", response_model=schemas.Product)
def get_product(prod_id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == prod_id).first()
    '''cursor.execute("SELECT * FROM products where id = %s", [prod_id])
    product = cursor.fetchone()
    print(product)'''
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The product with the id: {prod_id} was not found')
    return product


@app.get("/products", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    """cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()"""
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


@app.post("/products", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def add_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
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
def delete_product(prod_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == prod_id)
    '''cursor.execute("DELETE FROM products where id = %s RETURNING *", [str(prod_id)])
    product = cursor.fetchone()
    print(product)
    conn.commit()'''
    if product.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The product with the id: {prod_id} was not found')
    else:
        product.delete(synchronize_session='fetch')
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/products/{prod_id}', response_model=schemas.Product)
def update_product(prod_id: int, product: schemas.CreateProduct, db: Session = Depends(get_db)):
    updated_product = db.query(models.Products).filter(models.Products.id == prod_id)
    '''name = product.name
    price = product.price
    is_sale = product.is_sale

    cursor.execute("UPDATE products SET name = %s, Price = %s, is_sale= %s where ID = %s RETURNING *",
                   (name, price, is_sale, str(prod_id)))
    value = cursor.fetchone()
    conn.commit()'''
    if updated_product.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The product with the id: {prod_id} was not found')
    else:
        updated_product.update(product.dict(), synchronize_session="fetch")
        db.commit()
        return updated_product.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def user_registration(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
