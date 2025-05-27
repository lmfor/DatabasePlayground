import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# read .env into os.environ
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set! Check your .env file.")

# Engine = "socket" to talk to postgres
#             pool_pre_ping=True means make sure the connection is alive before using it
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLoca is a factory for Session objects (transaction scopes)
# Session is a private chat with the database
SessionLocal = sessionmaker(
    autoflush=False,  # have to manually .flush() before .commit()
    autocommit=False, # have to manually .commit()
    bind=engine
)

Base = declarative_base()
# Base is the declarative base class for all models