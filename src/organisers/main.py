from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from .dependencies import get_current_user

from .services import (
    check_login_credentials,
    delete_organiser,
    get_organiser_by_id,
    register_new_organiser,
    update_organiser_data,
)
from .schemas import (
    LoginSchema,
    OrganiserCreate,
    OrganiserRead,
    OrganiserUpdate,
    TokenRead,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


organisers_router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/organizers/auth/token")


@organisers_router.get("/")
async def organisers_home(user: str = Depends(get_current_user)):
    print(user)
    return "Organisers home"


@organisers_router.post(
    "/auth/token", include_in_schema=False, response_model=TokenRead
)
async def get_access_token(
    credentials: OAuth2PasswordRequestForm = Depends(),
) -> TokenRead:
    organiser = await check_login_credentials(
        LoginSchema(email=credentials.username, password=credentials.password)  # type: ignore
    )
    Authorize: AuthJWT = AuthJWT()
    access_token = Authorize.create_access_token(subject=str(organiser.id))
    refresh_token = Authorize.create_refresh_token(subject=str(organiser.id))
    return TokenRead(
        access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
    )


@organisers_router.post("/auth/login", response_model=TokenRead)
async def login(credentials: LoginSchema, Authorize: AuthJWT = Depends()):
    organiser = await check_login_credentials(credentials)
    access_token = Authorize.create_access_token(subject=str(organiser.id))
    refresh_token = Authorize.create_refresh_token(subject=str(organiser.id))
    return TokenRead(
        access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
    )


@organisers_router.post("/auth/register", response_model=OrganiserRead)
async def register_organiser(organiser_data: OrganiserCreate):
    organiser = await register_new_organiser(organiser_data)
    return organiser


@organisers_router.get("/me", response_model=OrganiserRead)
async def get_organiser_profile(organiser_id: str = Depends(get_current_user)):
    return await get_organiser_by_id(organiser_id=organiser_id)


@organisers_router.patch("/me", response_model=OrganiserRead)
async def update_organiser_details(
    update_data: OrganiserUpdate,
    organiser_id: str = Depends(get_current_user),
    # token: str = Depends(oauth2_scheme),
):
    db_update = await update_organiser_data(
        organiser_id=organiser_id, update_data=update_data
    )
    return db_update


@organisers_router.delete("/me", response_model=bool)
async def delete_organiser_data(
    organiser_id: str = Depends(get_current_user),
    # token: str = Depends(oauth2_scheme),
):
    await delete_organiser(organiser_id=organiser_id)
    return True
