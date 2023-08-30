from app import models, schemas, utils
from app.database import get_db
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix="/products"
)


@router.get("/{prod_id}", response_model=schemas.Product)
def get_product(prod_id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == prod_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The product with the id: {prod_id} was not found')
    return product


@router.get("/", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def add_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    new_product = models.Products(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.delete('/{prod_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(prod_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == prod_id)
    if product.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The product with the id: {prod_id} was not found')
    else:
        product.delete(synchronize_session='fetch')
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{prod_id}', response_model=schemas.Product)
def update_product(prod_id: int, product: schemas.CreateProduct, db: Session = Depends(get_db)):
    updated_product = db.query(models.Products).filter(models.Products.id == prod_id)
    if updated_product.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The product with the id: {prod_id} was not found')
    else:
        updated_product.update(product.dict(), synchronize_session="fetch")
        db.commit()
        return updated_product.first()