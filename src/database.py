from config import get_settings
from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from organisers.models import Organisers, SocialMediaLinks
from events.models import EventLocation, Events

settings = get_settings()

database_models = [Organisers, SocialMediaLinks, Events, EventLocation]


async def init_mongodb():
    # Create Motor client
    client = AsyncIOMotorClient(settings.mongodb_url)

    # Initialize beanie with the Product document class and a database
    await init_beanie(database=client.myszevents, document_models=database_models)
