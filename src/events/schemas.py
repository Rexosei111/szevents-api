from datetime import date, time, datetime
from enum import Enum
from typing import Optional
from beanie import PydanticObjectId

from pydantic import BaseModel, Field, HttpUrl


class EventStatus(str, Enum):
    Live = "live"
    Upcoming = "upcoming"
    Past = "Past"
    Draft = "Draft"


class EventLocation(BaseModel):
    address: str = Field(
        ..., description="The short description of the location of the event"
    )
    latitude: str = Field(...)
    longitude: str = Field(...)


class EventBase(BaseModel):
    # id: Optional[PydanticObjectId] = Field(alias="_id")
    name: str = Field(..., description="Name of organiser")
    summary: Optional[str] = Field(description="A little information about organiser")
    description: Optional[str] = Field(description="About organiser")
    location: Optional[EventLocation]
    coverImage: Optional[HttpUrl] = Field(
        description="This image will also be used in the tickets that will be sent to customers"
    )
    status: Optional[EventStatus] = Field(default=EventStatus.Draft)
    startDate: Optional[datetime]
    startTime: Optional[datetime]


class EventsReadWithId(EventBase):
    id: Optional[PydanticObjectId] = Field()


class EventsRead(EventBase):
    id: Optional[PydanticObjectId] = Field(alias="_id")


class EventCreate(EventBase):
    ...


class EventUpdate(BaseModel):
    name: Optional[str] = Field(description="Name of organiser")
    summary: Optional[str] = Field(description="A little information about organiser")
    description: Optional[str] = Field(description="About organiser")
    location: Optional[EventLocation]
    coverImage: Optional[HttpUrl] = Field(
        description="This image will also be used in the tickets that will be sent to customers"
    )
    # status: Optional[EventStatus] = Field(default=EventStatus.Draft)
    startDate: Optional[datetime]
    startTime: Optional[datetime]
