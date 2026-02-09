
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from models import Base

DATABASE_URL = 'sqlite:///database.db' # Put it in the '.env'

engine = create_engine(DATABASE_URL)

# Make a Varible so when i call it it make a session
Session_db = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
) 

# You call this function when making the endpoint function in FastAPI --> (@app.post('...'))
# database session dependency function for FastAPI
def get_db()->Generator[Session,None,None]:
    """
    Database session dependency for FastAPI
    This create a db sesssion and then make sure it's closed
    
    Yields:
        Session: A SQLAlchemy session object.
    """
    db = Session_db() # Create a new database session
    try:
        yield db # Provide the session to the endpoint
    finally:
        db.close() # Always close the session when done

# Initialize database tables if needed
def init_database():
    """ Initialize database tables. """
    Base.metadata.create_all(bind=engine)

def shutdown_database():
    """ Shutdown database connections. """
    engine.dispose()