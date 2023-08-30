# SQLAlchemy-API
Explore the power of modern web development with this project that combines FASTAPI, a high-performance web framework for building APIs, and SQLAlchemy, a versatile SQL toolkit and ORM.
### FastAPI
FastAPI is a modern, high-performance, and easy-to-use web framework for building APIs with Python.

### SQLAlchemy
SQLAlchemy is an open-source SQL toolkit and Object-Relational Mapping (ORM) library for the Python programming language.

### Pre-Requisites
```commandline
pip install sqlalchemy
pip install fastapi[all]
pip install passlib[bcrypt]
```

## Connecting to a Database using SQLAlchemy
```commandline
SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database-name>"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # engine is responsible for the connection to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # To talk to the database, we need to make use of a session

Base = declarative_base() # All models we use to create tables will reference this Base class
```

## Using Python models to create tables
Creating a table called _products_ in the Postgres database using an ORM. In this example, SQLAlchemy.
More columns can be added.
```commandline
from app.database import Base

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
```
Another table called _users_ to store information about the Users.
```commandline
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
```
Note that all to create any table, the class has to inherit the `Base` class

In order to create the tables in Postgres using the DB connections via SQLAlchemy, we use the below line
```commandline
models.Base.metadata.create_all(bind=engine)
```
### Database Operations (CRUD)
To perform any operation on a database, we first have to open a session to the database, and after the operation, close the session.
Function to create a session and close:
```commandline
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
We can use this function to establish sessions: `db: Session = Depends(get_db)`

#### Read
```commandline
@app.get("/products", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Products).all()
    return products
```
#### Write
```commandline
@app.post("/products", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def add_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    new_product = models.Products(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
```

### Hashing user passwords
`from passlib.context import CryptContext`

Now we have to tell passlib what _hashing algorithm_ do we want to use. 
In our case it will be *Bcrypt*

` pwd_context = CryptContext(schemes=["bcrypt"], depreciated="auto")`

To actually hash the password:
```commandline
hashed_password = pwd_context.hash(user.password)
user.password = hashed_password # Updating the password value from payload   with hashed password
```