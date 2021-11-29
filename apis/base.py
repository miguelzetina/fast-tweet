from fastapi import APIRouter

from apis.v1 import route_auth, route_me, route_users, route_tweets


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(route_auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(route_me.router, prefix="/home", tags=["Home"])
api_router.include_router(route_users.router, prefix="/users", tags=["Users"])
api_router.include_router(route_tweets.router, prefix="/tweets", tags=["Tweets"])
