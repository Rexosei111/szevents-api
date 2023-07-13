from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/organizers/auth/token")


async def get_current_user(
    Authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)
):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return current_user
