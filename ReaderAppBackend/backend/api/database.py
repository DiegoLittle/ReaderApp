from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = ""
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://diego:83o2Zw5GKzMQiH923u2OzKBHCZNUw@165.232.156.229:5432/reader_app"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
from sqlalchemy_utils import force_instant_defaults

force_instant_defaults()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()