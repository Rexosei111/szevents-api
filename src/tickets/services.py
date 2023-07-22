from beanie import PydanticObjectId

from organisers.services import get_organiser_by_id
from .models import Tickets
from .schemas import TicketCreate, TicketUpdate
from fastapi.exceptions import HTTPException


async def create_new_ticket(ticket_details: TicketCreate, organiser_id: str):
    organiser = await get_organiser_by_id(organiser_id=organiser_id)
    ticket = Tickets(**ticket_details.dict(), organiser=organiser)  # type: ignore
    new_ticket = await ticket.create()
    return new_ticket


async def get_ticket_by_id(ticket_id: str):
    ticket = await Tickets.find_one(Tickets.id == PydanticObjectId(ticket_id))
    if ticket is None:
        raise HTTPException(404, detail=f"Ticket not found")
    return ticket


async def get_all_tickets():
    tickets = Tickets.find({})
    return tickets


async def get_event_tickets(event_id: str):
    tickets = Tickets.find(Tickets.event.id == event_id, fetch_links=True)
    return tickets


async def update_a_ticket(update_data: TicketUpdate, ticket_id: str, organiser_id: str):
    ticket = await get_ticket_by_id(ticket_id=ticket_id)
    organiser = await ticket.organiser.fetch()
    if organiser.id != PydanticObjectId(organiser_id):
        raise HTTPException(403, detail=f"You are forbidden to perform this action")
    for key, value in update_data.dict(exclude_none=True).items():
        setattr(ticket, key, value)

    result = await ticket.replace()
    return result


async def delete_a_ticket(ticket_id: str, organiser_id: str):
    ticket = await Tickets.find_one(Tickets.id == PydanticObjectId(ticket_id))
    if ticket is None:
        raise HTTPException(404, detail=f"Ticket not found")
    organiser = await ticket.organiser.fetch()
    if str(organiser.id) != organiser_id:  # type: ignore
        raise HTTPException(403, detail=f"You are forbidden to perform this operation")
    await ticket.delete()  # type: ignore
    return True
