from fastapi import (
    APIRouter,
    Depends,
    Response
)


from sqlalchemy.orm import Session
from database import get_db
from rbac import get_current_user
from operations import get_user
from Responses import UserCreateBody

router = APIRouter()

@router.post('/login')
async def login(
    response: Response, # This where we create and store the cookie  
    db : Session = Depends(get_db),
    decoded_token : UserCreateBody = Depends(get_current_user)

):
    user = get_user(db,decoded_token.username)
    response.set_cookie(
        key = "fakesession", value = f'{user.id}'
    )

    return {"Message" : "User logged with success" }
    

@router.post('/logout')
async def logout(
    response = Response,
    user : UserCreateBody = Depends(get_current_user)
):
    response.delete_cookie(  # Delete the cookie
        "fakesession"
    )

    return {
        "message" : "User logged out successfully"
        }
