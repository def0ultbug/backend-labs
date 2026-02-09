import uvicorn
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
)

from auth_utils import router as auth_route
import uvicorn
from contextlib import asynccontextmanager
from database import shutdown_database,init_database,get_db
from operations import add_user
from sqlalchemy.orm import Session
from Responses import (
    ResponseCreateUser,
    UserCreateBody,
    UserCreateResponse,
)

from github_auth_operations import resolve_github_token

from premium_access import router as prem_router
from rbac import router as rbac_route
from github_login import router as github_router 
from mfa import routers as mfa_router
from api_key import router as key_router
from user_session import router as user_session_router

@asynccontextmanager
async def lifespan(app : FastAPI):
    """
    event handler for FastAPI Apps it manages database configs
    """
    #starts - create the database tables
    init_database()
    yield
    # shutdown the database session
    shutdown_database()

app = FastAPI(
    title = "API with auth",
    lifespan = lifespan # lifespan of the API
) 

app.include_router(auth_route)
app.include_router(prem_router)
app.include_router(rbac_route)
app.include_router(github_router)
app.include_router(mfa_router)
app.include_router(key_router)
app.include_router(user_session_router)

@app.post('/register/basic_user',status_code=status.HTTP_201_CREATED,response_model=ResponseCreateUser)
def register(user: UserCreateBody,
                   session: Session = Depends(get_db) # Pass the Database session (Dependancy Injection) 
                   )-> dict[str,UserCreateResponse]:
    user =  add_user(
        db = session, # Inject the database session
        **user.model_dump()
    )

    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists",
        )
    user_response = UserCreateResponse(
        username = user.username,
        email = user.email
    )

    return {
        "message" : "User Created",
        "User" : user_response
    }

@app.get("/home",responses={status.HTTP_403_FORBIDDEN: {"description": "token not valid"}})
def homepage(user : UserCreateResponse = Depends(resolve_github_token))->str:
    return {"message": f"logged in {user.username} !"}


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()