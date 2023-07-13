from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class SocialMediaTypes(str, Enum):
    facebook = "facebook"
    instagram = "instagram"
    twitter = "twitter"
    telegram = "telegram"


class SocialMediaLinks(BaseModel):
    social_media_type: SocialMediaTypes
    url: HttpUrl


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenRead(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class BaseOrganiser(BaseModel):
    name: str = Field(..., description="Name of organiser")
    summary: str = Field(description="A little information about organiser")
    description: Optional[str] = Field(description="About organiser")
    logo: Optional[HttpUrl] = Field(description="Url of organisers logo")


class OrganiserCreate(BaseOrganiser):
    email: EmailStr = Field(..., description="Email address for authentication")
    password: str = Field(...)


class OrganiserRead(BaseOrganiser):
    email_addresses: Optional[List[EmailStr]] = Field(
        description="List of email address for contact"
    )
    phone_numbers: Optional[List[str]] = Field(
        description="List of phone numbers for contact"
    )
    social_media_links: Optional[List[SocialMediaLinks]] = Field(
        description="List of social media handles"
    )


class OrganiserUpdate(BaseModel):
    name: Optional[str] = Field(description="Name of organiser")
    summary: Optional[str] = Field(description="A little information about organiser")
    description: Optional[str] = Field(description="About organiser")
    logo: Optional[HttpUrl] = Field(description="Url of organisers logo")
    email: Optional[EmailStr] = Field(description="Email address for authentication")
    password: Optional[str]
