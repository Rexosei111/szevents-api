from typing import List
from fastapi import APIRouter, Depends, Query

from .services import (
    create_new_ticket,
    delete_a_ticket,
    get_event_tickets,
    get_ticket_by_id,
    update_a_ticket,
    get_all_tickets,
)
from .schemas import TicketCreate, TicketRead, TicketReadWithId, TicketUpdate
from organisers.dependencies import get_current_user
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

ticket_router = APIRouter()


@ticket_router.get("/")
async def get_tickets(q: str = Query(default="")) -> Page[TicketReadWithId]:
    tickets = await get_all_tickets()

    return await paginate(tickets)


@ticket_router.get("/{ticket_id}", response_model=TicketRead)
async def get_a_ticket(ticket_id: str):
    ticket = await get_ticket_by_id(ticket_id=ticket_id)
    return ticket


@ticket_router.post("/", response_model=TicketRead)
async def add_new_ticket(
    ticket_data: TicketCreate, organiser_id: str = Depends(get_current_user)
):
    ticket = await create_new_ticket(
        ticket_details=ticket_data, organiser_id=organiser_id
    )
    return ticket


@ticket_router.patch("/{ticket_id}", response_model=TicketRead)
async def update_event_details(
    update_data: TicketUpdate,
    ticket_id: str,
    organiser_id: str = Depends(get_current_user),
):
    updated_ticket = await update_a_ticket(
        update_data=update_data, ticket_id=ticket_id, organiser_id=organiser_id
    )
    return updated_ticket


@ticket_router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: str, organiser_id: str = Depends(get_current_user)):
    await delete_a_ticket(ticket_id, organiser_id)
    return True
