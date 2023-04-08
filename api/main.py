from fastapi import FastAPI

from api.configs.Environment import env
from api.metadata.Tags import Tags
from api.models.BaseModel import init
from api.routers.v1.OauthScopeRouter import OauthScopeRouter
from api.routers.v1.TokenRouter import TokenRouter
from api.routers.v1.UserRouter import UserRouter

# Core Application Instance
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

# Add Routers
app.include_router(OauthScopeRouter)
app.include_router(TokenRouter)
app.include_router(UserRouter)

# Initialise Data Model Attributes
init()