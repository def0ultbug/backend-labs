from sqlalchemy.orm import Session

from database import get_db

from typing import Annotated

from auth_utils import (
    oauth2_scheme,
    decode_access_token
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from models import Role

from Responses import UserGetResponse


def get_current_user(
        db : Session = Depends(get_db),
        token : str = Depends(oauth2_scheme) # extract automaticly the token from the request header
        ) -> UserGetResponse:

    """
    This take the Token of the user that accessd this endpoint and then decoded 
    See if the user is valide if not it raise Error
    and Returns user data if valid, raises 401 if not
    """

    user = decode_access_token(token,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return UserGetResponse(
        username = user.username,
        role = user.role
    )


def get_permeiur_user(
        current_user: Annotated[UserGetResponse, Depends(get_current_user)]
        )-> str:
    if current_user.role != Role.PREMIUM:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return current_user

router = APIRouter()


@router.post('/welcame/all-users')
def all_users_can_access(
    user : Annotated[UserGetResponse,Depends(get_current_user)]
)-> str:
    """
    when a user access this function It calls "get_current_user" function that get's it token 
    see if that user is authenticated if not it raise an Error
    and then it get is information from the Token and 
    return :
    for example : welcome testname
                  Welcome to your space


    """
    return {f'welcome {user.username}\n',"Welcome to your space"}


@router.post('/welcome/premium-user',
             responses={
                 status.HTTP_401_UNAUTHORIZED: {
                     "description": "User not authorized"
                     }},)
def get_premium_user(current_user : Annotated[UserGetResponse,Depends(get_permeiur_user)]):
    """
    when a user access this function It calls "get_permeiur_user" function that get's it token 
    see if that user is authenticated and see if the current user is permeiur user 
    if not it raise an Error
    and then it get is information from the Token and 

    only the permeiur user can access this endpoint

    """
    return {f'Welcome {current_user.username}', 'Welcome to your premirum space'}
    