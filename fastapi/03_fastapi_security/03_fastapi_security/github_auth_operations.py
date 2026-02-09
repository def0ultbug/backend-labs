import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session

from database import get_db 
from models import User
from operations import get_user

"""
NOTE : in production env don't put those varaible and put them in an .env file and load them
"""
# Constant varaibles 
GITHUB_CLIENT_ID = "<code>"
GITHUB_CLIENT_SECRET = (
    "<SECRET>"
)
GITHUB_REDIRECT_URI = (
    "http://localhost:8000/github/auth/token"
)
GITHUB_AUTHORIZATION_URL = (
    "https://github.com/login/oauth/authorize"
)



"""
tells FastAPI that there is a Token need to be extracted
My API expects an OAuth2 Authorization Code token, and GitHub is the provider
My API expects requests that contain an OAuth2 Bearer token issued by GitHub
"""
github_oauth_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize", # this URL the user use it for GitHub login & consent page (User is redirected to GitHub,User logs in (if not already) and User approves your app) and Redirects back with: a temporary_code variable
    tokenUrl="https://github.com/login/oauth/access_token" # this URL your backend use it for Token exchange endpoint after you have the temporary_code variable from the first URL (/login/oauth/authorize) so the Backend sends:client_id,client_secret,code,edirect_uri) and then GitHub verifies everything then GitHub issues an access token 
    )

def resolve_github_token(
        access_token : str = Depends(github_oauth_scheme),
        db : Session = Depends(get_db)        
)-> User:
    """
    Take a GitHub access token, call GitHub API, get user info, map it to my DB user, return User
    This function should be used AFTER OAuth login.
    Details :
    So now we make a function that **extract** the GitHub access token from the **request header** and calls the GitHub API and sees if that Token is valide if it is not valide 
    it return Error or if it is valide  it decoded the Token (get user info)  and sees the information from in the decoded token (like username and email) 
    are  available in the database so if those information are in the database it give access to that user if not it raise Error

    Flow should be:
    Frontend → GitHub OAuth
    GitHub → returns access_token
    Frontend → sends token to your backend
    Backend → resolve_github_token
    Backend → creates your own JWT
    Frontend → uses your JWT, NOT GitHub token
    NOTE: Never use GitHub tokens as your app token auth token.
    """
    user_response = httpx.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        },
    ).json()

    username = user_response.get("login")
    user = get_user(db,username) # give the extracted username to the database to see if that username stored in the database

    if not user:
        email = user_response.get("email")
        user = get_user(db,email) # give the extracted email to the database to see if that email stored in the database

    
    if not user:
        raise HTTPException(status_code=403, detail="User not registered")
    return User



    