from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TicketBase(BaseModel):
    name: str = Field(
        ..., description="Name/type of ticket. Examples - Regular, VIP, PRO"
    )
    price: float = Field(
        ..., description="Price of this ticket. Take into consideration the charges"
    )
    quantity: Optional[int] = Field(description="Quantity of this ticket to be sold")
    quantity_sold: Optional[int] = Field(default=0)
    startDate: Optional[datetime]
    endDate: Optional[datetime]


class TicketCreate(TicketBase):
    ...


class TicketReadWithId(TicketBase):
    id: Optional[PydanticObjectId] = Field()


class TicketRead(TicketBase):
    id: Optional[PydanticObjectId] = Field(alias="_id")


class TicketUpdate(BaseModel):
    name: Optional[str] = Field(
        description="Name/type of ticket. Examples - Regular, VIP, PRO"
    )
    price: Optional[float] = Field(
        description="Price of this ticket. Take into consideration the charges"
    )
    quantity: Optional[int] = Field(description="Quantity of this ticket to be sold")
    quantity_sold: Optional[int] = Field(default=0)
    startDate: Optional[datetime]
    endDate: Optional[datetime]
