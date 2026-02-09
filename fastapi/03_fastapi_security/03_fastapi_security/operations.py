from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models import User,Role

from email_validator import (
    EmailNotValidError,
    validate_email,
)
import bcrypt

# Transform password into hash
def get_password_hash(password: str)-> str:
    """
    Hahsing the password using bcrypt
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# This function used for createing and adding a new user in the Database
def add_user(
        db: Session,
        username: str,
        password: str,
        email: str,
        role: Role = Role.BASIC,
)->User | None:

    hashed_password = get_password_hash(password)
    db_user = User(
        username = username,
        email = email,
        hash_password = hashed_password,
        role = role
    )

    db.add(db_user) # # 1. Stage the object for insertion
    try:
        db.commit() # 2. Save changes to the database
        db.refresh(db_user) # 3. Update the object with DB-generated values --> Now new_user.id is available
    except IntegrityError: # Catches duplicate emails, invalid foreign keys, etc.
        db.rollback() # 5. Undo any pending changes
        return None # 6.Return None if the there is an Error raised
    return db_user # 7. Return the created user as Dict (returns the username , email and password)


def get_user(db: Session,email_or_username:str,)-> User | None:
    
    try:
        validate_email(email_or_username)
        query_filter = User.email
    except EmailNotValidError:
        query_filter = User.username
    
    user = (
        db.query(User).filter(query_filter == email_or_username).first()
    )

    return user


