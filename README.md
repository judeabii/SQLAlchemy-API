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
