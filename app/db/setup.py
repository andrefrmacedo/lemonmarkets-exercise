from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:password@localhost:5432"

engine = create_engine(DATABASE_URL)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
