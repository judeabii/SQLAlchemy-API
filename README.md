# SQLAlchemy-API
Explore the power of modern web development with this project that combines FASTAPI, a high-performance web framework for building APIs, and SQLAlchemy, a versatile SQL toolkit and ORM.
### FastAPI
FastAPI is a modern, high-performance, and easy-to-use web framework for building APIs with Python.

### SQLAlchemy
SQLAlchemy is an open-source SQL toolkit and Object-Relational Mapping (ORM) library for the Python programming language.

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