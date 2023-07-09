from app.database import Base
from sqlalchemy import String, Integer, Boolean, Column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    is_sale = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
