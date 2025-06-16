import os
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100))
    phone = Column(String(20))
    role = Column(String(10))  # 'lister' or 'viewer'
    language = Column(String(5), default='en')
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(100))
    description = Column(String(500))
    address = Column(String(200))
    price = Column(Float)
    main_image = Column(String(200))
    additional_images = Column(String(500))  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

def init_db():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_db_session():
    engine = init_db()
    Session = sessionmaker(bind=engine)
    return Session()
