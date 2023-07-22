from typing import List
from fastapi import APIRouter, Depends, Query

from tickets.schemas import TicketRead

from .services import (
    create_new_event,
    delete_event,
    get_all_events,
    get_event_by_id,
    update_event,
)
from .schemas import EventCreate, EventUpdate, EventsRead, EventsReadWithId
from organisers.dependencies import get_current_user
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page
from tickets.services import get_event_tickets as get_event_assigned_tickets

event_router = APIRouter()


@event_router.get("/")
async def get_events(q: str = Query(default="")) -> Page[EventsReadWithId]:
    events = await get_all_events(q=q)
    return await paginate(events)


@event_router.get("/{event_id}", response_model=EventsRead)
async def get_an_event(event_id: str):
    event = await get_event_by_id(event_id=event_id)
    return event


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


@event_router.delete("/{event_id}")
async def delete_an_event(event_id: str, organiser_id: str = Depends(get_current_user)):
    await delete_event(event_id, organiser_id)
    return True


@event_router.get("/{event_id}/tickets", response_model=List[TicketRead])
async def get_event_tickets(
    event_id: str, organiser_id: str = Depends(get_current_user)
):
    tickets = await get_event_assigned_tickets(event_id=event_id)
    return await tickets.to_list()
