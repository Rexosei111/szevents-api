from fastapi import APIRouter, Query
from .schemas import EventsRead
from organisers.dependencies import get_current_user
from fastapi_pagination import add_pagination
from fastapi_pagination.ext.beanie import paginate
from fastapi_pagination.links import Page

event_router = APIRouter()


@event_router.get("/")
async def get_events(q: str = Query(default="")) -> Page(EventsRead):
    return "event homepage"
