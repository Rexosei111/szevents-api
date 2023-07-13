from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, EmailStr

from beanie import Document, Indexed


class contact_types(str, Enum):
    email = ("email",)
    phone = "phone"


class SocialMediaTypes(str, Enum):
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    telegram = "telegram"


class Contacts(Document):
    contact_type: contact_types
    email: EmailStr
    phone: str


class SocialMediaLinks(Document):
    social_media_type: SocialMediaTypes
    url: HttpUrl


class Organisers(Document):
    name: str = Field(..., description="Name of organiser")
    summary: str = Field(description="A little information about organiser")
    description: Optional[str] = Field(description="About organiser")
    logo: Optional[HttpUrl] = Field(description="Url of organisers logo")
    email: EmailStr = Field(..., description="Email address for authentication")
    password: str = Field(..., description="Password for authentication")
    is_active: Optional[bool] = Field(default=True)
    email_addresses: Optional[List[EmailStr]] = Field(
        default=[], description="List of email address for contact"
    )
    phone_numbers: Optional[List[str]] = Field(
        default=[], description="List of phone numbers for contact"
    )
    social_media_links: Optional[List[SocialMediaLinks]] = Field(
        default=[], description="List of social media handles"
    )
