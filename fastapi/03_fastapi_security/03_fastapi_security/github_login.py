
"""
NOTE:

the proper OAuth flow:

1. Browser is redirected to: `https://github.com/login/oauth/authorize`

Purpose: GitHub login & consent page  
What happens:

- User is redirected to GitHub
- User logs in (if not already logged in)
- User approves your app
- GitHub redirects back with a `code` parameter (temporary authorization code)


2. GitHub redirects browser back to: `http://localhost:8000/github/auth/token?code=<temporary_code>`

Purpose:OAuth callback endpoint (your backend)  
What happens:

- GitHub redirects the user's browser to this URL
- The `code` parameter contains the temporary authorization code
- Your backend receives this code and uses it in step 3 to exchange for an access token


3. Token Exchange (Backend ↔ GitHub):`https://github.com/login/oauth/access_token`

Purpose: Token exchange endpoint the current endpoint that we are building now 
What happens:

- Your backend sends a POST request to this URL with:
    - `client_id`
    - `client_secret`
    - `code` (the temporary code from step 2)
    - `redirect_uri`
- GitHub verifies everything
- GitHub responds with an `access_token`

Key distinction:

- Step 1 & 2: Browser interactions (user-facing redirects)
- Step 3: Server-to-server communication (your backend talks directly to GitHub's API)
"""

import httpx
from fastapi import APIRouter, HTTPException, status
from auth_utils import Token
from github_auth_operations import (
    GITHUB_AUTHORIZATION_URL,
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_REDIRECT_URI,
)

router = APIRouter()

@router.post('/auth/url')
def github_auth():
    """
    this endpoint used to return the URL used by the frontend to redirect the user to github login
    example return :
    
    {
    "auth_url": "https://github.com/login/oauth/authorize?client_id=<id_code>"
    }

    """
    return {
        "auth_url" : GITHUB_AUTHORIZATION_URL
        + f"?client_id={GITHUB_CLIENT_ID}"
    }

@router.get('/github/auth/token',
            response_model = Token)
async def OAuth_callback(code : str):
    """
    This endpoint exchanges a temporary GitHub authorization code for a GitHub access token.

    Flow:
    1. User clicks “Login with GitHub”
    2. Browser is redirected to: https://github.com/login/oauth/authorize -> this URL the user use it for GitHub login & consent page (User is redirected to GitHub,User logs in (if not already) and User approves your app) and Redirects back with: a temporary_code variable
    3. User logs in and approves the application
    4. GitHub redirects back to: http://localhost:8000/github/auth/token?code=<temporary_code> -> this URL used by Github to talk to your backend it is OAuth callback endpoint which is this endpoint. GitHub redirects the browser to this URL and give your backend a GitHub token
    5. This endpoint (github_callback) runs and:
    - Takes the temporary authorization code
    - Sends it to GitHub is /access_token endpoint
    - Proves the app is identity using client_id and client_secret
    - Exchanges the code for a GitHub access token

    Request data sent to GitHub:
    {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GITHUB_REDIRECT_URI
    }

    NOTE :
    - The authorization code is short-lived and can be used only once
    - This endpoint ONLY performs the OAuth exchange
    - It does NOT identify users, access the database, or issue the app is JWT
    - GitHub always gives a temporary `code` first.  
    Then, using that `code` plus your app credentials, that your backend exchanges it for an access token.

    --> The backend sends the client_secret so GitHub can verify that the request is coming from the real, trusted application — 
    not from a random attacker. so The client_secret proves your backend iss identity to GitHub during the token exchange.

    """

    token_reponse = httpx.post(
        "https://github.com/login/oauth/access_token",
        data = {
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI,
            },
            headers={"Accept": "application/json"},
    ).json()

    access_token =  token_reponse.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="User not registered",
        )
    token_type = token_reponse.get(
        "token_type", "bearer"
    )

    return {
        "access_token": access_token,
        "token_type": token_type,
    }