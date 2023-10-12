from sqlalchemy import *

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:203JJmario%40j@localhost:5432/Relational_db'

engine = create_engine(URL_DATABASE)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()