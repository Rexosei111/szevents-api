from beanie import Document, Link
from pydantic import Field
from typing import Optional
from datetime import datetime


class Tickets(Document):
    name: str = Field(
        ..., description="Name/type of ticket. Examples - Regular, VIP, PRO"
    )
    price: float = Field(
        ..., description="Price of this ticket. Take into consideration the charges"
    )
    quantity: Optional[int] = Field(
        ..., description="Quantity of this ticket to be sold"
    )
    quantity_sold: Optional[int] = Field(default=0)
    startDate: Optional[datetime]
    endDate: Optional[datetime]
    event: Optional[Link["Events"]]
    organiser: Link["Organisers"]


from events.models import Events
from organisers.models import Organisers
