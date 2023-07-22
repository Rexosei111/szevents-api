from typing import Optional
from .models import Events
from .schemas import EventCreate, EventUpdate
from organisers.services import get_organiser_by_id
from fastapi.exceptions import HTTPException
from beanie import PydanticObjectId


async def get_all_events(q: Optional[str] = None):
    events = Events.find({})
    return events


async def create_new_event(data: EventCreate, organiser_id: str):
    organiser = await get_organiser_by_id(organiser_id=organiser_id)
    if organiser is None:
        raise HTTPException(404, detail=f"Organiser not found")
    new_event = Events(**data.dict(), organiser=organiser)  # type: ignore
    return await new_event.create()


async def get_event_by_id(event_id: str):
    event = await Events.find_one(Events.id == PydanticObjectId(event_id))
    if event is None:
        raise HTTPException(401, detail=f"Event does not exist")
    return event


async def update_event(update_data: EventUpdate, event_id: str, organiser_id: str):
    event = await get_event_by_id(event_id=event_id)
    organiser = await event.organiser.fetch()
    if str(organiser.id) != organiser_id:  # type: ignore
        raise HTTPException(403, detail=f"You are forbidden to update event")
    for key, value in update_data.dict(exclude_none=True).items():
        setattr(event, key, value)

    result = await event.replace()  # type: ignore
    return result


async def delete_event(event_id: str, organiser_id: str):
    event = await Events.find_one(Events.id == PydanticObjectId(event_id))
    if event is None:
        raise HTTPException(404, detail=f"Event not found")
    organiser = await event.organiser.fetch()
    if str(organiser.id) != organiser_id:  # type: ignore
        raise HTTPException(403, detail=f"You are forbidden to perform this operation")
    await event.delete()  # type: ignore
    return True
