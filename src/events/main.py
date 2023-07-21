from typing import List
from fastapi import APIRouter, Depends, Query

from .services import create_new_event, get_all_events, update_event
from .schemas import EventCreate, EventUpdate, EventsRead
from organisers.dependencies import get_current_user
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

event_router = APIRouter()


@event_router.get("/")
async def get_events(q: str = Query(default="")) -> Page[EventsRead]:
    events = await get_all_events(q=q)
    return await paginate(events)


@event_router.post("/", response_model=EventsRead)
async def add_new_event(
    event_data: EventCreate, organiser_id: str = Depends(get_current_user)
):
    event = await create_new_event(data=event_data, organiser_id=organiser_id)
    return event


@event_router.patch("/{event_id}", response_model=EventsRead)
async def update_event_details(
    update_data: EventUpdate,
    event_id: str,
    organiser_id: str = Depends(get_current_user),
):
    updated_event = await update_event(
        update_data=update_data, event_id=event_id, organiser_id=organiser_id
    )
    return updated_event
