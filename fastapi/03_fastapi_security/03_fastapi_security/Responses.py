from pydantic import BaseModel,EmailStr,Field
from typing import Annotated

class UserCreateBody(BaseModel):
    """
    what should a Person input when he want to create a user
    """
    username: str
    email: EmailStr
    password: str


class UserCreateResponse(BaseModel):
    """
    Response model for ship data returned by the API. Part of the returned Model with ResponseCreateUser class
    """
    username: str
    email: EmailStr

class ResponseCreateUser(BaseModel):
    """
    Response model for ship data returned by the API when a User has been Created succefully
    """
    message: Annotated[str,Field(default = 'User Created')]
    User : UserCreateResponse

class UserGetResponse(BaseModel):
    username: str
    role : str