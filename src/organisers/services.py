from fastapi import HTTPException

from .schemas import LoginSchema, OrganiserCreate, OrganiserUpdate

from .utils import get_password_hash, verify_password
from .models import Organisers
from beanie.odm.operators.update.general import Set


async def check_login_credentials(credentials: LoginSchema) -> Organisers:
    organiser = await Organisers.find_one(Organisers.email == credentials.email)
    if organiser is None:
        raise HTTPException(
            status_code=404, detail="Organiser with this email not found"
        )

    if organiser.is_active is False:
        raise HTTPException(status_code=401, detail="Activate your account")
    is_password_correct = verify_password(credentials.password, organiser.password)
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Incorrect password")
    return organiser


async def register_new_organiser(organiser_data: OrganiserCreate):
    existing_organiser = await Organisers.find_one(
        Organisers.email == organiser_data.email
    )
    if existing_organiser:
        raise HTTPException(
            status_code=400, detail="Organiser with this email already exists"
        )
    hashed_password = get_password_hash(organiser_data.password)
    organiser_data.password = hashed_password
    new_organiser = Organisers(**organiser_data.__dict__)
    return await new_organiser.create()


async def get_organiser_by_id_with_events(organiser_id: str):
    organiser = await Organisers.get(organiser_id, fetch_links=True)
    return organiser


async def get_organiser_by_id(organiser_id: str):
    organiser = await Organisers.get(organiser_id)
    return organiser


async def update_organiser_data(organiser_id: str, update_data: OrganiserUpdate):
    organiser = await Organisers.get(organiser_id)
    if organiser is None:
        raise HTTPException(status_code=404, detail="Organiser not found")
    for key, value in update_data.dict(exclude_none=True).items():
        if key == "password":
            value = get_password_hash(value)
        setattr(organiser, key, value)

    result = await organiser.replace()  # type: ignore
    return result


async def delete_organiser(organiser_id: str):
    organiser = await Organisers.get(organiser_id)
    if organiser is None:
        raise HTTPException(status_code=404, detail="Organiser not found")
    organiser.is_active = False  # type: ignore
    await organiser.replace()  # type: ignore
    return True
