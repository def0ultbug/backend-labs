import pyotp

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session 

from database import get_db
from operations import get_user
from rbac import get_current_user
from Responses import UserGetResponse

"""
Typical flow for the functions:

    secret = generate_totp_secret()  # Save this in DB
    uri = generate_totp_uri(secret, "user@example.com")  # Convert to QR code
    # User scans QR → App generates codes → Verify with secret
"""

# ============================================================================
# Helper Functions
# ============================================================================

def generate_totp_secret()-> str:
    """
    Generates a random secret key in Base32 format (like JBSWY3DPEHPK3PXP).
    Should be kept secure and never shared with anyone except the user during setup
    it must be :
        - Unique for each user
        - Stored in your database
    """
    return pyotp.random_base32()



def generate_totp_uri(secret, user_email)-> str:
    """
    Creates a provisioning URI that authenticator apps can use to set up 2FA
    parameters:
        - name=user_email - Identifies which account this is for
        - issuer_name="FastAPI-auth" - Your app's name

    NOTE : This URI Encoded into a QR code that users scan with Google Authenticator, Authy, etc.
    After scanning, the app generates 6-digit codes that has a short period of 30 seconds

    """
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_email, issuer_name="FastAPI-auth"
    )

### Now make the Endpoints for MFA ###

# ============================================================================
# API Endpoints
# ============================================================================

routers = APIRouter()

# This endpoint to give you the Code of the MFA
@routers.post('/user/enable-mfa')
def enable_mfa(
    current_user : UserGetResponse = Depends(get_current_user), # This gets the username when it decoded the Token so you need to be authenticated in order to access this endpoint for more checks 
    db : Session = Depends(get_db)
):
    
    user_in_db = get_user(db, current_user.username) # Get full user from database
    
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    secret = generate_totp_secret() # generate a secret key
    uri = generate_totp_uri(secret, current_user.username) # Generate provisioning URI for QR code

    # Save secret to database
    user_in_db.mfa_secret = secret
    db.commit()
    db.refresh(user_in_db)

    return {
        "secret": secret,
        "provisioning_uri": uri,
        "message": "Scan QR code with authenticator app"
    }


# This endpoint to check if you input the correct Code or not 
@routers.post('/verify-MFA-code')
def verify(
    code : str,
    db : Session = Depends(get_db),
    current_user : UserGetResponse = Depends(get_current_user), # This gets the username when it decoded the Token so you need to be authenticated in order to access this endpoint for more checks 
)-> str:
    """
    Verify a TOTP code from the user's authenticator app.
    
    Args:
        code: 6-digit TOTP code from authenticator app
    
    Returns:
        dict: Success message with username
    
    Raises:
        HTTPException(404): User not found in database
        HTTPException(401): Invalid or expired TOTP code
    
    Note:
        Codes are valid for 30 seconds. This endpoint should be called
        after initial MFA setup or during login to verify the second factor.
    """
    
    # 1. Verify user exists
    user_in_db = get_user(db,current_user.username) # Get full user from database
    
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
    )

    # 2. Check if MFA is set up for this user
    if not user_in_db.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA not enabled for this user"
        )
    # 3. Verify the TOTP code
    totp = pyotp.TOTP(user_in_db.mfa_secret)
    if not totp.verify(code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TOTP token",
        )
    # Proceed with granting access
    # or performing the sensitive operation
    return "message: TOTP token verified successfully \n" + f"welcome {user_in_db.username}"

    