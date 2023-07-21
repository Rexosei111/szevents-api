from enum import Enum
from typing import Optional
from pydantic import Field, HttpUrl
from beanie import Document, Link, BackLink
from datetime import date, time, datetime


class EventStatus(str, Enum):
    Live = "live"
    Upcoming = "upcoming"
    Past = "Past"
    Draft = "Draft"


class EventLocation(Document):
    address: str = Field(
        ..., description="The short description of the location of the event"
    )
    latitude: str = Field(...)
    longitude: str = Field(...)


class Events(Document):
    name: str = Field(..., description="Name of organiser")
    summary: str = Field(description="A little information about organiser")
    description: Optional[str] = Field(description="About organiser")
    location: Optional[EventLocation]
    coverImage: Optional[HttpUrl] = Field(
        description="This image will also be used in the tickets that will be sent to customers"
    )
    status: Optional[EventStatus] = Field(default=EventStatus.Draft)
    startDate: Optional[datetime]
    startTime: Optional[datetime]
    organiser: Link["Organisers"]


from organisers.models import Organisers
