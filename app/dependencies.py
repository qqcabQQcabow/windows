import jwt
from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .infrastructure.auth_utils import decode_jwt_token

security = HTTPBearer()

async def get_jwt_payload(authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)] ):

    token = authorization.credentials

    try:
        return decode_jwt_token(token)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unknow error {e}"
        )
