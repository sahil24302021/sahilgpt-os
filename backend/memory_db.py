import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime
import os

# Define database path
DB_PATH = "data/memory.db"
DB_URL = f"sqlite:///{DB_PATH}"

# Ensure the data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# SQLAlchemy setup
engine = db.create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Memory table model
class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(String, nullable=False)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

def get_db():
    """Generator to get a database session."""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

def add_memory(content: str):
    """Adds a new memory entry to the database."""
    db_session = next(get_db())
    new_memory = Memory(content=content)
    db_session.add(new_memory)
    db_session.commit()
    db_session.refresh(new_memory)
    db_session.close()
    return new_memory

def list_memories(limit: int = 50):
    """Retrieves the most recent memories from the database."""
    db_session = next(get_db())
    memories = db_session.query(Memory).order_by(Memory.timestamp.desc()).limit(limit).all()
    db_session.close()
    return memories
    