from operations import add_user
from models import User,Role

# User is the table name

def test_add_user_function(db):
    user = add_user(
        session=db,
        username="test",
        password="azzzzz",
        email="test1@email.com",
    )
    
    assert (
        db.query(User).filter(User.id == user.id).first() == user
    )