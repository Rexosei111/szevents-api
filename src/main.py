from fastapi import FastAPI, Request
import uvicorn
from config import get_settings
from database import init_mongodb
from organisers.main import organisers_router
from tickets.main import ticket_router
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from events.main import event_router
from fastapi_pagination import add_pagination


app = FastAPI()

add_pagination(app)


@AuthJWT.load_config
def get_config():
    return get_settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(organisers_router, prefix="/organizers", tags=["Organisers"])
app.include_router(event_router, prefix="/events", tags=["Events"])
app.include_router(ticket_router, prefix="/tickets", tags=["Tickets"])


@app.on_event("startup")
async def startup_events():
    await init_mongodb()


if __name__ == "__main__":
    uvicorn.run("main:app", log_level="info", reload=True, host="127.0.0.1", port=8000)
