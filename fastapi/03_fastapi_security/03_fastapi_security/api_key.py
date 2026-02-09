from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

# ============================================================================
# Helper Functions
# ============================================================================

# This contain the VALID_API_KEYS constent 
VALID_API_KEYS = [
    "apitestkey",
    "anotherapitestkey",
    "moreapitestkey"
]

async def get_api_key(
        api_kei : str
)->str:
    if api_kei not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_kei

# ============================================================================
# Helper Functions
# ============================================================================

router = APIRouter()

@router.get('/secure-resources')
async def get_secure_resources(
    api_key : bool = Depends(get_api_key)
):
    """
    This function you can only access it by giving the rigth API Keys without giving one of them you can't access this endpoint
    """
    return {"message": "Access to secure data granted"} 