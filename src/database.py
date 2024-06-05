from sqlalchemy import create_engine, Column, Integer, String, Float, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'SQLITE:///data/menu_items.db' 
engine = create_engine(DATABASE_URI)
Base = declarative_base()

class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def store_items(items_prices):
    for item, price in items_prices:
        menu_item = MenuItem(name=item, price=float(price))
        session.add(menu_item)
    session.commit()