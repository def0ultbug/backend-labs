import bcrypt
from sqlalchemy.orm import Session
from operations import get_user
from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from models import User
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    
)

from database import get_db

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from pydantic import BaseModel


def verify_password(plain_pass:str,hash_pass:str)->bool:
    """
    Verify a plain password against a hashed password using bcrypt  
    """
    return bcrypt.checkpw(plain_pass.encode('utf-8'), hash_pass.encode('utf-8'))


def auth_user(db : Session,user_or_email : str , password : str):
    user = get_user(db,user_or_email)
    if not verify_password(password,user.hash_password):
        return None
    return user 


### To create the access token we need to specify a secret key, the algorithm used to generate it, and the expiration time,###

# JWT configuration variables
SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# now create the create_access_token function

def create_access_token(data:dict)->str:
    """
    Create a JWT access token with an optional expiration delta.

    This is what data contain for example
    data = {
        "sub": "sheldonsonny",  # "sub" (subject) - typically the username or user ID
        "user_id": 123,          # Optional: numeric user ID
        "email": "sheldonsonny@email.com",  # Optional: user email
        # any other custom claims you want to include
    }
    """
    to_encode = data.copy() # make a copy of the data dict
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # contain the expriration time of the Token
    to_encode.update({'exp':expire}) # add the expriration time into the data dict
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM) # Create the Token with the algorithm that we specified
    return encode_jwt


"""
- You have data variable that is dict so when you generate a token it will be tyoe :str and when you want to decode that String Token 
it return into the data variable of type dict 

You have a data variable of type dict. When you encode it using jwt.encode(), it generates a token of type str. 
When you decode that string token using jwt.decode(), it returns back to a dict containing the original data plus
any added claims like expiration time.

1. Encoding (dict → token string):
    data = {"sub": "sheldonsonny", "user_id": 123}
    token = create_access_token(data)
    #Output :  token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGVsZG9uc29ubnkiLCJ1c2VyX2lkIjoxMjMsImV4cCI6MTczODg3NjU0M30.signature_here"

2.Decoding (token string → dict):
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #Output : decoded_data = {"sub": "sheldonsonny", "user_id": 123, "exp": 1738876543}

"""

def decode_access_token(
        token:str,
        db: Session
)-> User | None:
    try:
        payload = jwt.decode(
            token,SECRET_KEY,algorithms=[ALGORITHM]
        )

        username :str = payload.get("sub")

    except JWTError:
        return None
    
    if not username:
        return None
    
    user = get_user(db,username)
    return user

router = APIRouter()

class Token(BaseModel):
    access_token : str
    token_type : str


# This function is a login endpoint that authenticates a user and returns a JWT access token
@router.post("/token/create",response_model= Token)
def get_user_access_token(
    form_data : OAuth2PasswordRequestForm = Depends(), # Receives login credentials (username and password)
    session : Session = Depends(get_db)):
    
    """
    So it get's username and password from the request
    and then it calls auth_user() --> to verify the credentials "checks if username exists and password hash matches"
    If credentials are invalid, returns a 401 Unauthorized error
    Generates a JWT token containing the username --> This Token that proves the user is authenticated
    and then return the Token
    """


    user = auth_user(
        session,
        form_data.username,
        form_data.password
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token = create_access_token(
        data={
            "sub" : user.username
        }
    )

    return {
        "access_token" : access_token,
        "token_type" : "bearer",
    }
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # 

@router.get('/users/me')
def read_user_me(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    """
    So when a User access to an endpoint 
    This see if that user has token means if the user is authenticated and raise an Error if the credentials are invalid
    If no token is present, FastAPI automatically returns 401 Unauthorized
    If token is present, it extracts the token string and passes it to your function
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_data = decode_access_token(token,db)

    if not user_data:
        raise credentials_exception
    return {
        "description" : f"{user_data.username} is authorized",
    }

