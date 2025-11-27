from sqlalchemy import Column, Integer, String, Float, JSON
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    longDescription = Column(String)
    price = Column(Float)
    image = Column(String)
    category = Column(String, index=True)
    sentiment = Column(JSON)
    dataAiHint = Column(String)
    tags = Column(JSON)
