
from database import get_db
from Responses import (
    ResponseCreateUser,
    UserCreateBody,
    UserCreateResponse
    )


from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from models import Role

from operations import add_user

router = APIRouter()

@router.post('/register/premium-user',
             response_model=ResponseCreateUser,
             status_code=status.HTTP_201_CREATED,
             responses={
        status.HTTP_409_CONFLICT: {
            "description": "The user already exists"
        },
        status.HTTP_201_CREATED: {
            "description": "User created"
        }},)
def resgister(user:UserCreateBody,
              session : Session = Depends(get_db))->dict[str,UserCreateResponse]:
        user =  add_user(
        db = session, # Inject the database session
        **user.model_dump(),
        role=Role.PREMIUM)

        if not user:
              raise HTTPException(
                     status.HTTP_409_CONFLICT,
                    "username or email already exists",
                    )
        user_res = UserCreateResponse(
               username= user.username,
               email = user.email 
        )

        return {
               'message' : 'User Created',
               'User' : user_res
        }


