from fastapi import FastAPI

from api.configs.Environment import env
from api.metadata.Tags import Tags
from api.models.BaseModel import init
from api.routers.v1.RoleRouter import RoleRouter
from api.routers.v1.TokenRouter import TokenRouter, PublicTokenRouter
from api.routers.v1.UserRouter import UserRouter, PublicUserRouter
from api.routers.v1.PermissionRouter import PermissionRouter

# Core Application Instance
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

# Add Routers
app.include_router(RoleRouter)
app.include_router(PublicUserRouter)
app.include_router(UserRouter)
app.include_router(PublicTokenRouter)
app.include_router(TokenRouter)
app.include_router(PermissionRouter)

# Initialise Data Model Attributes
init()