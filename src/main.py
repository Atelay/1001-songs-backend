from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from sqladmin import Admin

from src.config import (
    settings,
    ALLOW_HEADERS,
    ALLOW_METHODS,
    EXPOSE_HEADERS,
    ORIGINS,
    PROJECT_NAME,
    SWAGGER_PARAMETERS,
    API_PREFIX,
)
from src.admin import __all__ as views
from src.utils import lifespan
from src.middlewares import add_process_time_header, logger_middleware
from src.database.database import engine, async_session_maker
from src.admin.auth import authentication_backend
from src.auth.routers import auth_router
from src.payment.routers import payment_router
from src.footer.routers import footer_router
from src.our_team.routers import team_router
from src.education.routers import education_router
from src.about.routers import about_router
from src.location.routers import location_router, map_router
from src.news.routers import news_router
from src.expedition.routers import expedition_router
from src.our_project.routers import project_router
from src.partners.routers import partners_router


app = FastAPI(
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title=PROJECT_NAME,
    lifespan=lifespan,
)

admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    logo_url="/static/interface/logo.svg",
    session_maker=async_session_maker,
)
admin.site_url = settings.SITE_URL

app.mount("/static", StaticFiles(directory="static"), name="static")
api_routers = [
    auth_router,
    payment_router,
    footer_router,
    partners_router,
    team_router,
    about_router,
    location_router,
    map_router,
    education_router,
    news_router,
    expedition_router,
    project_router,
]

[app.include_router(router, prefix=API_PREFIX) for router in api_routers]

[admin.add_view(view) for view in views]


app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.add_middleware(BaseHTTPMiddleware, dispatch=logger_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
    expose_headers=EXPOSE_HEADERS,
)

add_pagination(app)
